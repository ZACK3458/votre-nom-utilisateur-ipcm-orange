"""
Module de visualisation et calcul d'utilisation des interfaces
"""
from app.inventory.interfaces import Interface
from app.snmp.collector import collect_interface_data

def calculate_utilization(interface):
    # Placeholder: à compléter avec la logique de calcul
    if interface.speed:
        utilization = ((interface.in_octets + interface.out_octets) / interface.speed) * 100
        return round(utilization, 2)
    return 0
