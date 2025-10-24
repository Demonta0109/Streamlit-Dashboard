import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go
import plotly.express as px


def line_chart(data):
    """Create a line chart showing the evolution of collective dose over time.

    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame with columns 'year', 'collective_dose_total', 'average_dose_monitored'
    """
    if data.empty:
        st.warning("No data available for the line chart")
        return
    
    # Créer un graphique avec Altair
    chart = alt.Chart(data).mark_line(point=True, size=3).encode(
    x=alt.X('year:O', title='Year', axis=alt.Axis(format='d')),
    y=alt.Y('collective_dose_total:Q', title='Total collective dose (Sv)'),
        tooltip=['year:O', 'collective_dose_total:Q', 'average_dose_monitored:Q']
    ).properties(
        width=800,
        height=400
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    
    # Afficher les statistiques
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Mean collective dose", f"{data['collective_dose_total'].mean():.3f} Sv")
    with col2:
        st.metric("Mean monitored dose", f"{data['average_dose_monitored'].mean():.3f} Sv")
    with col3:
        st.metric("Number of years", len(data))


def bar_chart(data):
    """Create a bar chart to compare countries.

    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame with columns 'country', 'collective_dose_total', 'average_dose_monitored'
    """
    if data.empty:
        st.warning("No data available for the bar chart")
        return
    
    # Renommer 'country' en 'region' pour cohérence
    if 'country' in data.columns:
        data = data.copy()
        data = data.rename(columns={'country': 'region'})
    
    # Créer un graphique avec Altair
    chart = alt.Chart(data).mark_bar(color='steelblue').encode(
        x=alt.X('region:N', title='Country'),
        y=alt.Y('collective_dose_total:Q', title='Total collective dose (Sv)'),
        tooltip=['region:N', 'collective_dose_total:Q', 'average_dose_monitored:Q', 'total_workers_number:Q']
    ).properties(
        width=800,
        height=400
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    
    # Afficher un tableau détaillé
    st.subheader("Details by country")
    display_data = data[['region', 'collective_dose_total', 'average_dose_monitored', 'total_workers_number']].copy()
    display_data.columns = ['Country', 'Collective Dose (Sv)', 'Mean monitored dose (Sv)', 'Workers']
    st.dataframe(display_data, use_container_width=True)


def map_chart(data):
    """Create an interactive map for geographic data.

    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame with columns 'country', 'year', 'collective_dose_total', 'average_dose_monitored'
    """
    if data.empty:
        st.warning("No data available for the map")
        return
    
    # Add GPS coordinates for each country
    country_coords = {
        'France': (46.2276, 2.2137),
        'Germany': (51.1657, 10.4515),
        'Greece': (39.0742, 21.8243),
        'Lithuania': (55.1694, 23.8813)
    }
    
    # Préparer les données
    map_data = data.copy()
    map_data['latitude'] = map_data['country'].map(lambda x: country_coords.get(x, (0, 0))[0])
    map_data['longitude'] = map_data['country'].map(lambda x: country_coords.get(x, (0, 0))[1])
    
    # Aggregate by country to avoid duplicates
    map_agg = map_data.groupby(['country', 'latitude', 'longitude']).agg({
        'collective_dose_total': 'sum',
        'average_dose_monitored': 'mean',
        'total_workers_number': 'sum'
    }).reset_index()

    map_agg['collective_dose_total'] = map_agg['collective_dose_total'].round(3)
    map_agg['average_dose_monitored'] = map_agg['average_dose_monitored'].round(3)

    # Vérifier qu'il y a des données avec coordonnées valides
    if (map_agg['latitude'] == 0).all() and (map_agg['longitude'] == 0).all():
        st.warning("No valid coordinates for the selected countries")
        return
    
    # --- Utiliser pydeck (deck.gl) pour une carte intégrée à Streamlit ---
    try:
        import pydeck as pdk
    except Exception:
        st.warning("pydeck is not available. Install pydeck to display the advanced map.")
        return

    # Préparer un code couleur RGB selon la dose moyenne (normalisation simple)
    min_avg = map_agg['average_dose_monitored'].min()
    max_avg = map_agg['average_dose_monitored'].max()
    range_avg = max_avg - min_avg if max_avg != min_avg else 1.0

    def avg_to_color(v):
        # Normaliser v entre 0 et 1
        norm = (v - min_avg) / range_avg
        # Gradient bleu -> orange
        r = int(255 * norm)
        g = int(120 * (1 - norm) + 60 * norm)
        b = int(200 * (1 - norm))
        return [r, g, b, 180]

    map_agg['color'] = map_agg['average_dose_monitored'].apply(lambda x: avg_to_color(x))

    # Calculer un rayon visuel (en mètres) proportionnel à la dose
    max_dose = map_agg['collective_dose_total'].max()
    if max_dose == 0 or np.isnan(max_dose):
        map_agg['radius'] = 10000
    else:
        # Échelle: 10k - 120k m
        map_agg['radius'] = map_agg['collective_dose_total'] / max_dose * 110000 + 10000

    # Centre initial de la carte
    center_lat = map_agg['latitude'].replace(0, np.nan).mean()
    center_lon = map_agg['longitude'].replace(0, np.nan).mean()
    if pd.isna(center_lat) or pd.isna(center_lon):
        center_lat, center_lon = 50.0, 10.0

    # Construire la layer ScatterplotLayer
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_agg,
        get_position="[longitude, latitude]",
        get_radius="radius",
        radius_scale=1,
        radius_min_pixels=4,
        get_fill_color="color",
        pickable=True,
        auto_highlight=True
    )

    tooltip = {
        "html": "<b>{country}</b><br/>Collective dose: {collective_dose_total} Sv<br/>Average dose: {average_dose_monitored} Sv<br/>Workers: {total_workers_number}",
        "style": {"backgroundColor": "steelblue", "color": "white"}
    }

    view_state = pdk.ViewState(latitude=center_lat, longitude=center_lon, zoom=4, pitch=0)

    deck = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)

    st.pydeck_chart(deck)

    # Display country statistics table
    st.subheader(":bar_chart: Country statistics")
    stats = map_agg[['country', 'collective_dose_total', 'average_dose_monitored', 'total_workers_number']].copy()
    stats.columns = ['Country', 'Collective Dose (Sv)', 'Mean monitored dose (Sv)', 'Workers']
    st.dataframe(stats.sort_values('Collective Dose (Sv)', ascending=False), use_container_width=True)