# This script will create properly formatted versions of main.py and shop.py

import os

# Define the content for main.py
main_py_content = '''import streamlit as st
import os
import sys
import traceback
from config.settings import PAGE_CONFIG

# Ta funkcja musi być wywołana jako pierwsza funkcja Streamlit
st.set_page_config(**PAGE_CONFIG)

# Ścieżka do głównego katalogu aplikacji (dla importów)
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

# Pozostały import - próbujemy z obsługą błędów
try:
    from utils.session import init_session_state, clear_session
    from utils.components import zen_header, navigation_menu
    from views.login import show_login_page
    from views.dashboard import show_dashboard
    from views.degen_test import show_degen_test
    from views.lesson import show_lesson
    from views.profile import show_profile
    from views.degen_explorer import show_degen_explorer
    from views.skills_new import show_skill_tree
    # Import shop module is done within the routing section
except Exception as e:
    st.error(f"Błąd podczas importowania modułów: {str(e)}")
    st.code(traceback.format_exc())

# Załaduj plik CSS
def load_css(css_file):
    with open(css_file, "r", encoding="utf-8") as f:
        css = f.read()
    return css

# Ścieżka do pliku CSS
css_path = os.path.join(os.path.dirname(__file__), "static", "css", "style.css")
css = load_css(css_path)
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def main():
    # Initialize session state
    init_session_state()
    
    # Sidebar for logged-in users
    if st.session_state.logged_in:
        with st.sidebar:
            st.markdown(f"### Witaj, {st.session_state.username}!")
            
            # Nawigacja
            navigation_menu()
            
            # Przycisk wylogowania na dole sidebara
            if st.button("Wyloguj się", key="logout_button"):
                clear_session()
                st.rerun()
                
    # Page routing
    if not st.session_state.logged_in:
        show_login_page()
    else:
        if st.session_state.page == "dashboard":
            show_dashboard()
        elif st.session_state.page == "degen_test":
            show_degen_test()
        elif st.session_state.page == "lesson":
            show_lesson()
        elif st.session_state.page == "profile":
            show_profile()
        elif st.session_state.page == "degen_explorer":
            show_degen_explorer()
        elif st.session_state.page == "skills":
            show_skill_tree()
        elif st.session_state.page == "shop":
            try:
                # Direct import to ensure we only use the new shop
                import views.shop_new
                views.shop_new._IS_SHOP_NEW_LOADED = False  # Reset flag each time
                from views.shop_new import show_shop
                show_shop()
            except Exception as e:
                st.error(f"Błąd podczas ładowania sklepu: {e}")
                import traceback
                st.code(traceback.format_exc())

st.markdown("""
<style>
div.stButton > button { 
    margin-bottom: 1px; 
}

/* Poprawa widoczności tekstu w przyciskach przy różnych stanach */
div.stButton > button:hover {
    color: #000000 !important; /* Czarny tekst dla lepszego kontrastu */
    font-weight: bold;
}

/* Przyciski z niebieskim tłem */
section[data-testid="stSidebar"] div.stButton > button:hover,
div.stButton > button[kind="primary"]:hover {
    color: black !important; /* Biały tekst na niebieskim tle */
    text-shadow: 0 0 2px rgba(0,0,0,0.5); /* Cień tekstu dla lepszej widoczności */
    font-weight: bold;
}

/* Przyciski w aplikacji - "POKAŻ LEK", "ANALITYKA" itp. */
button[kind="secondary"] {
    color: black !important;
    text-shadow: 0 0 2px rgba(0,0,0,0.5); 
    font-weight: bold !important;
}

button[kind="secondary"]:hover {
    color: white !important;
    background-color: var(--primary-color) !important;
}

/* Style poprawiające responsywność na urządzeniach mobilnych */
@media (max-width: 768px) {
    /* Zwiększenie obszaru klikalnego dla elementów rozwijanego menu */
    .st-expander {
        padding: 10px 0;
    }
    
    /* Zwiększenie rozmiaru czcionki w rozwijanym menu */
    .st-expander .st-expander-header {
        font-size: 1.2rem !important;
        padding: 15px 10px !important;
    }
    
    /* Zapewnienie wystarczającej przestrzeni dla zawartości rozwijanej */
    .st-expander .st-expander-content {
        padding: 12px !important;
    }
    
    /* Dodanie wyraźnego wskaźnika dotyku */
    .st-expander .st-expander-header:after {
        content: "▼";
        margin-left: 8px;
        font-size: 0.8rem;
    }
    
    .st-expander.st-expander-expanded .st-expander-header:after {
        content: "▲";
    }
}
</style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()'''

# Define the content for shop.py
shop_py_content = '''import streamlit as st

# Uproszczona wersja sklepu - jedynie do kompatybilności wstecznej
# Właściwa implementacja znajduje się w shop_new.py

def show_shop():
    """
    Wyświetla sklep z przedmiotami do zakupu.
    UWAGA: Ta wersja jest przestarzała - używamy shop_new.py
    """
    # Import and use shop_new.py implementation
    try:
        import views.shop_new
        views.shop_new._IS_SHOP_NEW_LOADED = False  # Reset flag each time
        from views.shop_new import show_shop as show_shop_new
        show_shop_new()
    except Exception as e:
        st.error(f"Błąd podczas ładowania nowego sklepu: {e}")'''

# Create the fixed versions
base_path = r'c:\Users\Anna\Dropbox\Maverick\ZenDegenAcademy'

# Backup and create main.py
with open(os.path.join(base_path, 'main.py.final_fix'), 'w') as f:
    f.write(main_py_content)

# Backup and create shop.py
with open(os.path.join(base_path, 'views', 'shop.py.final_fix'), 'w') as f:
    f.write(shop_py_content)

print("Fixed files created: main.py.final_fix and views/shop.py.final_fix")
print("Please rename them to main.py and views/shop.py respectively.")
