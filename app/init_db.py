"""
Module de configuration et initialisation de la base de données IPCM
"""
from app import db

def init_db():
    db.create_all()
