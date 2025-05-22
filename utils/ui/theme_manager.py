import streamlit as st
import os

def load_theme(theme_name):
    """Ładuje wybrany motyw CSS."""
    theme_path = os.path.join("static", "css", "themes", f"{theme_name}.css")
    
    if not os.path.exists(theme_path):
        st.warning(f"Plik motywu {theme_path} nie istnieje.")
        return
    
    with open(theme_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_current_theme():
    """Zwraca aktualnie wybrany motyw."""
    return st.session_state.get("current_theme", "modern_ui")

def set_theme(theme_name):
    """Ustawia wybrany motyw."""
    st.session_state.current_theme = theme_name
    return load_theme(theme_name)

def theme_selector():
    """Komponent do wyboru motywu."""
    theme = st.sidebar.selectbox(
        "Wybierz layout aplikacji:",
        ["modern_ui", "card_layout"],
        index=0 if get_current_theme() == "modern_ui" else 1
    )
    
    if theme != get_current_theme():
        set_theme(theme)
        st.rerun()
