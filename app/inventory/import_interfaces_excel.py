"""
Module d'import des interfaces réseau depuis Excel
"""
import pandas as pd
from app.inventory.interfaces import Interface
from app import db

def importer_interfaces_depuis_excel(fichier_excel):
    df = pd.read_excel(fichier_excel)
    for _, row in df.iterrows():
        interface = Interface(
            equipment_id=row.get('EquipmentID', None),
            name=row.get('InterfaceName', ''),
            ifIndex=row.get('ifIndex', None),
            description=row.get('Description', ''),
            speed=row.get('Speed', None),
            status=row.get('Status', ''),
            in_octets=row.get('InOctets', 0),
            out_octets=row.get('OutOctets', 0)
        )
        db.session.add(interface)
    db.session.commit()
    print('Importation des interfaces terminée.')
