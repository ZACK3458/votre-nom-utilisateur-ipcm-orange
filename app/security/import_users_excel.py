"""
Module d'import des utilisateurs depuis Excel
"""
import pandas as pd
from app.user_model import User
from app import db

def importer_utilisateurs_depuis_excel(fichier_excel):
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
