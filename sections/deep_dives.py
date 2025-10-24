import streamlit as st
from utils.viz import bar_chart, line_chart, map_chart

def show_deep_dives(filtered_data):
    st.header("In-depth analysis : Comparisons and disparities")
    
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

    st.markdown("#### As we can see above, the dose decreases over time, which is a positive trend indicating improved safety measures and reduced exposure levels for monitored workers globally.")
    st.markdown("#### But we can see that in `2018`, there is a slight increase in the average monitored dose")
    st.markdown("---")
    
    st.markdown("#### Now, let's explore how different countries compare in terms of radiation exposure for monitored workers.")
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

    st.markdown("#### The bar chart above highlights the disparities in average monitored doses across different countries. Some countries exhibit significantly higher exposure levels, indicating potential areas for improvement in radiation safety protocols.")
    st.markdown("#### As we can see, in `Hungary`, the average monitored dose is particularly high compared to other countries, meaning that workers in Hungary may be at a greater risk of radiation exposure.")


    st.markdown("---")

    st.markdown("#### Finally, let's visualize the geographic distribution of radiation exposure using an interactive map.")

    # 3. Map view
    st.subheader(":world_map: Map view")
    # Use filtered_data directly (it already respects the 'All' selection)
    geo_filtered = filtered_data.copy()

    if not geo_filtered.empty:
        map_chart(geo_filtered)
    else:
        st.warning(":x: No data for the selected period")

    st.markdown("---")
