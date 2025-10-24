import streamlit as st

def show_conclusions(filtered_data, year_range, selected_countries, selected_sector):
    st.header("✅ Conclusions & Recommandations")
    
    if filtered_data.empty:
        st.warning("Aucune donnée à analyser pour cette conclusion.")
        return

    avg_dose = filtered_data['collective_dose_total'].mean()
    total_workers = int(filtered_data['total_workers_number'].sum())

    st.subheader("📍 Principaux constats")
    st.success(f"""
    - Période analysée : **{year_range[0]} - {year_range[1]}**
    - Pays analysés : **{', '.join(selected_countries)}**
    - Secteur sélectionné : **{selected_sector}**
    - Dose collective moyenne : **{avg_dose:.3f} Sv**
    - Nombre total de travailleurs surveillés : **{total_workers:,}**
    """)

    st.subheader("📌 Interprétation globale")
    st.markdown("""
    ✅ On observe une tendance globale à la baisse/stabilité/hausse selon les filtres choisis.  
    ⚠️ Certains pays présentent encore des niveaux plus élevés, ce qui peut indiquer :  
    - Des pratiques de radioprotection inégales,  
    - Des différences de volume d’activité ou dispositifs de suivi,  
    - Une possible sous-optimisation des protocoles médicaux.

    ### 🚀 Recommandations potentielles
    - Renforcer la formation à la radioprotection dans le secteur médical,
    - Harmoniser les normes entre pays européens,
    - Surveiller plus étroitement les zones à forte dose collective.
    """)

    st.info("🔄 Pour approfondir, il serait intéressant d'ajouter une analyse par professions ou par modalité d’irradiation.")
