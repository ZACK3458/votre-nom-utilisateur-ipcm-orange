"""Collecte SNMP avancée pour interfaces réseau selon spécifications IPCM.

Ce module collecte les données SNMP des interfaces selon les OIDs standards
et calcule l'utilisation des interfaces pour le monitoring temps réel.
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import time

try:
    from pysnmp.hlapi import (
        getCmd, nextCmd, SnmpEngine, CommunityData, UdpTransportTarget, 
        ContextData, ObjectType, ObjectIdentity
    )
    from pysnmp.proto.rfc1902 import Integer, OctetString, Counter32, Counter64
    _HAS_PYSNMP = True
except Exception:  # ImportError ou autre
    _HAS_PYSNMP = False

from ..inventory.models import Interface, InterfaceStatus


# OIDs SNMP standards pour les interfaces (RFC 2863)
SNMP_OIDS = {
    'if_descr': '1.3.6.1.2.1.2.2.1.2',      # ifDescr
    'if_type': '1.3.6.1.2.1.2.2.1.3',       # ifType
    'if_mtu': '1.3.6.1.2.1.2.2.1.4',        # ifMtu
    'if_speed': '1.3.6.1.2.1.2.2.1.5',      # ifSpeed
    'if_phys_address': '1.3.6.1.2.1.2.2.1.6', # ifPhysAddress
    'if_admin_status': '1.3.6.1.2.1.2.2.1.7', # ifAdminStatus
    'if_oper_status': '1.3.6.1.2.1.2.2.1.8',  # ifOperStatus
    'if_in_octets': '1.3.6.1.2.1.2.2.1.10',   # ifInOctets
    'if_out_octets': '1.3.6.1.2.1.2.2.1.16',  # ifOutOctets
    'if_in_errors': '1.3.6.1.2.1.2.2.1.14',   # ifInErrors
    'if_out_errors': '1.3.6.1.2.1.2.2.1.20',  # ifOutErrors
    # High Capacity Counters (64-bit) pour les interfaces rapides
    'if_hc_in_octets': '1.3.6.1.2.1.31.1.1.1.6',   # ifHCInOctets
    'if_hc_out_octets': '1.3.6.1.2.1.31.1.1.1.10',  # ifHCOutOctets
    'if_name': '1.3.6.1.2.1.31.1.1.1.1',            # ifName
    'if_alias': '1.3.6.1.2.1.31.1.1.1.18',          # ifAlias
    'if_high_speed': '1.3.6.1.2.1.31.1.1.1.15',     # ifHighSpeed (Mbps pour interfaces >20Mbps)
}

# Mapping des statuts SNMP vers nos enums
STATUS_MAPPING = {
    1: InterfaceStatus.UP,
    2: InterfaceStatus.DOWN,
    3: InterfaceStatus.TESTING,
    4: InterfaceStatus.UNKNOWN,
    5: InterfaceStatus.UNKNOWN,  # dormant
    6: InterfaceStatus.UNKNOWN,  # notPresent
    7: InterfaceStatus.ADMIN_DOWN,  # lowerLayerDown
}


class SNMPCollector:
    """Collecteur SNMP pour équipements réseau."""
    
    def __init__(self, ip: str, community: str = "public", port: int = 161, timeout: int = 3, retries: int = 2):
        self.ip = ip
        self.community = community
        self.port = port
        self.timeout = timeout
        self.retries = retries
        self._engine = None
        self._community_data = None
        self._transport_target = None
        
        if _HAS_PYSNMP:
            self._engine = SnmpEngine()
            self._community_data = CommunityData(community)
            self._transport_target = UdpTransportTarget((ip, port), timeout=timeout, retries=retries)

    def is_available(self) -> bool:
        """Vérifie si SNMP est disponible."""
        return _HAS_PYSNMP and self._engine is not None

    def test_connectivity(self) -> bool:
        """Test de connectivité SNMP basique."""
        if not self.is_available():
            return False
        
        try:
            # Test avec sysDescr (1.3.6.1.2.1.1.1.0)
            result = self._get_single_oid('1.3.6.1.2.1.1.1.0')
            return result is not None
        except Exception:
            return False

    def _get_single_oid(self, oid: str) -> Optional[Any]:
        """Récupère une seule valeur SNMP."""
        if not self.is_available():
            return None
        
        try:
            iterator = getCmd(
                self._engine,
                self._community_data,
                self._transport_target,
                ContextData(),
                ObjectType(ObjectIdentity(oid))
            )
            
            for (errorIndication, errorStatus, errorIndex, varBinds) in iterator:
                if errorIndication or errorStatus:
                    return None
                
                for varBind in varBinds:
                    return varBind[1]
        except Exception:
            return None

    def _walk_oid(self, oid: str) -> List[Tuple[str, Any]]:
        """Effectue un SNMP walk sur un OID."""
        if not self.is_available():
            return []
        
        results = []
        try:
            iterator = nextCmd(
                self._engine,
                self._community_data,
                self._transport_target,
                ContextData(),
                ObjectType(ObjectIdentity(oid)),
                lexicographicMode=False,
                maxRows=1000  # Limite pour éviter les boucles infinies
            )
            
            for (errorIndication, errorStatus, errorIndex, varBinds) in iterator:
                if errorIndication or errorStatus:
                    break
                
                for varBind in varBinds:
                    # Extraire l'index de l'interface du OID
                    oid_parts = str(varBind[0]).split('.')
                    if len(oid_parts) >= 2:
                        interface_index = oid_parts[-1]
                        results.append((interface_index, varBind[1]))
        except Exception:
            pass
        
        return results

    def collect_interface_indices(self) -> List[int]:
        """Collecte tous les index d'interfaces disponibles."""
        indices = []
        for index, _ in self._walk_oid(SNMP_OIDS['if_descr']):
            try:
                indices.append(int(index))
            except ValueError:
                continue
        return sorted(indices)

    def collect_interface_data(self, if_index: int) -> Optional[Dict[str, Any]]:
        """Collecte les données d'une interface spécifique."""
        if not self.is_available():
            return self._generate_simulated_interface_data(if_index)
        
        data = {'if_index': if_index, 'last_updated': datetime.now()}
        
        # Collecte des données de base
        basic_oids = [
            ('name', f"{SNMP_OIDS['if_name']}.{if_index}"),
            ('description', f"{SNMP_OIDS['if_descr']}.{if_index}"),
            ('admin_status', f"{SNMP_OIDS['if_admin_status']}.{if_index}"),
            ('oper_status', f"{SNMP_OIDS['if_oper_status']}.{if_index}"),
            ('speed', f"{SNMP_OIDS['if_speed']}.{if_index}"),
            ('high_speed', f"{SNMP_OIDS['if_high_speed']}.{if_index}"),
            ('alias', f"{SNMP_OIDS['if_alias']}.{if_index}"),
        ]
        
        for field, oid in basic_oids:
            value = self._get_single_oid(oid)
            if value is not None:
                if field in ['admin_status', 'oper_status']:
                    data[field] = STATUS_MAPPING.get(int(value), InterfaceStatus.UNKNOWN)
                elif field in ['speed', 'high_speed']:
                    data[field] = int(value)
                else:
                    data[field] = str(value)
        
        # Gestion de la vitesse (privilégier ifHighSpeed pour les interfaces rapides)
        if data.get('high_speed', 0) > 0:
            data['speed'] = data['high_speed'] * 1000000  # Conversion Mbps vers bps
        elif data.get('speed', 0) == 4294967295:  # Valeur max 32-bit, utiliser HC
            data['speed'] = data.get('high_speed', 0) * 1000000
        
        # Collecte des compteurs d'octets
        in_octets = self._get_single_oid(f"{SNMP_OIDS['if_hc_in_octets']}.{if_index}")
        if in_octets is None:
            in_octets = self._get_single_oid(f"{SNMP_OIDS['if_in_octets']}.{if_index}")
        
        out_octets = self._get_single_oid(f"{SNMP_OIDS['if_hc_out_octets']}.{if_index}")
        if out_octets is None:
            out_octets = self._get_single_oid(f"{SNMP_OIDS['if_out_octets']}.{if_index}")
        
        data['in_octets'] = int(in_octets) if in_octets is not None else 0
        data['out_octets'] = int(out_octets) if out_octets is not None else 0
        
        return data

    def collect_all_interfaces(self) -> List[Interface]:
        """Collecte les données de toutes les interfaces."""
        interfaces = []
        indices = self.collect_interface_indices()
        
        if not indices and not self.is_available():
            # Mode simulation pour développement hors-ligne
            return self._generate_simulated_interfaces()
        
        for if_index in indices:
            data = self.collect_interface_data(if_index)
            if data:
                try:
                    interface = Interface(
                        if_index=data['if_index'],
                        name=data.get('name', f'Interface{if_index}'),
                        description=data.get('description', data.get('alias', '')),
                        speed=data.get('speed', 0),
                        status=data.get('oper_status', InterfaceStatus.UNKNOWN),
                        admin_status=data.get('admin_status', InterfaceStatus.UNKNOWN),
                        in_octets=data.get('in_octets', 0),
                        out_octets=data.get('out_octets', 0),
                        last_updated=data.get('last_updated', datetime.now())
                    )
                    
                    # Calculer l'utilisation
                    utilization = interface.calculate_utilization()
                    interface.in_utilization = utilization['in']
                    interface.out_utilization = utilization['out']
                    
                    interfaces.append(interface)
                except Exception as e:
                    # Log l'erreur mais continue avec les autres interfaces
                    continue
        
        return interfaces

    def _generate_simulated_interface_data(self, if_index: int) -> Dict[str, Any]:
        """Génère des données simulées pour le mode hors-ligne."""
        import random
        
        interface_types = [
            ('GigabitEthernet', 1000000000),
            ('TenGigabitEthernet', 10000000000),
            ('FastEthernet', 100000000),
            ('Serial', 2048000)
        ]
        
        itype, speed = random.choice(interface_types)
        status = random.choice([InterfaceStatus.UP, InterfaceStatus.DOWN, InterfaceStatus.ADMIN_DOWN])
        
        return {
            'if_index': if_index,
            'name': f'{itype}0/{if_index}',
            'description': f'Interface {itype} {if_index}',
            'speed': speed,
            'oper_status': status,
            'admin_status': InterfaceStatus.UP,
            'in_octets': random.randint(1000000, 100000000),
            'out_octets': random.randint(1000000, 100000000),
            'last_updated': datetime.now()
        }

    def _generate_simulated_interfaces(self) -> List[Interface]:
        """Génère des interfaces simulées pour le développement."""
        interfaces = []
        for i in range(1, 13):  # 12 interfaces simulées
            data = self._generate_simulated_interface_data(i)
            interface = Interface(
                if_index=data['if_index'],
                name=data['name'],
                description=data['description'],
                speed=data['speed'],
                status=data['oper_status'],
                admin_status=data['admin_status'],
                in_octets=data['in_octets'],
                out_octets=data['out_octets'],
                last_updated=data['last_updated']
            )
            
            utilization = interface.calculate_utilization()
            interface.in_utilization = utilization['in']
            interface.out_utilization = utilization['out']
            
            interfaces.append(interface)
        
        return interfaces


def collect_interface_data(ip: str, community: str = "public", oid: str = None) -> Optional[Dict[str, Any]]:
    """Fonction legacy pour compatibilité."""
    collector = SNMPCollector(ip, community)
    if not collector.is_available():
        return None
    
    if oid:
        value = collector._get_single_oid(oid)
        return {oid: str(value)} if value is not None else None
    
    # Collecte les interfaces par défaut
    interfaces = collector.collect_all_interfaces()
    return {'interfaces': [
        {
            'if_index': iface.if_index,
            'name': iface.name,
            'description': iface.description,
            'status': iface.status.value,
            'utilization_in': iface.in_utilization,
            'utilization_out': iface.out_utilization
        }
        for iface in interfaces
    ]}


def calculate_interface_utilization(in_octets: int, out_octets: int, speed: int, interval: int = 300) -> Tuple[float, float]:
    """Calcule l'utilisation d'une interface en pourcentage.
    
    Args:
        in_octets: Octets entrants
        out_octets: Octets sortants  
        speed: Vitesse de l'interface en bps
        interval: Intervalle de mesure en secondes
    
    Returns:
        Tuple (utilisation_in, utilisation_out) en pourcentage
    """
    if speed == 0 or interval == 0:
        return 0.0, 0.0
    
    # Conversion octets vers bits puis calcul du pourcentage
    in_bps = (in_octets * 8) / interval
    out_bps = (out_octets * 8) / interval
    
    in_utilization = (in_bps / speed) * 100
    out_utilization = (out_bps / speed) * 100
    
    return (
        min(100.0, max(0.0, in_utilization)),
        min(100.0, max(0.0, out_utilization))
    )
