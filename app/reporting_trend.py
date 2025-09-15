"""
Module d'exportation des rapports de tendance d'utilisation (offline).
Permet d'exporter des données de tendance au format Excel ou CSV.
"""
import pandas as pd

def export_trend_report(data, filepath):
    """
    Exporte les données de tendance dans un fichier Excel (ou CSV selon extension).
    Args:
        data (list): Données à exporter (list of dict).
        filepath (str): Chemin du fichier de sortie.
    """
    df = pd.DataFrame(data)
    df.to_excel(filepath, index=False)
