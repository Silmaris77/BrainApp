import streamlit as st
from data.users import load_user_data

def init_session_state():
    """Inicjalizuje stan sesji z domyślnymi wartościami"""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if "username" not in st.session_state:
        st.session_state.username = None
        
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"    # Upewnij się, że strona jest poprawna
    valid_pages = ["dashboard", "degen_test", "neuroleader_test", "lesson", "profile", "neuroleader_explorer", "skills", "shop"]
    if st.session_state.page not in valid_pages:
        st.session_state.page = "dashboard"

def clear_session():
    """Clear all session state variables"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def get_user_data():
    """
    Pobiera dane użytkownika z pliku dla aktualnie zalogowanego użytkownika.
    
    Returns:
    - dict: Dane użytkownika lub pusty słownik jeśli użytkownik nie jest zalogowany
    """
    if not st.session_state.get('logged_in', False) or not st.session_state.get('username'):
        return {}
    
    users_data = load_user_data()
    return users_data.get(st.session_state.username, {})