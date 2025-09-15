"""
Module de reporting hors-ligne (sans base de données ni dépendances externes).

export_inventory_to_excel(filepath):
- Génère un fichier tabulaire minimal à l'emplacement donné.
- Utilise des données simulées afin d'être 100% offline-first.
- Le format écrit est CSV simple, indépendamment de l'extension fournie.
  Cela suffit pour les tests unitaires et peut être ouvert par Excel.
"""

from datetime import datetime


SIMULATED_EQUIPMENTS = [
    {
        'Nom': 'Router01',
        'Type': 'Routeur',
        'Marque': 'Cisco',
        'Modèle': 'ASR1001-X',
        'Version Logiciel': '16.12',
        'IP': '192.168.1.1',
        'Localisation': 'DC Yaoundé',
        'Support': 'Actif',
        'Modules': 'SFP-10Gx2'
    },
    {
        'Nom': 'Switch02',
        'Type': 'Switch',
        'Marque': 'Cisco',
        'Modèle': 'C9300',
        'Version Logiciel': '17.9',
        'IP': '192.168.1.2',
        'Localisation': 'DC Douala',
        'Support': 'Actif',
        'Modules': 'STK-2'
    },
]


def export_inventory_to_excel(filepath: str) -> None:
    """Écrit un fichier CSV (séparateur virgule) avec l'inventaire simulé.

    Paramètres:
        filepath: Chemin de sortie (extension libre; .xlsx accepté mais contenu CSV).
    """
    headers = ['Nom', 'Type', 'Marque', 'Modèle', 'Version Logiciel', 'IP', 'Localisation', 'Support', 'Modules']
    def to_csv_cell(text: str) -> str:
        t = str(text) if text is not None else ''
        return '"' + t.replace('"', '""') + '"'

    lines = []
    # En-tête et métadonnées légères en commentaire (compatibles avec de nombreux lecteurs CSV)
    lines.append(f"# IPCM Export Inventaire - {datetime.now().isoformat(timespec='seconds')}")
    lines.append(','.join(headers))
    for row in SIMULATED_EQUIPMENTS:
        cells = [to_csv_cell(row.get(h, '')) for h in headers]
        lines.append(','.join(cells))

    # Écriture fichier (texte) quel que soit l'extension fournie.
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(lines))

