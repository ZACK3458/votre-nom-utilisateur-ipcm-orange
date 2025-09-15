"""
Module de gestion des interfaces réseau
"""
from app import db

class Interface(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))
    name = db.Column(db.String(100))
    ifIndex = db.Column(db.Integer)
    description = db.Column(db.String(200))
    speed = db.Column(db.Integer)
    status = db.Column(db.String(50))
    in_octets = db.Column(db.BigInteger)
    out_octets = db.Column(db.BigInteger)

    def __repr__(self):
        return f'<Interface {self.name} ({self.status})>'
