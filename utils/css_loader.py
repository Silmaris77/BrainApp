import streamlit as st
import os

def ensure_css_files():
    """Upewnia się, że wszystkie wymagane katalogi i pliki CSS istnieją"""
    os.makedirs('assets/css', exist_ok=True)
    
    # Sprawdź i utwórz plik login.css jeśli nie istnieje
    if not os.path.exists('assets/css/login.css'):
        with open('assets/css/login.css', 'w') as f:
            f.write("""
/* Style dla strony logowania */

/* Style dla równych kolumn */
div[data-testid="column"] {
    width: 50% !important;
    flex: 1 1 0 !important;
    min-width: 0px !important;
}

/* Centrowanie tekstu w lewej kolumnie */
div[data-testid="column"]:first-child {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}

/* Style dla hasła pod logo */
.app-subtitle {
    font-size: 1.2rem;
    margin-top: 0;
    margin-bottom: 2rem;
    color: #555;
    font-style: italic;
    text-align: center;
    max-width: 80%;
}

/* Zapewnienie równej wysokości */
div.css-1r6slb0.e1tzin5v2 {
    min-height: 500px;
}

/* Style dla formularza w prawej kolumnie */
div[data-testid="column"]:nth-child(2) {
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.1);
}

/* Centrowanie przycisków formularza */
.stButton > button {
    display: block;
    margin: 0 auto;
}

/* Responsywność dla telefonów */
@media (max-width: 768px) {
    div[data-testid="column"] {
        width: 100% !important;
    }
}
""")

def load_login_css():
    """Ładuje style CSS dla strony logowania"""
    try:
        with open('assets/css/login.css', 'r') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Plik CSS dla logowania nie został znaleziony.")