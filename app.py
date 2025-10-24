import streamlit as st
import pandas as pd
from utils.io import load_data
from utils.prep import make_tables
from utils.viz import line_chart, bar_chart, map_chart

st.set_page_config(page_title="Data Storytelling Dashboard - Dosimétrie", layout="wide")

@st.cache_data(show_spinner=False)
def get_data():
    df_raw = load_data()
    tables = make_tables(df_raw)
    return df_raw, tables

st.title("📊 Dosimétrie - Exposition à la Radiation")
st.caption("Source: Données d'exposition cristallin des yeux — Monitoring dosimétrique")

raw, tables = get_data()

# === SIDEBAR - FILTRES ===
with st.sidebar:
    st.header("🔧 Filtres")
    
    # Filtre par pays
    all_countries = raw['country'].unique().tolist()
    selected_countries = st.multiselect(
        "Pays",
        all_countries,
        default=all_countries,
        help="Sélectionnez les pays à afficher"
    )
    
    # Filtre par année
    min_year = raw['year'].min()
    max_year = raw['year'].max()
    year_range = st.slider(
        "Plage d'années",
        min_value=int(min_year),
        max_value=int(max_year),
        value=(int(min_year), int(max_year)),
        help="Sélectionnez la période à analyser"
    )
    
    # Filtre par secteur
    sectors = ['ALL MONITORED WORKERS', 'MEDICAL FIELD', 'NUCLEAR FIELD']
    selected_sector = st.selectbox(
        "Secteur",
        sectors,
        help="Choisir le secteur à analyser"
    )
    
    st.markdown("---")
    st.markdown("### 📌 À propos")
    st.info("Ce tableau de bord visualise les données d'exposition à la radiation pour le cristallin de l'oeil dans différents pays et secteurs.")

# === APPLICATION DES FILTRES ===
filtered_data = raw[
    (raw['country'].isin(selected_countries)) &
    (raw['year'] >= year_range[0]) &
    (raw['year'] <= year_range[1]) &
    (raw['sector'] == selected_sector)
].copy()

# === KPI ROW ===
st.markdown("### 📈 Indicateurs Clés")
c1, c2, c3 = st.columns(3)

with c1:
    total_dose = filtered_data['collective_dose_total'].sum()
    st.metric(
        "💉 Dose Collective Totale",
        f"{total_dose:.3f} Sv",
        delta=f"{((total_dose / raw['collective_dose_total'].sum()) * 100):.1f}% du total"
    )

with c2:
    avg_dose = filtered_data['average_dose_monitored'].mean()
    st.metric(
        "⚠️ Dose Moyenne Surveillée",
        f"{avg_dose:.3f} Sv",
        help="Moyenne des doses chez les travailleurs surveillés"
    )

with c3:
    total_workers = filtered_data['total_workers_number'].sum()
    st.metric(
        "👥 Travailleurs Exposés",
        f"{int(total_workers):,}",
        help="Nombre total de travailleurs surveillés"
    )

st.markdown("---")

# === VISUALISATIONS ===

# 1. Trends over time
st.subheader("📅 Évolution Temporelle de la Dose")
timeseries_filtered = filtered_data[filtered_data['sector'] == selected_sector].groupby('year').agg({
    'collective_dose_total': 'sum',
    'average_dose_monitored': 'mean',
    'total_workers_number': 'sum'
}).reset_index().sort_values('year')

if not timeseries_filtered.empty:
    line_chart(timeseries_filtered)
else:
    st.warning("❌ Aucune donnée pour la période sélectionnée")

st.markdown("---")

# 2. Compare regions (countries)
st.subheader("🌍 Comparaison par Pays")
by_country_filtered = filtered_data[filtered_data['sector'] == selected_sector].groupby('country').agg({
    'collective_dose_total': 'sum',
    'average_dose_monitored': 'mean',
    'average_dose_exposed': 'mean',
    'total_workers_number': 'sum'
}).reset_index().sort_values('collective_dose_total', ascending=False)

if not by_country_filtered.empty:
    bar_chart(by_country_filtered)
else:
    st.warning("❌ Aucune donnée pour la période sélectionnée")

st.markdown("---")

# 3. Map view
st.subheader("🗺️ Vue Cartographique")
geo_filtered = filtered_data[filtered_data['sector'] == selected_sector].copy()

if not geo_filtered.empty:
    map_chart(geo_filtered)
else:
    st.warning("❌ Aucune donnée pour la période sélectionnée")

st.markdown("---")

# === SECTIONS INFORMATIVES ===

st.markdown("### 🔬 Qualité des Données & Limitations")
st.info("""
- **Cristallin de l'oeil**: Organe sensible aux radiations
- **Dose équivalente**: Mesurée en Sieverts (Sv)
- **Travailleurs surveillés**: Personnel professionnel exposé à des radiations
- **Secteurs**: Médical (radiologie), Nucléaire (installations)
- **Données manquantes**: Marquées par des valeurs vides (—)
""")

st.markdown("### 💡 Principaux Enseignements")
if not filtered_data.empty:
    insights = f"""
    - **Période analysée**: {year_range[0]} à {year_range[1]}
    - **Pays sélectionnés**: {', '.join(selected_countries)}
    - **Secteur**: {selected_sector}
    - **Dose collective moyenne**: {filtered_data['collective_dose_total'].mean():.3f} Sv
    - **Nombre de travailleurs**: {int(filtered_data['total_workers_number'].sum()):,}
    """
    st.success(insights)
else:
    st.warning("Aucune donnée correspondant aux critères sélectionnés")

st.markdown("---")
st.caption("Tableau de bord créé avec Streamlit | Données: Dosimétrie Cristallin Yeux")