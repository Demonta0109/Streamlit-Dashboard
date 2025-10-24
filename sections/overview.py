import streamlit as st
import pandas as pd

def show_overview(filtered_data, raw):
    # === KPI ROW ===
    st.header(":chart_with_upwards_trend: Key indicators")
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
