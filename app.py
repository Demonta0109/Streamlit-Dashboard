import streamlit as st
import pandas as pd
from utils.io import load_data
from utils.prep import make_tables
from utils.viz import line_chart, bar_chart, map_chart
from sections.intro import intro_section
from sections.overview import overview_section

st.set_page_config(page_title="Data Storytelling Dashboard - Dosimetry", layout="wide")

@st.cache_data(show_spinner=False)
def get_data():
    df_raw = load_data()
    tables = make_tables(df_raw)
    return df_raw, tables

st.title(":bar_chart: Dosimetry - Radiation Exposure")
st.caption("Source: Exposition professionnelle aux rayonnements ionisants en Europe - DataGouv.fr - Licence Ouverte")

raw, tables = get_data()

# === OVERVIEW SECTION ===
overview_section()

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
    
    # Sector filter (allow an explicit 'All' option)
    sectors = ['All', 'ALL MONITORED WORKERS', 'MEDICAL FIELD', 'NUCLEAR FIELD', 'INTERVENTIONAL RADIOLOGY']
    selected_sector = st.selectbox(
        "Sector",
        sectors,
        index=0,
        help="Choose the sector to analyse (or 'All' to include every sector)"
    )
    
    st.markdown("---")
    st.markdown("### :pushpin: About")
    st.info("This dashboard visualises radiation exposure data for the eye lens across countries and sectors.")


# === APPLY FILTERS ===
mask = (
    (raw['country'].isin(selected_countries)) &
    (raw['year'] >= year_range[0]) &
    (raw['year'] <= year_range[1])
)
if selected_sector != 'All':
    mask &= (raw['sector'] == selected_sector)

filtered_data = raw[mask].copy()

# === KPI ROW ===
st.markdown("### :chart_with_upwards_trend: Key indicators")
c1, c2, c3 = st.columns(3)

with c1:
    total_dose = filtered_data['collective_dose_total'].sum()
    st.metric(
        ":syringe: Total collective dose",
        f"{total_dose:.3f} Sv",
        help="Sum of collective doses for monitored workers"
    )

with c2:
    avg_dose = filtered_data['average_dose_monitored'].mean()
    st.metric(
        ":warning: Average monitored dose",
        f"{avg_dose:.3f} Sv",
        help="Average dose among monitored workers"
    )

with c3:
    total_workers = filtered_data['total_workers_number'].sum()
    st.metric(
        ":busts_in_silhouette: Exposed workers",
        f"{int(total_workers):,}",
        help="Total number of monitored workers",
        delta=f"{((total_workers / raw['total_workers_number'].sum()) * 100):.1f}% of total"
    )

st.markdown("---")





# === VISUALISATIONS ===

# 1. Trends over time
st.subheader(":calendar: Dose time series")
# Use filtered_data directly (it already respects the 'All' selection)
timeseries_filtered = filtered_data.groupby('year').agg({
    'collective_dose_total': 'sum',
    'average_dose_monitored': 'mean',
    'total_workers_number': 'sum'
}).reset_index().sort_values('year')

if not timeseries_filtered.empty:
    line_chart(timeseries_filtered)
else:
    st.warning(":x: No data for the selected period")

st.markdown("---")

# 2. Compare regions (countries)
st.subheader(":globe_with_meridians: Comparison by country")
# Use filtered_data directly (it already respects the 'All' selection)
by_country_filtered = filtered_data.groupby('country').agg({
    'collective_dose_total': 'sum',
    'average_dose_monitored': 'mean',
    'average_dose_exposed': 'mean',
    'total_workers_number': 'sum'
}).reset_index().sort_values('collective_dose_total', ascending=False)

if not by_country_filtered.empty:
    bar_chart(by_country_filtered)
else:
    st.warning(":x: No data for the selected period")

st.markdown("---")

# 3. Map view
st.subheader(":world_map: Map view")
# Use filtered_data directly (it already respects the 'All' selection)
geo_filtered = filtered_data.copy()

if not geo_filtered.empty:
    map_chart(geo_filtered)
else:
    st.warning(":x: No data for the selected period")

st.markdown("---")

# === SECTIONS INFORMATIVES ===

st.markdown("### :microscope: Data quality & limitations")
st.info("""
- **Eye lens**: Sensitive organ to radiation
- **Equivalent dose**: Measured in Sieverts (Sv)
- **Monitored workers**: Occupationally exposed staff
- **Sectors**: Medical (radiology), Nuclear (facilities)
- **Missing data**: Marked by empty values (—)
""")

st.markdown("### :bulb: Key insights")
if not filtered_data.empty:
    insights = f"""
    - **Period analysed**: {year_range[0]} to {year_range[1]}
    - **Selected countries**: {', '.join(selected_countries)}
    - **Sector**: {selected_sector}
    - **Mean collective dose**: {filtered_data['collective_dose_total'].mean():.3f} Sv
    - **Number of workers**: {int(filtered_data['total_workers_number'].sum()):,}
    """
    st.success(insights)
else:
    st.warning(":warning: No data matching the selected filters")

st.markdown("---")
st.caption("Tableau de bord créé avec Streamlit | Données: Dosimétrie Cristallin Yeux")