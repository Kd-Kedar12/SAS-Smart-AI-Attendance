import streamlit as st


def footer_home():
    logo_url = "https://i.ibb.co/ns8nJYrW/logo.png"
    
    st.markdown(f"""
           
        <div style="margin-top: 2rem; display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <p style="font-weight: bold !important; color: white;">Created with ❤️ by KD</p>
        </div>


            """, unsafe_allow_html=True)


def footer_dashboard():
    logo_url = "https://i.ibb.co/ns8nJYrW/logo.png"
    
    st.markdown(f"""
           
        <div style="margin-top: 2rem; display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <p style="font-weight: bold !important; color: black;">Created with ❤️ by KD</p>
        
        </div>


            """, unsafe_allow_html=True)        