import pandas as pd
from datetime import datetime, timedelta
import numpy as np


def make_tables(df_raw):
    """
    Prépare les données brutes de dosimétrie pour la visualisation.
    
    Parameters:
    -----------
    df_raw : pd.DataFrame
        DataFrame brut contenant les données de dosimétrie
    
    Returns:
    --------
    dict : Dictionnaire contenant les tableaux préparés
        - 'timeseries': Évolution de la dose collective par année
        - 'by_region': Doses par pays
        - 'by_sector': Doses par secteur
        - 'by_country_year': Données détaillées par pays et année
    """
    
    tables = {}
    
    # 1. Série temporelle: évolution de la dose collective par année
    timeseries = df_raw.groupby('year').agg({
        'collective_dose_total': 'sum',
        'total_workers_number': 'sum',
        'average_dose_monitored': 'mean'
    }).reset_index()
    timeseries = timeseries.sort_values('year')
    tables['timeseries'] = timeseries
    
    # 2. Agrégation par pays (country)
    by_country = df_raw.groupby('country').agg({
        'collective_dose_total': 'sum',
        'average_dose_monitored': 'mean',
        'average_dose_exposed': 'mean',
        'total_workers_number': 'sum'
    }).reset_index().sort_values('collective_dose_total', ascending=False)
    tables['by_region'] = by_country  # Renommé pour correspondre à app.py
    
    # 3. Agrégation par secteur (sector)
    by_sector = df_raw[df_raw['sector'] != 'ALL MONITORED WORKERS'].groupby('sector').agg({
        'collective_dose_total': 'sum',
        'average_dose_monitored': 'mean',
        'total_workers_number': 'sum'
    }).reset_index().sort_values('collective_dose_total', ascending=False)
    tables['by_sector'] = by_sector
    
    # 4. Données détaillées par pays et année pour visualisations avancées
    by_country_year = df_raw[df_raw['sector'] == 'ALL MONITORED WORKERS'].groupby(['country', 'year']).agg({
        'collective_dose_total': 'sum',
        'average_dose_monitored': 'mean',
        'total_workers_number': 'sum'
    }).reset_index().sort_values(['country', 'year'])
    tables['by_country_year'] = by_country_year
    
    # 5. Données géographiques (approximation avec dummy coordinates pour carte)
    # Ajouter des coordonnées GPS approximatives pour chaque pays
    country_coords = {
        'France': (46.2276, 2.2137),
        'Germany': (51.1657, 10.4515),
        'Greece': (39.0742, 21.8243),
        'Lithuania': (55.1694, 23.8813)
    }
    
    geo_data = df_raw[df_raw['sector'] == 'ALL MONITORED WORKERS'].copy()
    geo_data['latitude'] = geo_data['country'].map(lambda x: country_coords.get(x, (0, 0))[0])
    geo_data['longitude'] = geo_data['country'].map(lambda x: country_coords.get(x, (0, 0))[1])
    geo_data = geo_data.rename(columns={'collective_dose_total': 'value'})
    tables['geo'] = geo_data[['country', 'year', 'latitude', 'longitude', 'value', 'average_dose_monitored']]
    return tables