import streamlit as st
import os
import sys

# Dodaj główny katalog do ścieżki
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

try:
    from utils.session import init_session_state, clear_session

    # Reset sesji
    clear_session()
    init_session_state()
    
    print("Pomyślnie zresetowano stan sesji")
    print("Nowe uruchomienie aplikacji będzie używać domyślnego układu modern_ui")
    print("\nAby uruchomić aplikację z nowym UI, użyj:")
    print("streamlit run main_ui.py")
    
except Exception as e:
    print(f"Błąd podczas resetowania sesji: {str(e)}")
    
if __name__ == "__main__":
    # Nic więcej do zrobienia - sam import zresetuje sesję
    pass
