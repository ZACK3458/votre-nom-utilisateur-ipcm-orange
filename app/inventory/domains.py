"""Gestion des domaines réseau selon les spécifications IPCM.

Ce module gère la répartition des équipements par domaines réseau :
- LAN (Local Area Network)
- Backbone
- Datacenter  
- Fabric IP
- Cœur Internet

Chaque domaine a ses propres KPI et seuils d'alerte.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

from .models import Equipment, NetworkDomain, EquipmentType
from .store import get_equipments_by_domain, load_equipment_objects


@dataclass
class DomainMetrics:
    """Métriques d'un domaine réseau."""
    domain: NetworkDomain
    total_equipments: int = 0
    active_equipments: int = 0
    critical_equipments: int = 0
    total_interfaces: int = 0
    active_interfaces: int = 0
    average_utilization_in: float = 0.0
    average_utilization_out: float = 0.0
    peak_utilization: float = 0.0
    equipments_by_type: Dict[str, int] = None
    support_status_distribution: Dict[str, int] = None

    def __post_init__(self):
        if self.equipments_by_type is None:
            self.equipments_by_type = {}
        if self.support_status_distribution is None:
            self.support_status_distribution = {}


@dataclass 
class DomainThresholds:
    """Seuils d'alerte par domaine."""
    domain: NetworkDomain
    utilization_warning: float = 70.0  # Seuil d'avertissement utilisation
    utilization_critical: float = 85.0  # Seuil critique utilisation
    interface_down_warning: int = 1  # Nombre d'interfaces down avant alerte
    interface_down_critical: int = 3  # Nombre d'interfaces down critique
    equipment_down_warning: int = 1  # Nombre d'équipements down avant alerte
    equipment_down_critical: int = 2  # Nombre d'équipements down critique


# Configuration des seuils par domaine
DOMAIN_THRESHOLDS = {
    NetworkDomain.CORE_INTERNET: DomainThresholds(
        domain=NetworkDomain.CORE_INTERNET,
        utilization_warning=60.0,
        utilization_critical=75.0,
        interface_down_warning=1,
        interface_down_critical=1,
        equipment_down_warning=1,
        equipment_down_critical=1
    ),
    NetworkDomain.BACKBONE: DomainThresholds(
        domain=NetworkDomain.BACKBONE,
        utilization_warning=65.0,
        utilization_critical=80.0,
        interface_down_warning=1,
        interface_down_critical=2,
        equipment_down_warning=1,
        equipment_down_critical=1
    ),
    NetworkDomain.DATACENTER: DomainThresholds(
        domain=NetworkDomain.DATACENTER,
        utilization_warning=75.0,
        utilization_critical=90.0,
        interface_down_warning=2,
        interface_down_critical=5,
        equipment_down_warning=1,
        equipment_down_critical=3
    ),
    NetworkDomain.FABRIC_IP: DomainThresholds(
        domain=NetworkDomain.FABRIC_IP,
        utilization_warning=70.0,
        utilization_critical=85.0,
        interface_down_warning=2,
        interface_down_critical=4,
        equipment_down_warning=1,
        equipment_down_critical=2
    ),
    NetworkDomain.LAN: DomainThresholds(
        domain=NetworkDomain.LAN,
        utilization_warning=80.0,
        utilization_critical=95.0,
        interface_down_warning=3,
        interface_down_critical=10,
        equipment_down_warning=2,
        equipment_down_critical=5
    )
}


class DomainManager:
    """Gestionnaire des domaines réseau."""
    
    def __init__(self):
        self.thresholds = DOMAIN_THRESHOLDS

    def get_domain_metrics(self, domain: NetworkDomain) -> DomainMetrics:
        """Calcule les métriques d'un domaine."""
        equipments = get_equipments_by_domain(domain)
        metrics = DomainMetrics(domain=domain)
        
        if not equipments:
            return metrics
        
        # Statistiques de base
        metrics.total_equipments = len(equipments)
        metrics.active_equipments = len([eq for eq in equipments 
                                       if eq.support_status.value != 'obsolete'])
        metrics.critical_equipments = len([eq for eq in equipments 
                                         if eq.criticality_level == 'critical'])
        
        # Statistiques des interfaces
        all_interfaces = []
        for eq in equipments:
            all_interfaces.extend(eq.interfaces)
        
        metrics.total_interfaces = len(all_interfaces)
        metrics.active_interfaces = len([iface for iface in all_interfaces 
                                       if iface.status.value == 'up'])
        
        # Calcul des utilisations moyennes
        if all_interfaces:
            metrics.average_utilization_in = sum(iface.in_utilization for iface in all_interfaces) / len(all_interfaces)
            metrics.average_utilization_out = sum(iface.out_utilization for iface in all_interfaces) / len(all_interfaces)
            metrics.peak_utilization = max(
                max(iface.in_utilization for iface in all_interfaces),
                max(iface.out_utilization for iface in all_interfaces)
            )
        
        # Distribution par type d'équipement
        metrics.equipments_by_type = {}
        for eq in equipments:
            eq_type = eq.type.value
            metrics.equipments_by_type[eq_type] = metrics.equipments_by_type.get(eq_type, 0) + 1
        
        # Distribution par statut de support
        metrics.support_status_distribution = {}
        for eq in equipments:
            status = eq.support_status.value
            metrics.support_status_distribution[status] = metrics.support_status_distribution.get(status, 0) + 1
        
        return metrics

    def get_all_domains_metrics(self) -> Dict[NetworkDomain, DomainMetrics]:
        """Récupère les métriques de tous les domaines."""
        metrics = {}
        for domain in NetworkDomain:
            metrics[domain] = self.get_domain_metrics(domain)
        return metrics

    def check_domain_alerts(self, domain: NetworkDomain) -> List[Dict[str, Any]]:
        """Vérifie les alertes pour un domaine."""
        alerts = []
        metrics = self.get_domain_metrics(domain)
        thresholds = self.thresholds.get(domain)
        
        if not thresholds:
            return alerts
        
        # Alerte utilisation critique
        if metrics.peak_utilization >= thresholds.utilization_critical:
            alerts.append({
                'type': 'critical',
                'domain': domain.value,
                'message': f'Utilisation critique dans {domain.value}: {metrics.peak_utilization:.1f}%',
                'value': metrics.peak_utilization,
                'threshold': thresholds.utilization_critical,
                'category': 'utilization'
            })
        elif metrics.peak_utilization >= thresholds.utilization_warning:
            alerts.append({
                'type': 'warning',
                'domain': domain.value,
                'message': f'Utilisation élevée dans {domain.value}: {metrics.peak_utilization:.1f}%',
                'value': metrics.peak_utilization,
                'threshold': thresholds.utilization_warning,
                'category': 'utilization'
            })
        
        # Alerte interfaces down
        interfaces_down = metrics.total_interfaces - metrics.active_interfaces
        if interfaces_down >= thresholds.interface_down_critical:
            alerts.append({
                'type': 'critical',
                'domain': domain.value,
                'message': f'{interfaces_down} interfaces down dans {domain.value}',
                'value': interfaces_down,
                'threshold': thresholds.interface_down_critical,
                'category': 'interfaces'
            })
        elif interfaces_down >= thresholds.interface_down_warning:
            alerts.append({
                'type': 'warning',
                'domain': domain.value,
                'message': f'{interfaces_down} interfaces down dans {domain.value}',
                'value': interfaces_down,
                'threshold': thresholds.interface_down_warning,
                'category': 'interfaces'
            })
        
        return alerts

    def get_critical_interfaces_by_domain(self, domain: NetworkDomain, threshold: float = 85.0) -> List[Dict[str, Any]]:
        """Récupère les interfaces critiques d'un domaine."""
        equipments = get_equipments_by_domain(domain)
        critical_interfaces = []
        
        for eq in equipments:
            for iface in eq.interfaces:
                if (iface.in_utilization >= threshold or iface.out_utilization >= threshold):
                    critical_interfaces.append({
                        'equipment_name': eq.name,
                        'equipment_ip': eq.ip_address,
                        'interface_name': iface.name,
                        'interface_description': iface.description,
                        'utilization_in': iface.in_utilization,
                        'utilization_out': iface.out_utilization,
                        'status': iface.status.value,
                        'speed': iface.speed
                    })
        
        return sorted(critical_interfaces, 
                     key=lambda x: max(x['utilization_in'], x['utilization_out']), 
                     reverse=True)

    def get_domain_summary(self) -> Dict[str, Any]:
        """Résumé global de tous les domaines."""
        all_metrics = self.get_all_domains_metrics()
        all_alerts = []
        
        for domain in NetworkDomain:
            all_alerts.extend(self.check_domain_alerts(domain))
        
        summary = {
            'total_equipments': sum(m.total_equipments for m in all_metrics.values()),
            'total_interfaces': sum(m.total_interfaces for m in all_metrics.values()),
            'active_interfaces': sum(m.active_interfaces for m in all_metrics.values()),
            'critical_alerts': len([a for a in all_alerts if a['type'] == 'critical']),
            'warning_alerts': len([a for a in all_alerts if a['type'] == 'warning']),
            'domains': {
                domain.value: {
                    'equipments': metrics.total_equipments,
                    'interfaces': metrics.total_interfaces,
                    'active_interfaces': metrics.active_interfaces,
                    'utilization': metrics.peak_utilization,
                    'alerts': len(self.check_domain_alerts(domain))
                }
                for domain, metrics in all_metrics.items()
            },
            'alerts': all_alerts
        }
        
        return summary

    def get_equipment_distribution(self) -> Dict[str, Dict[str, int]]:
        """Distribution des équipements par domaine et type."""
        distribution = {}
        
        for domain in NetworkDomain:
            metrics = self.get_domain_metrics(domain)
            distribution[domain.value] = metrics.equipments_by_type
        
        return distribution

    def recommend_capacity_actions(self, domain: NetworkDomain) -> List[Dict[str, Any]]:
        """Recommandations d'actions basées sur l'analyse de capacité."""
        recommendations = []
        metrics = self.get_domain_metrics(domain)
        thresholds = self.thresholds.get(domain)
        
        if not thresholds:
            return recommendations
        
        # Recommandations basées sur l'utilisation
        if metrics.peak_utilization >= thresholds.utilization_critical:
            recommendations.append({
                'priority': 'high',
                'action': 'capacity_upgrade',
                'description': f'Augmentation de capacité urgente requise dans {domain.value}',
                'details': f'Utilisation pic: {metrics.peak_utilization:.1f}%'
            })
        elif metrics.peak_utilization >= thresholds.utilization_warning:
            recommendations.append({
                'priority': 'medium',
                'action': 'capacity_planning',
                'description': f'Planification d\'augmentation de capacité pour {domain.value}',
                'details': f'Utilisation pic: {metrics.peak_utilization:.1f}%'
            })
        
        # Recommandations basées sur les équipements obsolètes
        obsolete_count = metrics.support_status_distribution.get('obsolete', 0) + \
                        metrics.support_status_distribution.get('end_of_support_both', 0)
        
        if obsolete_count > 0:
            recommendations.append({
                'priority': 'medium',
                'action': 'equipment_replacement',
                'description': f'Remplacement de {obsolete_count} équipements obsolètes dans {domain.value}',
                'details': 'Équipements en fin de support détectés'
            })
        
        return recommendations


# Instance globale du gestionnaire de domaines
domain_manager = DomainManager()


# Fonction legacy pour compatibilité
def organize_by_domain():
    """Organisation legacy par domaine (maintenue pour compatibilité)."""
    summary = domain_manager.get_domain_summary()
    return {
        domain: summary['domains'].get(domain, {})
        for domain in ['LAN', 'Backbone', 'Datacenter', 'Fabric IP', 'Core Internet']
    }
