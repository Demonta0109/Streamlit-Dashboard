import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


def load_data():
    """
    Load dosimetry data from the CSV file.
    The file uses ';' as separator (French CSV format).

    Returns:
    --------
    pd.DataFrame : DataFrame containing the raw dosimetry data
    """
    path = "data/corp_entier.csv"
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} does not exist. Please ensure the file is present.")

    # Read CSV using ';' as separator
    df = pd.read_csv(path, sep=';')

    # Clean column names
    df.columns = df.columns.str.strip()

    # Convert object columns that look numeric into floats (replace ',' with '.')
    # We attempt conversion but leave the column untouched if it fails
    obj_cols = df.select_dtypes(include=['object']).columns
    for col in obj_cols:
        # Skip obviously non-numeric text columns such as 'country' or 'sector'
        if col.lower() in ("country", "sector", "subsector", "label"):
            continue
        cleaned = df[col].astype(str).str.replace(',', '.').str.strip()
        # A simple heuristic: if >50% of values look numeric after cleaning, convert
        num_like = cleaned.str.match(r"^-?\d+(?:\.\d+)?$")
        if num_like.mean() >= 0.5:
            try:
                df[col] = pd.to_numeric(cleaned, errors='coerce')
            except Exception:
                pass

    # Convert 'year' column to integer
    if 'year' in df.columns:
        # coerce first in case year column contains floats or stray strings
        df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
        # convert to plain int where possible (Streamlit UI expects ints for sliders)
        if df['year'].notna().all():
            df['year'] = df['year'].astype(int)

    return df