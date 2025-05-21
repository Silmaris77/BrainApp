import streamlit as st
from views.admin import show_admin_dashboard

# Uruchom panel administratora bezpośrednio
st.session_state['username'] = 'admin'
st.session_state['logged_in'] = True
show_admin_dashboard()