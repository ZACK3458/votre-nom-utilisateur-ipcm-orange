"""
Module de consolidation d'inventaire et d'utilisation
"""
from app.inventory.models import Equipment
from app.inventory.interfaces import Interface

def consolidate_inventory():
    equipments = Equipment.query.all()
    interfaces = Interface.query.all()
    # Placeholder: logique de consolidation à compléter
    return equipments, interfaces
