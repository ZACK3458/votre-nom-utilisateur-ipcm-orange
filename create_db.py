"""
Script de création de la base de données PostgreSQL IPCM
"""
from app import db
from app.inventory.models import Equipment
from app.inventory.interfaces import Interface
from app.security import User

def create_all_tables():
    db.create_all()
    print('Tables PostgreSQL créées avec succès.')

if __name__ == '__main__':
    create_all_tables()
