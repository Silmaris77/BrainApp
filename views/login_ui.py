import streamlit as st
import hashlib
from data.users import load_user_data, save_user_data
from utils.ui import initialize_ui
from utils.ui.components.interactive import zen_button, notification

def show_login():
    """
    Wyświetla ekran logowania używając nowego systemu UI zgodnego z CSP
    """
    # Inicjalizacja UI
    initialize_ui()
    
    st.markdown("## Witaj w BrainApp!")
    st.markdown("Zaloguj się lub utwórz nowe konto, aby rozpocząć swoją przygodę.")
    
    