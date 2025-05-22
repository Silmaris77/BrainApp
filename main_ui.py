import streamlit as st
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
    from utils.ui import initialize_ui, theme_selector
    from utils.ui.components.interactive import zen_button, notification
    from utils.ui.components.text import zen_header    # Importy starych modułów (które jeszcze nie zostały zmigrowane)
    from views.login import show_login_page
    from views.lesson import show_lesson
    
    # Import nowych modułów zgodnych z CSP
    from views.degen_test_ui import show_degen_test
    from views.neuroleader_test_ui import show_neuroleader_test
    from views.neuroleader_explorer_ui import show_neuroleader_explorer
    
    # Importy nowych modułów zgodnych z CSP
    from views.skills_ui import show_skill_tree
    from views.dashboard_ui import show_dashboard
    from views.profile_ui import show_profile
    
    # Importy nowych modułów zgodnych z CSP
    from views.admin_ui import show_admin_dashboard
    from views.shop_ui import show_shop_ui
    from views.lesson_ui import show_lesson_content, show_lesson_summary
    
except Exception as e:
    st.error(f"Błąd podczas importowania modułów: {str(e)}")
    st.code(traceback.format_exc())
    st.stop()  # Stop execution if imports fail

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
    # Inicjalizacja systemu UI
    initialize_ui()
    
    # Initialize session state
    init_session_state()
    
    # Sidebar for logged-in users
    if st.session_state.logged_in:
        with st.sidebar:
            st.markdown(f"### Witaj, {st.session_state.username}!")
            
            # Wybór motywu
            theme_selector()
            
            # Przyciski nawigacji
            if zen_button("🏠 DASHBOARD", key="nav_dashboard"):
                st.session_state.page = "dashboard"
                st.rerun()
                
            if zen_button("🧠 TEST DEGENA", key="nav_degen_test"):
                st.session_state.page = "degen_test"
                st.rerun()
                
            if zen_button("🧩 TEST NEUROLIDERERA", key="nav_neuroleader_test"):
                st.session_state.page = "neuroleader_test"
                st.rerun()
                
            if zen_button("📚 LEKCJE", key="nav_lesson"):
                st.session_state.page = "lesson"
                st.rerun()
                
            if zen_button("🌟 UMIEJĘTNOŚCI", key="nav_skills"):
                st.session_state.page = "skills"
                st.rerun()
                
            if zen_button("🛒 SKLEP", key="nav_shop"):
                st.session_state.page = "shop"
                st.rerun()
                
            if zen_button("🔍 EKSPLORATOR", key="nav_explorer"):
                st.session_state.page = "neuroleader_explorer"
                st.rerun()
                
            if zen_button("👤 PROFIL", key="nav_profile"):
                st.session_state.page = "profile"
                st.rerun()
                
            # Admin panel button (only for admins)
            users_data = {}
            try:
                from data.users import load_user_data
                users_data = load_user_data()
                user_data = users_data.get(st.session_state.username, {})
                
                if user_data.get('role') == 'admin':
                    if zen_button("⚙️ ADMIN", key="nav_admin"):
                        st.session_state.page = "admin"
                        st.rerun()
            except Exception as e:
                pass  # Nie pokazuj błędu, jeśli nie można załadować danych
            
            # Przycisk wylogowania na dole sidebara
            if zen_button("Wyloguj się", key="logout_button"):
                clear_session()
                st.rerun()
                
    # Page routing
    if not st.session_state.logged_in:
        show_login_page()    
    else:
        if st.session_state.page == 'dashboard':
            show_dashboard()
        elif st.session_state.page == 'degen_test':
            show_degen_test()
        elif st.session_state.page == 'neuroleader_test':
            show_neuroleader_test()
        elif st.session_state.page == 'lesson':
            # Tutaj możemy używać starego modułu, ale w przyszłości zmienimy na nowy
            show_lesson()
        elif st.session_state.page == 'profile':
            show_profile()
        elif st.session_state.page == 'neuroleader_explorer':
            show_neuroleader_explorer()
        elif st.session_state.page == 'skills':
            show_skill_tree()
        elif st.session_state.page == 'shop':
            # Używamy nowego modułu zgodnego z CSP
            show_shop_ui()
        elif st.session_state.get('page') == 'admin':
            # Używamy nowego modułu zgodnego z CSP
            show_admin_dashboard()

if __name__ == "__main__":
    main()
