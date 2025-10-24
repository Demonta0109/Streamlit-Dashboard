# Data Storytelling Dashboard — Dosimetry

This repository contains a Streamlit dashboard that visualises occupational radiation exposure datasets (eye-lens / full-body) across European countries and sectors.

The app was developed to load CSV files placed in the `data/` folder and provides:
- interactive filters (country, year range, sector)
- KPIs (total collective dose, mean monitored dose, number of workers)
- time-series line chart and country comparison bar chart (Altair)
- interactive map view (pydeck) with scatter points and a colour legend showing average monitored dose

Files of interest
- `app.py` - main Streamlit application
- `data/` - folder containing CSV dataset(s). The app prefers `corp_entier.csv` and falls back to `cristallin_yeux.csv`.
- `utils/io.py` - data loader and parser
- `utils/prep.py` - data preparation and aggregation
- `utils/viz.py` - plotting functions (line, bar, map)
- `utils/geo.py` - centralised country -> (lat, lon) mapping used by the map
- `sections/` - informational text sections for the dashboard

Quick start (PowerShell)

1. Install dependencies

```powershell
pip install -r requirements.txt
```

2. Run the Streamlit app

```powershell
streamlit run app.py
```

Notes & troubleshooting
- CSV format: the project expects semicolon-separated CSV files (";"), and `utils/io.py` will attempt to convert comma decimals ("0,123") into floats automatically.
- Map / pydeck: the map uses `pydeck`. If the map panel warns that `pydeck` is missing, install it with `pip install pydeck`.
- Country coordinates: `utils/geo.py` contains an approximate centroid mapping. If a country is missing on the map, add its name / centroid there or ask me to add fuzzy matching.