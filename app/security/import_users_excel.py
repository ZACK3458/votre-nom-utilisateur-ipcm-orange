"""
Module d'import des utilisateurs depuis Excel (offline).
Permet d'ajouter des utilisateurs à partir d'un fichier Excel.
"""
# ATTENTION : Ce module nécessite pandas et une structure User compatible ORM.
# Pour IPCM offline, privilégier l'import manuel ou adapter User pour JSON.

import pandas as pd
from app.user_model import User
from app import db

def importer_utilisateurs_depuis_excel(fichier_excel):
    """Importe les utilisateurs depuis un fichier Excel et les ajoute à la base (offline ou ORM selon config).
    Args:
        fichier_excel (str): Chemin du fichier Excel à importer.
    """
    df = pd.read_excel(fichier_excel)
    for _, row in df.iterrows():
        user = User(
            username=row.get('Username', ''),
            password=row.get('Password', ''),
            role=row.get('Role', 'user')
        )
        db.session.add(user)
    db.session.commit()
    print('Importation des utilisateurs terminée.')
