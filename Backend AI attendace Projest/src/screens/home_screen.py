import streamlit as st
from src.components.footer import footer_home
from src.components.header import header_home
from src.ui.base_layout import style_base_layout, style_background_home

def home_screen():
    


    header_home()
    style_background_home()
    style_base_layout()


    col1, col2 = st.columns(2, gap='large')

    with col1:
        st.header("I'm Student")
        st.image("https://i.ibb.co/23WY8pmc/Student-logo.png",width=145)
        if st.button('Student_Portal', type='primary', icon=':material/arrow_outward:'):
            st.session_state['login_type'] = 'student'
            st.rerun()
        

    with col2:
        st.header("I'm Teacher")
        st.image("https://i.ibb.co/Z6zmLD4s/Teacher-logo.png", width=140)
        if st.button('Teacher_Portal', type='primary', icon=':material/arrow_outward:'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    footer_home()
