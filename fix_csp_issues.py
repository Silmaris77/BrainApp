import streamlit as st
import importlib
import sys
import os

def fix_csp_issues():
    """
    Główna funkcja naprawiająca problemy z Content Security Policy
    """
    st.title("Naprawa błędów CSP w Neuroliderach")
    
    st.markdown("""
    To narzędzie pomaga naprawić problemy związane z Content Security Policy (CSP) w aplikacji Neuroliderzy.
    Główne źródło problemów to inline JavaScript, który jest zablokowany przez CSP.
    
    Wybierz moduł, który chcesz naprawić:
    """)
    
    # Menu wyboru modułu do naprawy
    module_choice = st.selectbox(
        "Wybierz moduł:",
        ["Panel administratora", "Lekcje", "Sklep", "Instrukcje migracji"]
    )
    
    # Wyświetl odpowiedni moduł
    if module_choice == "Panel administratora":
        fix_admin_view()
    elif module_choice == "Lekcje":
        fix_lesson_view()
    elif module_choice == "Sklep":
        fix_shop_view()
    elif module_choice == "Instrukcje migracji":
        show_migration_instructions()

def fix_admin_view():
    """
    Zastępuje stary widok admin_card_layout.py nowym admin_ui.py
    """
    st.header("Naprawa panelu administratora")
    
    try:
        # Importuj nowy moduł (który już został utworzony)
        from views.admin_ui import show_admin_dashboard
        
        st.success("✅ Moduł admin_ui.py został pomyślnie zaimportowany")
        
        # Wyświetl informacje
        st.markdown("""
        ### Zmienione elementy:
        - Usunięto inline JavaScript używający 'onclick'
        - Zastąpiono elementy HTML komponentami Streamlit
        - Dodano responsywny layout dla różnych urządzeń
        - Zintegrowano z systemem UI zgodnym z CSP
        """)
        
        # Opcja przetestowania nowego widoku
        if st.button("Przetestuj nowy panel administratora"):
            st.session_state.username = "admin"  # Tymczasowo ustaw użytkownika jako admina
            show_admin_dashboard()
            
    except Exception as e:
        st.error(f"❌ Błąd podczas importowania modułu admin_ui.py: {str(e)}")

def fix_lesson_view():
    """
    Zastępuje stary widok lesson_card_layout.py nowym lesson_ui.py
    """
    st.header("Naprawa widoku lekcji")
    
    try:
        # Importuj nowy moduł (który już został utworzony)
        from views.lesson_ui import show_lesson_content, show_lesson_summary
        
        st.success("✅ Moduł lesson_ui.py został pomyślnie zaimportowany")
        
        # Wyświetl informacje
        st.markdown("""
        ### Zmienione elementy:
        - Usunięto inline JavaScript używający 'onclick'
        - Zastąpiono przyciski HTML komponentami Streamlit
        - Dodano responsywny layout dla treści lekcji
        - Dodano obsługę zdarzeń bez JavaScript
        """)
        
        # Opcja przetestowania nowego widoku
        if st.button("Przetestuj widok lekcji"):
            # Przykładowe dane do przetestowania
            lesson_id = "lesson1"
            if 'test_view' not in st.session_state:
                st.session_state.test_view = "content"
                
            if st.session_state.test_view == "content":
                show_lesson_content(lesson_id)
                # Symuluj rozpoczęcie lekcji po kliknięciu
                if st.session_state.get('lesson_started', False):
                    st.session_state.test_view = "summary"
                    st.rerun()
            else:
                show_lesson_summary(lesson_id, 100, 50)
                # Symuluj powrót do drzewa umiejętności
                if st.session_state.get('return_to_skills', False):
                    st.session_state.test_view = "content"
                    st.session_state.pop('return_to_skills', None)
                    st.session_state.pop('lesson_started', None)
                    st.rerun()
            
    except Exception as e:
        st.error(f"❌ Błąd podczas importowania modułu lesson_ui.py: {str(e)}")

def fix_shop_view():
    """
    Zastępuje stary widok shop_card_layout.py nowym shop_ui.py
    """
    st.header("Naprawa widoku sklepu")
    
    try:
        # Importuj nowy moduł (który już został utworzony)
        from views.shop_ui import show_shop_ui
        
        st.success("✅ Moduł shop_ui.py został pomyślnie zaimportowany")
        
        # Wyświetl informacje
        st.markdown("""
        ### Zmienione elementy:
        - Usunięto inline JavaScript używający 'onclick'
        - Zastąpiono przyciski HTML komponentami Streamlit
        - Dodano responsywną siatkę produktów
        - Zintegrowano z systemem powiadomień
        """)
        
        # Opcja przetestowania nowego widoku
        if st.button("Przetestuj widok sklepu"):
            show_shop_ui()
            
    except Exception as e:
        st.error(f"❌ Błąd podczas importowania modułu shop_ui.py: {str(e)}")

def show_migration_instructions():
    """
    Wyświetla instrukcje migracji dla deweloperów
    """
    st.header("Instrukcje migracji dla deweloperów")
    
    st.markdown("""
    ### Jak migrować inne pliki z układem kart
    
    1. **Zidentyfikuj problematyczny kod**:
       - Wyszukaj wszystkie wystąpienia `onclick="javascript` lub `onclick="document`
       - Znajdź wszystkie przypadki, gdzie HTML jest generowany z atrybutami `onclick`
    
    2. **Utwórz nowy plik UI**:
       - Utwórz nowy plik w katalogu `views` z nazwą `[nazwa_modułu]_ui.py`
       - Importuj niezbędne komponenty z `utils.ui`
       - Zdefiniuj główną funkcję do renderowania widoku
    
    3. **Zamień inline JavaScript**:
       - Użyj komponentu `zen_button` zamiast przycisków HTML z `onclick`
       - Zastosuj stan w sesji Streamlit do kontrolowania przepływu aplikacji
       - Użyj `responsive_grid()` do tworzenia responsywnych layoutów
    
    4. **Aktualizuj importy**:
       - Zmień importy w głównym pliku aplikacji, aby używały nowych modułów UI
       - W razie potrzeby, używaj warunkowego importu dla kompatybilności wstecznej
    """)
    
    # Przykład migracji kodu
    st.markdown("### Przykład migracji kodu")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Stary kod z inline JavaScript:**")
        st.code("""
# HTML z inline JavaScript
st.markdown('''
<button class='material-button' 
    onclick="document.getElementById('btn-action').click()">
    Kliknij mnie
</button>
''', unsafe_allow_html=True)

# Ukryty przycisk
if st.button("Kliknij mnie", key="btn-action",
             label_visibility="collapsed"):
    # Logika
    pass
        """, language="python")
        
    with col2:
        st.markdown("**Nowy kod zgodny z CSP:**")
        st.code("""
# Import komponentów UI
from utils.ui.components.interactive import zen_button

# Bezpośredni przycisk Streamlit
if zen_button("Kliknij mnie", key="btn-action"):
    # Logika (ta sama co wcześniej)
    pass
        """, language="python")

def scan_inline_js():
    """
    Skanuje pliki w projekcie pod kątem użycia inline JavaScript
    """
    st.header("Wykrywanie inline JavaScript")
    
    views_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'views')
    results = {}
    
    # Szukaj wzorców problematycznego kodu
    patterns = ['onclick="document', 'onclick="javascript']
    
    for filename in os.listdir(views_dir):
        if filename.endswith('.py'):
            file_path = os.path.join(views_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    
                    # Sprawdź każdy wzorzec
                    for pattern in patterns:
                        if pattern in content:
                            if filename not in results:
                                results[filename] = []
                            results[filename].append(pattern)
            except Exception as e:
                st.warning(f"Nie można przeczytać pliku {filename}: {str(e)}")
    
    # Wyświetl wyniki
    if results:
        st.warning(f"Znaleziono {len(results)} plików z inline JavaScript:")
        
        for filename, patterns in results.items():
            with st.expander(f"📄 {filename}"):
                st.markdown(f"**Problematyczne wzorce:**")
                for pattern in patterns:
                    st.markdown(f"- `{pattern}`")
                
                if filename in ["admin_card_layout.py", "lesson_card_layout.py", "shop_card_layout.py"]:
                    st.success("✓ Nowa wersja pliku została już utworzona")
                else:
                    st.warning("⚠️ Ten plik wymaga migracji")
    else:
        st.success("Nie znaleziono plików z inline JavaScript.")

if __name__ == "__main__":
    fix_csp_issues()
    scan_inline_js()
