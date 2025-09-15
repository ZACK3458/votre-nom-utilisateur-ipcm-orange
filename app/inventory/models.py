"""Modèles d'inventaire hors-ligne (sans base de données).

Ce module fournit les dataclasses Equipment et Interface pour représenter
les équipements réseau et leurs interfaces selon les spécifications IPCM.
Aucune dépendance à SQLAlchemy ni à un objet `db`.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class EquipmentType(Enum):
    ROUTER = "routeur"
    SWITCH = "switch"
    FIREWALL = "firewall"
    LOAD_BALANCER = "load_balancer"
    SERVER = "server"
    OTHER = "other"


class NetworkDomain(Enum):
    LAN = "LAN"
    BACKBONE = "Backbone"
    DATACENTER = "Datacenter"
    FABRIC_IP = "Fabric IP"
    CORE_INTERNET = "Core Internet"


class SupportStatus(Enum):
    ACTIVE = "active"
    END_OF_SUPPORT_SW = "end_of_support_software"
    END_OF_SUPPORT_HW = "end_of_support_hardware"
    END_OF_SUPPORT_BOTH = "end_of_support_both"
    OBSOLETE = "obsolete"


class InterfaceStatus(Enum):
    UP = "up"
    DOWN = "down"
    ADMIN_DOWN = "admin_down"
    TESTING = "testing"
    UNKNOWN = "unknown"


@dataclass
class Interface:
    """Interface réseau avec données SNMP et utilisation."""
    if_index: int
    name: str = ""
    description: str = ""
    speed: int = 0  # vitesse nominale en bps
    status: InterfaceStatus = InterfaceStatus.UNKNOWN
    admin_status: InterfaceStatus = InterfaceStatus.UNKNOWN
    in_octets: int = 0
    out_octets: int = 0
    in_utilization: float = 0.0  # pourcentage d'utilisation entrante
    out_utilization: float = 0.0  # pourcentage d'utilisation sortante
    last_updated: Optional[datetime] = None
    equipment_id: Optional[int] = None
    
    def __post_init__(self):
        if isinstance(self.status, str):
            self.status = InterfaceStatus(self.status)
        if isinstance(self.admin_status, str):
            self.admin_status = InterfaceStatus(self.admin_status)
        if self.last_updated is None:
            self.last_updated = datetime.now()

    def calculate_utilization(self) -> Dict[str, float]:
        """Calcule l'utilisation en pourcentage basée sur les octets et la vitesse."""
        if self.speed == 0:
            return {"in": 0.0, "out": 0.0}
        
        # Conversion octets/seconde vers bits/seconde puis pourcentage
        in_util = (self.in_octets * 8 * 100) / self.speed if self.speed > 0 else 0.0
        out_util = (self.out_octets * 8 * 100) / self.speed if self.speed > 0 else 0.0
        
        return {
            "in": min(100.0, max(0.0, in_util)),
            "out": min(100.0, max(0.0, out_util))
        }


@dataclass
class Equipment:
    """Équipement réseau avec informations complètes selon spécifications IPCM."""
    id: Optional[int] = None
    name: str = ""
    type: EquipmentType = EquipmentType.OTHER
    brand: str = ""
    model: str = ""
    software_version: str = ""
    ip_address: str = ""
    location: str = ""
    domain: NetworkDomain = NetworkDomain.LAN
    support_status: SupportStatus = SupportStatus.ACTIVE
    modules: List[str] = field(default_factory=list)
    interfaces: List[Interface] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # Roadmap et lifecycle
    installation_date: Optional[datetime] = None
    end_of_life_date: Optional[datetime] = None
    replacement_planned: bool = False
    replacement_date: Optional[datetime] = None
    # Données SNMP
    snmp_community: str = "public"
    snmp_version: str = "2c"
    snmp_enabled: bool = True
    # Métadonnées additionnelles
    serial_number: str = ""
    asset_tag: str = ""
    vendor_support_contract: str = ""
    criticality_level: str = "medium"  # low, medium, high, critical
    notes: str = ""

    def __post_init__(self):
        if isinstance(self.type, str):
            self.type = EquipmentType(self.type)
        if isinstance(self.domain, str):
            self.domain = NetworkDomain(self.domain)
        if isinstance(self.support_status, str):
            self.support_status = SupportStatus(self.support_status)
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'équipement en dictionnaire pour la sérialisation JSON."""
        data = {
            'id': self.id,
            'name': self.name,
            'type': self.type.value,
            'brand': self.brand,
            'model': self.model,
            'software_version': self.software_version,
            'ip_address': self.ip_address,
            'location': self.location,
            'domain': self.domain.value,
            'support_status': self.support_status.value,
            'modules': self.modules,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'installation_date': self.installation_date.isoformat() if self.installation_date else None,
            'end_of_life_date': self.end_of_life_date.isoformat() if self.end_of_life_date else None,
            'replacement_planned': self.replacement_planned,
            'replacement_date': self.replacement_date.isoformat() if self.replacement_date else None,
            'snmp_community': self.snmp_community,
            'snmp_version': self.snmp_version,
            'snmp_enabled': self.snmp_enabled,
            'serial_number': self.serial_number,
            'asset_tag': self.asset_tag,
            'vendor_support_contract': self.vendor_support_contract,
            'criticality_level': self.criticality_level,
            'notes': self.notes,
            'interfaces': [
                {
                    'if_index': iface.if_index,
                    'name': iface.name,
                    'description': iface.description,
                    'speed': iface.speed,
                    'status': iface.status.value,
                    'admin_status': iface.admin_status.value,
                    'in_octets': iface.in_octets,
                    'out_octets': iface.out_octets,
                    'in_utilization': iface.in_utilization,
                    'out_utilization': iface.out_utilization,
                    'last_updated': iface.last_updated.isoformat() if iface.last_updated else None,
                    'equipment_id': iface.equipment_id
                }
                for iface in self.interfaces
            ]
        }
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Equipment':
        """Crée un équipement à partir d'un dictionnaire."""
        interfaces_data = data.pop('interfaces', [])
        
        # Conversion des dates
        for date_field in ['created_at', 'updated_at', 'installation_date', 'end_of_life_date', 'replacement_date']:
            if data.get(date_field):
                data[date_field] = datetime.fromisoformat(data[date_field])
        
        equipment = cls(**data)
        
        # Reconstruction des interfaces
        equipment.interfaces = []
        for iface_data in interfaces_data:
            if iface_data.get('last_updated'):
                iface_data['last_updated'] = datetime.fromisoformat(iface_data['last_updated'])
            interface = Interface(**iface_data)
            equipment.interfaces.append(interface)
        
        return equipment

    def get_active_interfaces(self) -> List[Interface]:
        """Retourne les interfaces actives."""
        return [iface for iface in self.interfaces if iface.status == InterfaceStatus.UP]

    def get_interface_by_name(self, name: str) -> Optional[Interface]:
        """Trouve une interface par son nom."""
        return next((iface for iface in self.interfaces if iface.name == name), None)

    def get_total_utilization(self) -> Dict[str, float]:
        """Calcule l'utilisation totale de l'équipement."""
        active_interfaces = self.get_active_interfaces()
        if not active_interfaces:
            return {"in": 0.0, "out": 0.0}
        
        total_in = sum(iface.in_utilization for iface in active_interfaces)
        total_out = sum(iface.out_utilization for iface in active_interfaces)
        
        return {
            "in": total_in / len(active_interfaces),
            "out": total_out / len(active_interfaces)
        }

    def __repr__(self) -> str:
        return f"<Equipment {self.name} ({self.type.value}) - {self.domain.value}>"
