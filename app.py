import streamlit as st
import pandas as pd
from utils.io import load_data
from utils.prep import make_tables
from utils.viz import line_chart, bar_chart, map_chart
from sections.intro import show_intro
from sections.overview import show_overview
from sections.deep_dives import show_deep_dives
from sections.conclusions import show_resume, show_conclusions


st.set_page_config(page_title="Data Storytelling Dashboard - Dosimetry", layout="wide")

@st.cache_data(show_spinner=False)
def get_data():
    df_raw = load_data()
    tables = make_tables(df_raw)
    return df_raw, tables

st.title(":bar_chart: Dosimetry - Radiation Exposure")
st.caption("Source: Exposition professionnelle aux rayonnements ionisants en Europe - DataGouv.fr - Licence Ouverte")

raw, tables = get_data()

# === SIDEBAR - FILTERS ===
with st.sidebar:
    st.header(":gear: Filters")
    
    # Country filter
    all_countries = raw['country'].unique().tolist()
    selected_countries = st.multiselect(
        "Country",
        all_countries,
        default=all_countries,
        help="Select countries to display"
    )
    
    # Year range filter
    min_year = raw['year'].min()
    max_year = raw['year'].max()
    year_range = st.slider(
        "Year range",
        min_value=int(min_year),
        max_value=int(max_year),
        value=(int(min_year), int(max_year)),
        help="Select the period to analyse"
    )
    
    # Sector filter (dynamic list, keep 'All' as first option)
    sectors_from_data = raw['sector'].dropna().unique().tolist()
    # Preferred order defined by the user; any other sectors from data will be appended
    preferred_order = [
        'ALL MONITORED WORKERS', 'MEDICAL FIELD', 'INDUSTRY', 'NUCLEAR FIELD',
        'RESEARCH AND EDUCATION', 'NATURAL SOURCES', 'TRANSPORT', 'OTHER FIELDS'
    ]
    ordered = [s for s in preferred_order if s in sectors_from_data]
    others = [s for s in sectors_from_data if s not in preferred_order]
    sectors = ['All'] + ordered + sorted(others)

    selected_sector = st.selectbox(
        "Sector",
        sectors,
        index=0,
        help="Choose the sector to analyse (or 'All' to include every sector)"
    )
    
    st.markdown("---")
    st.markdown("### :pushpin: About")
    st.info("This data set has **3082** rows and 7 columns, covering dosimetry records from various countries and sectors over multiple years.")

# === APPLY FILTERS ===
mask = (
    (raw['country'].isin(selected_countries)) &
    (raw['year'] >= year_range[0]) &
    (raw['year'] <= year_range[1])
)
if selected_sector != 'All':
    mask &= (raw['sector'] == selected_sector)

filtered_data = raw[mask].copy()

# === INTRO SECTION ===
show_intro()

# === OVERVIEW SECTION ===
show_overview(filtered_data, raw)

# === DEEP DIVE SECTION ===
show_deep_dives(filtered_data)

# === CONCLUSIONS SECTION ===
show_resume(filtered_data, year_range, selected_countries, selected_sector)
show_conclusions()