import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go
import plotly.express as px


def line_chart(data):
    """
    Crée un graphique linéaire pour l'évolution temporelle de la dose collective.
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame avec colonnes 'year', 'collective_dose_total', 'average_dose_monitored'
    """
    if data.empty:
        st.warning("Aucune donnée disponible pour le graphique linéaire")
        return
    
    # Créer un graphique avec Altair
    chart = alt.Chart(data).mark_line(point=True, size=3).encode(
        x=alt.X('year:O', title='Année', axis=alt.Axis(format='d')),
        y=alt.Y('collective_dose_total:Q', title='Dose Collective Totale (Sv)'),
        tooltip=['year:O', 'collective_dose_total:Q', 'average_dose_monitored:Q']
    ).properties(
        width=800,
        height=400
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    
    # Afficher les statistiques
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Dose Collective Moyenne", f"{data['collective_dose_total'].mean():.3f} Sv")
    with col2:
        st.metric("Dose Monitée Moyenne", f"{data['average_dose_monitored'].mean():.3f} Sv")
    with col3:
        st.metric("Nombre d'années", len(data))


def bar_chart(data):
    """
    Crée un graphique en barres pour comparer les pays (régions).
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame avec colonnes 'country', 'collective_dose_total', 'average_dose_monitored'
    """
    if data.empty:
        st.warning("Aucune donnée disponible pour le graphique en barres")
        return
    
    # Renommer 'country' en 'region' pour cohérence
    if 'country' in data.columns:
        data = data.copy()
        data = data.rename(columns={'country': 'region'})
    
    # Créer un graphique avec Altair
    chart = alt.Chart(data).mark_bar(color='steelblue').encode(
        x=alt.X('region:N', title='Pays'),
        y=alt.Y('collective_dose_total:Q', title='Dose Collective Totale (Sv)'),
        tooltip=['region:N', 'collective_dose_total:Q', 'average_dose_monitored:Q', 'total_workers_number:Q']
    ).properties(
        width=800,
        height=400
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    
    # Afficher un tableau détaillé
    st.subheader("Détails par pays")
    display_data = data[['region', 'collective_dose_total', 'average_dose_monitored', 'total_workers_number']].copy()
    display_data.columns = ['Pays', 'Dose Collective (Sv)', 'Dose Moyenne Monitée (Sv)', 'Travailleurs']
    st.dataframe(display_data, use_container_width=True)


def map_chart(data):
    """
    Crée une carte interactive pour les données géographiques.
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame avec colonnes 'latitude', 'longitude', 'value', 'country', 'year'
    """
    if data.empty:
        st.warning("Aucune donnée disponible pour la carte")
        return
    
    # Préparer les données pour la carte
    if 'latitude' not in data.columns or 'longitude' not in data.columns:
        st.warning("Les colonnes 'latitude' et 'longitude' sont requises pour la carte")
        return
    
    # Utiliser Plotly pour une meilleure visualisation
    # Agréger les données par pays pour éviter les doublons
    map_data = data.groupby(['country', 'latitude', 'longitude']).agg({
        'value': 'mean',
        'average_dose_monitored': 'mean',
        'year': 'count'
    }).reset_index()
    map_data = map_data.rename(columns={'year': 'nb_records', 'value': 'dose_collective'})
    
    fig = px.scatter_geo(map_data,
        lat='latitude',
        lon='longitude',
        size='dose_collective',
        color='average_dose_monitored',
        hover_name='country',
        hover_data={
            'latitude': ':.2f',
            'longitude': ':.2f',
            'dose_collective': ':.3f',
            'average_dose_monitored': ':.3f'
        },
        title='Distribution Géographique des Doses de Radiation',
        size_max=50,
        projection='natural earth'
    )
    
    fig.update_layout(height=500, width=800)
    st.plotly_chart(fig, use_container_width=True)
    
    # Afficher les statistiques par pays
    st.subheader("Statistiques par Pays")
    stats = data.groupby('country').agg({
        'value': 'mean',
        'average_dose_monitored': 'mean',
        'total_workers_number': 'sum'
    }).reset_index()
    stats.columns = ['Pays', 'Dose Collective Moy. (Sv)', 'Dose Monitée Moy. (Sv)', 'Travailleurs Total']
    st.dataframe(stats, use_container_width=True)