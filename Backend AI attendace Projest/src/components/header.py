import streamlit as st


def header_home():

    logo_url = "https://i.ibb.co/ns8nJYrW/logo.png"
    

    
    st.markdown(f"""
           
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 0px; margin-top: 0px;">
            <img src='{logo_url}' style='height: 200px;'/>
            <h1 style='text-align:center; color: #E0E3FF; '>SAS</br> CLASS</h1>
        </div>
    """, unsafe_allow_html=True)


def header_dashboard():

    logo_url = "https://i.ibb.co/ns8nJYrW/logo.png"
    st.markdown(f"""
           
        <div style="display: flex;  align-items: center; justify-content: center; gap: 10px;">
            <img src='{logo_url}' style='height: 75px;'/>
            <h2 style='text-align:left; color: #5965F0; '>SAS</br> CLASS</h2>
        </div>
    """, unsafe_allow_html=True)