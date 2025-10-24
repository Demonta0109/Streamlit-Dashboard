import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


def load_data():
    """
    Charge les données de dosimétrie depuis le fichier CSV.
    Le fichier utilise ';' comme séparateur (format CSV français).
    
    Returns:
    --------
    pd.DataFrame : DataFrame contenant les données brutes de dosimétrie
    """
    path = "data/cristallin_yeux.csv"
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Le fichier {path} n'existe pas. Assurez-vous que le fichier est présent.")
    
    # Charger le CSV avec ';' comme séparateur
    df = pd.read_csv(path, sep=';')
    
    # Nettoyer les noms de colonnes (enlever les espaces inutiles)
    df.columns = df.columns.str.strip()
    
    # Convertir les colonnes numériques en float (remplacer les ',' par '.')
    numeric_cols = df.select_dtypes(include=['object']).columns
    for col in numeric_cols:
        try:
            df[col] = df[col].astype(str).str.replace(',', '.').astype(float)
        except (ValueError, TypeError):
            pass  # Garder les colonnes non numériques
    
    # Convertir la colonne year en entier
    if 'year' in df.columns:
        df['year'] = df['year'].astype(int)
    
    return df