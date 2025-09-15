"""
Module d'exportation des rapports de tendance d'utilisation
"""
import pandas as pd

def export_trend_report(data, filepath):
    df = pd.DataFrame(data)
    df.to_excel(filepath, index=False)
