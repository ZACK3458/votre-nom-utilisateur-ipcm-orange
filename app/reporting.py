"""
Module de reporting hors-ligne (sans base de données ni dépendances externes).

Fonctions :
- export_inventory_to_excel(filepath): Génère un fichier tabulaire minimal à l'emplacement donné.
  Utilise des données simulées pour garantir le mode offline.
  Le format écrit est CSV simple, compatible Excel.
"""

from datetime import datetime


NOM = 'Nom'
TYPE = 'Type'
MARQUE = 'Marque'
MODELE = 'Modèle'
VERSION_LOGICIEL = 'Version Logiciel'
IP = 'IP'
LOCALISATION = 'Localisation'
SUPPORT = 'Support'
MODULES = 'Modules'

SIMULATED_EQUIPMENTS = [
    {
        NOM: 'Router01',
        TYPE: 'Routeur',
        MARQUE: 'Cisco',
        MODELE: 'ASR1001-X',
        VERSION_LOGICIEL: '16.12',
        IP: '192.168.1.1',
        LOCALISATION: 'DC Yaoundé',
        SUPPORT: 'Actif',
        MODULES: 'SFP-10Gx2'
    },
    {
        NOM: 'Switch02',
        TYPE: 'Switch',
        MARQUE: 'Cisco',
        MODELE: 'C9300',
        VERSION_LOGICIEL: '17.9',
        IP: '192.168.1.2',
        LOCALISATION: 'DC Douala',
        SUPPORT: 'Actif',
        MODULES: 'STK-2'
    },
]


def export_inventory_to_excel(filepath: str) -> None:
    """
    Écrit un fichier CSV (séparateur virgule) avec l'inventaire simulé.

    Args:
        filepath (str): Chemin de sortie (extension libre; .xlsx accepté mais contenu CSV).
    """
    headers = [NOM, TYPE, MARQUE, MODELE, VERSION_LOGICIEL, IP, LOCALISATION, SUPPORT, MODULES]
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

