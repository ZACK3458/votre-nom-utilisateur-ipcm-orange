import pandas as pd
from app.inventory.models import Equipment
from app import db

def importer_equipements_depuis_excel(fichier_excel):
    df = pd.read_excel(fichier_excel)
    for _, row in df.iterrows():
        eq = Equipment(
            name=row.get('Nom', ''),
            type=row.get('Type', ''),
            brand=row.get('Marque', ''),
            model=row.get('Modèle', ''),
            software_version=row.get('Version Logiciel', ''),
            ip_address=row.get('IP', ''),
            location=row.get('Localisation', ''),
            support_status=row.get('Support', ''),
            modules=row.get('Modules', '')
        )
        db.session.add(eq)
    db.session.commit()
    print('Importation terminée.')

# Exemple d'utilisation :
# importer_equipements_depuis_excel(r'C:\orange\IP Capacity Management (2).xlsx')
