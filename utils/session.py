import streamlit as st

def init_session_state():
    """Inicjalizuje stan sesji z domyślnymi wartościami"""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if "username" not in st.session_state:
        st.session_state.username = None
        
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"
      # Upewnij się, że strona jest poprawna
    valid_pages = ["dashboard", "degen_test", "lesson", "profile", "degen_explorer", "skills", "shop"]
    if st.session_state.page not in valid_pages:
        st.session_state.page = "dashboard"

def clear_session():
    """Clear all session state variables"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]