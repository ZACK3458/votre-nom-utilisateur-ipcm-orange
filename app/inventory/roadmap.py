"""
Module de gestion de la roadmap équipements
"""
from app.inventory.models import Equipment
from app import db

def get_equipment_roadmap():
    # Placeholder: à compléter avec la logique de cycle de vie
    return Equipment.query.all()
