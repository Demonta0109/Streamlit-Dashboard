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
    path = "data/cristallin_yeux.csv"
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} does not exist. Please ensure the file is present.")

    # Read CSV using ';' as separator
    df = pd.read_csv(path, sep=';')

    # Clean column names (strip whitespace)
    df.columns = df.columns.str.strip()

    # Convert object columns that look numeric into floats (replace ',' with '.')
    numeric_cols = df.select_dtypes(include=['object']).columns
    for col in numeric_cols:
        try:
            df[col] = df[col].astype(str).str.replace(',', '.').astype(float)
        except (ValueError, TypeError):
            pass  # keep non-numeric columns as-is

    # Convert 'year' column to integer
    if 'year' in df.columns:
        df['year'] = df['year'].astype(int)

    return df