import streamlit as st
from data.users import register_user, login_user
from utils.components import zen_header, notification, zen_button, add_animations_css
from utils.material3_components import apply_material3_theme
from utils.css_loader import ensure_css_files, load_login_css
import os
import base64

# Funkcja do konwersji obrazu na Base64
def img_to_base64(img_path):
    try:
        if os.path.exists(img_path):
            with open(img_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        st.error(f"Błąd wczytywania logo: {str(e)}")
    return ""

def show_login_page():
    # Zastosuj Material 3 Theme
    apply_material3_theme()
    
    # Dodaj animacje CSS
    add_animations_css()
    
    # Upewnij się, że pliki CSS istnieją i załaduj je
    ensure_css_files()
    load_login_css()
    
    # Znajdź logo
    logo_path = os.path.join("assets", "images", "zen_degen_logo.png")
    
    # Podziel ekran na dwie kolumny o równej szerokości
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        # Dodaj odstęp na górze
        st.write("")
        st.write("")
        
        # Wyświetl logo
        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)
        else:
            st.markdown("# 🧘‍♂️💰")
        
        # Wycentrowane tytuł i hasło pod logo
        # st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>ZEN DEGEN ACADEMY</h1>", unsafe_allow_html=True)
        st.markdown("<p class='app-subtitle'>Balans i mądrość w świecie inwestycji</p>", unsafe_allow_html=True)
    
    with col2:
        # Tytuł formularza wycentrowany
        st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>Zaloguj się lub zarejestruj</h2>", unsafe_allow_html=True)
        
        # Zakładki Logowanie/Rejestracja
        login_tab, register_tab = st.tabs(["Logowanie", "Rejestracja"])
        
        # Zakładka logowania
        with login_tab:
            with st.form("login_form", clear_on_submit=False):
                username = st.text_input("Nazwa użytkownika")
                password = st.text_input("Hasło", type="password")
                submit_login = st.form_submit_button("Zaloguj się", use_container_width=True)
                
                if submit_login:
                    if login_user(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.page = 'dashboard'
                        st.rerun()
                    else:
                        st.error("Niepoprawna nazwa użytkownika lub hasło.")
        
        # Zakładka rejestracji
        with register_tab:
            with st.form("register_form", clear_on_submit=False):
                new_username = st.text_input("Nazwa użytkownika")
                new_password = st.text_input("Hasło", type="password")
                confirm_password = st.text_input("Potwierdź hasło", type="password")
                submit_register = st.form_submit_button("Zarejestruj się", use_container_width=True)
                
                if submit_register:
                    if not new_username or not new_password:
                        st.error("Nazwa użytkownika i hasło są wymagane.")
                    elif new_password != confirm_password:
                        st.error("Hasła nie pasują do siebie.")
                    else:
                        registration_successful = register_user(new_username, new_password, confirm_password)
                        
                        if registration_successful:
                            st.success("Rejestracja udana! Możesz się teraz zalogować.")
                            # Automatyczne logowanie po rejestracji
                            st.session_state.logged_in = True
                            st.session_state.username = new_username
                            st.session_state.page = 'dashboard'
                            st.rerun()
                        else:
                            st.error("Nazwa użytkownika jest już zajęta.")
