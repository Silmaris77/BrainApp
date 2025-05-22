import streamlit as st
import hashlib
import os
import base64
from data.users import load_user_data, save_user_data, register_user, login_user
from utils.ui import initialize_ui
from utils.ui.components.interactive import zen_button, notification
from utils.ui.components.text import zen_header

def img_to_base64(img_path):
    """Konwertuje obraz do formatu base64 dla wyświetlenia w HTML"""
    try:
        if os.path.exists(img_path):
            with open(img_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        st.error(f"Błąd wczytywania obrazu: {str(e)}")
    return ""

def show_login():
    """
    Wyświetla ekran logowania i obsługuje proces logowania/rejestracji
    """
    # Inicjalizacja UI
    initialize_ui()
    
    # Logo aplikacji
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "images", "logo.png")
    logo_base64 = img_to_base64(logo_path)
    
    if logo_base64:
        st.markdown(
            f"""
            <div class="logo-container">
                <img src="data:image/png;base64,{logo_base64}" alt="Logo" class="app-logo">
            </div>
            """,
            unsafe_allow_html=True
        )
    
    zen_header("BrainApp", "Aplikacja do rozwoju umiejętności przywódczych")
    
    # Wybór między logowaniem a rejestracją
    login_tab, register_tab = st.tabs(["Logowanie", "Rejestracja"])
    
    with login_tab:
        login_username = st.text_input("Nazwa użytkownika", key="login_username")
        login_password = st.text_input("Hasło", type="password", key="login_password")
        
        if zen_button("Zaloguj się", key="login_button"):
            if login_user(login_username, login_password):
                st.session_state.logged_in = True
                st.session_state.username = login_username
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                notification("Nieprawidłowa nazwa użytkownika lub hasło", type="error")
    
    with register_tab:
        register_username = st.text_input("Wybierz nazwę użytkownika", key="register_username")
        register_email = st.text_input("Email", key="register_email")
        register_password = st.text_input("Hasło", type="password", key="register_password")
        register_password2 = st.text_input("Powtórz hasło", type="password", key="register_password2")
        
        if zen_button("Zarejestruj się", key="register_button"):
            if not register_username or not register_password:
                notification("Proszę wypełnić wszystkie pola", type="warning")
            elif register_password != register_password2:
                notification("Hasła nie są identyczne", type="error")
            else:
                if register_user(register_username, register_password, register_email):
                    notification("Konto zostało utworzone! Możesz się teraz zalogować.", type="success")
                    # Automatyczne logowanie po rejestracji
                    st.session_state.logged_in = True
                    st.session_state.username = register_username
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    notification("Użytkownik o takiej nazwie już istnieje", type="error")

