import streamlit as st

def show_resume(filtered_data, year_range, selected_countries, selected_sector):

    if filtered_data.empty:
        st.warning(":x: No data available to analyze for this conclusion.")
        return

    avg_dose = filtered_data['collective_dose_total'].mean()
    total_workers = int(filtered_data['total_workers_number'].sum())

    st.subheader("Key Findings")
    st.success(f"""
    - Analysis period: **{year_range[0]} - {year_range[1]}**
    - Countries analyzed: **{', '.join(selected_countries)}**
    - Selected sector: **{selected_sector}**
    - Average collective dose: **{avg_dose:.3f} Sv**
    - Total number of monitored workers: **{total_workers:,}**
    """)

def show_conclusions():
    st.header("Conclusions & Recommendations")
    
    st.subheader("Overall interpretation")
    st.markdown("""
    A general trend of decrease/stability/increase is observed depending on the selected filters.  
    Some countries still show higher levels, which may indicate:  
    - Uneven radiation protection practices,  
    - Differences in activity volumes or monitoring systems,  
    - Possible sub-optimization of medical protocols.

    ### Potential recommendations for concerned countries:
    - Strengthen radiation protection training in the medical sector,
    - Harmonize standards across European countries,
    - More closely monitor areas with high collective dose.
    """)