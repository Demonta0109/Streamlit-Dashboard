import pandas as pd
from datetime import datetime, timedelta
import numpy as np


def make_tables(df_raw):
    """
    Prepare raw dosimetry data for visualization.

    Parameters:
    -----------
    df_raw : pd.DataFrame
        Raw DataFrame containing dosimetry records

    Returns:
    --------
    dict : Dictionary with prepared tables
        - 'timeseries': Collective dose time series by year
        - 'by_region': Aggregated doses by country
        - 'by_sector': Aggregated doses by sector
        - 'by_country_year': Detailed country-year table
    """
    
    tables = {}
    
    # 1. Time series: collective dose aggregated by year
    timeseries = df_raw.groupby('year').agg({
        'collective_dose_total': 'sum',
        'total_workers_number': 'sum',
        'average_dose_monitored': 'mean'
    }).reset_index()
    timeseries = timeseries.sort_values('year')
    tables['timeseries'] = timeseries
    
    # 2. Aggregation by country
    by_country = df_raw.groupby('country').agg({
        'collective_dose_total': 'sum',
        'average_dose_monitored': 'mean',
        'average_dose_exposed': 'mean',
        'total_workers_number': 'sum'
    }).reset_index().sort_values('collective_dose_total', ascending=False)
    tables['by_region'] = by_country  # Renommé pour correspondre à app.py
    
    # 3. Aggregation by sector
    by_sector = df_raw[df_raw['sector'] != 'ALL MONITORED WORKERS'].groupby('sector').agg({
        'collective_dose_total': 'sum',
        'average_dose_monitored': 'mean',
        'total_workers_number': 'sum'
    }).reset_index().sort_values('collective_dose_total', ascending=False)
    tables['by_sector'] = by_sector
    
    # 4. Detailed country-year table for advanced visualizations
    by_country_year = df_raw[df_raw['sector'] == 'ALL MONITORED WORKERS'].groupby(['country', 'year']).agg({
        'collective_dose_total': 'sum',
        'average_dose_monitored': 'mean',
        'total_workers_number': 'sum'
    }).reset_index().sort_values(['country', 'year'])
    tables['by_country_year'] = by_country_year
    
    # 5. Geographic data: use centralised country coordinate mapping
    from utils.geo import get_coord

    geo_data = df_raw[df_raw['sector'] == 'ALL MONITORED WORKERS'].copy()
    geo_data[['latitude', 'longitude']] = geo_data['country'].apply(lambda c: pd.Series(get_coord(c)))
    geo_data = geo_data.rename(columns={'collective_dose_total': 'value'})
    # Keep rows even if coordinates are missing; consumers (viz.map_chart)
    # will drop entries without coords when rendering the map.
    tables['geo'] = geo_data[['country', 'year', 'latitude', 'longitude', 'value', 'average_dose_monitored']]
    return tables