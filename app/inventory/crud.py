# Fonctions CRUD pour l'inventaire
from app.inventory.models import Equipment
from app import db

def add_equipment(data):
    eq = Equipment(**data)
    db.session.add(eq)
    db.session.commit()
    return eq

def get_equipment(eq_id):
    return Equipment.query.get(eq_id)

def update_equipment(eq_id, data):
    eq = Equipment.query.get(eq_id)
    for key, value in data.items():
        setattr(eq, key, value)
    db.session.commit()
    return eq

def delete_equipment(eq_id):
    eq = Equipment.query.get(eq_id)
    db.session.delete(eq)
    db.session.commit()
