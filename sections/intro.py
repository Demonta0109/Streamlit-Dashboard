import streamlit as st

def show_intro():
    st.title("Context & Objectives")
    st.markdown("""
    #### The human body is sensitive to ionizing radiation. Excessive exposure can lead to occupational cataracts, particularly among workers in the medical (radiology, radiotherapy) or nuclear sectors.

    ### Dashboard objective  
    - The evolution of collective and average doses over time,  
    - Disparities between European countries,  
    - Differences between sectors (Medical, Nuclear, All monitored workers),  
    - The numbers of workers potentially at risk.  

    ### Data limitations
    - Some years are missing for certain countries,
    - Granularity by job type is not available, only by sector""")