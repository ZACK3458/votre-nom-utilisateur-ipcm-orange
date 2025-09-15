# Module de reporting et export Excel
import pandas as pd
from app.inventory.models import Equipment

def export_inventory_to_excel(filepath):
    equipments = Equipment.query.all()
    data = [{
        'Nom': eq.name,
        'Type': eq.type,
        'Marque': eq.brand,
        'Modèle': eq.model,
        'Version Logiciel': eq.software_version,
        'IP': eq.ip_address,
        'Localisation': eq.location,
        'Support': eq.support_status,
        'Modules': eq.modules
    } for eq in equipments]
    df = pd.DataFrame(data)
    df.to_excel(filepath, index=False)
    return filepath
