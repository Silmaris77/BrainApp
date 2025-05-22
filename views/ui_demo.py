import streamlit as st
from utils.ui import initialize_ui, theme_selector
from utils.ui.components.cards import stat_card, skill_card, mission_card, lesson_card
from utils.ui.components.interactive import zen_button, notification, progress_bar
from utils.ui.components.text import zen_header, tip_block, quote_block, content_section
from utils.ui.layouts.grid import render_dashboard_header, render_stats_section, responsive_grid, render_two_column_layout
from utils.ui.bridge import initialize_bridge, bridge_degen_card, bridge_stat_card

def show_ui_demo():
    """Demonstracja nowego systemu UI."""
    # Inicjalizacja UI
    initialize_ui()
    
    # Selektor motywu
    with st.sidebar:
        st.header("Opcje UI")
        theme_selector()
        
        # Przełącznik trybu bridge
        use_bridge_mode = st.checkbox("Tryb mostkowania (bridge mode)", value=False, 
                                 help="Włącz, aby zobaczyć jak działa tryb kompatybilności wstecznej")
        
        if use_bridge_mode:
            initialize_bridge()
        
        st.markdown("---")
        st.write("Ten widok demonstracyjny prezentuje wszystkie komponenty UI dostępne w nowym systemie. Możesz przełączać się między różnymi motywami, aby zobaczyć, jak komponenty dostosowują się do różnych stylów.")
      # Tabs dla różnych kategorii komponentów
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Statystyki i karty", "📝 Tekst i zawartość", "🔘 Interaktywne", "📐 Layout", "🌉 Bridge Mode"])
    
    with tab1:
        # Nagłówek strony
        render_dashboard_header("Statystyki i karty", "Komponenty do wyświetlania danych")
        
        # Sekcja statystyk
        st.subheader("Przykład sekcji statystyk")
        stats_data = [
            ("🏆", "89%", "Całkowity postęp"),
            ("📚", "24", "Ukończone lekcje"),
            ("⭐", "5", "Średni poziom")
        ]
        render_stats_section(stats_data)
        
        # Przykład karty umiejętności
        st.subheader("Przykład karty umiejętności")
        
        # Użyj responsywnej siatki do wyświetlenia kart
        columns = responsive_grid(columns_desktop=3, columns_tablet=2, columns_mobile=1)
        
        with columns[0]:
            skill_card(
                "Neurobiologia przywództwa", 
                75, 
                "in-progress", 
                "🧠", 
                "Podstawy neuroprzywództwa i struktura mózgu lidera", 
                8, 
                10
            )
        
        with columns[1]:
            skill_card(
                "Procesy decyzyjne", 
                100, 
                "max-level", 
                "⚖️", 
                "Analiza procesów decyzyjnych w kontekście neuroliderskim", 
                10, 
                10
            )
        
        with columns[2]:
            skill_card(
                "Empatia i komunikacja", 
                30, 
                "in-progress", 
                "🗣️", 
                "Budowanie efektywnej komunikacji w zespole", 
                3, 
                10
            )
            
        # Przykład karty misji
        st.subheader("Przykład karty misji")
        mission_card(
            "Ukończ moduł Neurobiologia", 
            "Poznaj podstawy neurobiologii przywództwa", 
            "🧠", 
            250, 
            progress=75, 
            completed=False
        )
        
        mission_card(
            "Przeczytaj artykuł naukowy", 
            "Zapoznaj się z najnowszymi badaniami nad neuronauki", 
            "📚", 
            100, 
            progress=100, 
            completed=True
        )
        
        # Przykład karty lekcji
        st.subheader("Przykład karty lekcji")
        lesson_card(
            "Wprowadzenie do neuronauk", 
            "Poznaj podstawowe terminy i koncepcje neuronaukowe, które pomogą Ci zrozumieć jak działa mózg lidera.", 
            xp=150, 
            difficulty="beginner", 
            category="Neurobiologia", 
            completed=False
        )
        
        lesson_card(
            "Neurony lustrzane w przywództwie", 
            "Odkryj rolę neuronów lustrzanych w budowaniu relacji lidera z zespołem i wpływ empatii na efektywność przywódczą.", 
            xp=200, 
            difficulty="intermediate", 
            category="Neurobiologia", 
            completed=True
        )
    
    with tab2:
        # Przykład bloków tekstowych
        render_dashboard_header("Tekst i zawartość", "Komponenty tekstowe i informacyjne")
        
        # Przykład bloku ze wskazówką
        st.subheader("Przykład bloku ze wskazówką")
        tip_block(        "Ten nowy system UI pozwala na łatwiejsze zarządzanie i modyfikację layoutu aplikacji.",
        type="tip",
        title="Tip dla nowego UI",
        icon="💡"
    )
    
    # Przykład cytatu
    st.subheader("Przykład cytatu")
    quote_block(
        "Neuroplastyczność mózgu lidera jest kluczowym czynnikiem pozwalającym na adaptację do zmieniających się warunków i wyzwań biznesowych.",
        "Dr. David Rock, NeuroLeadership Institute"
    )
    
    # Przykład sekcji zawartości
    st.subheader("Przykład sekcji zawartości")
    content_section(
        "Wpływ stresu na mózg lidera",
        """
        <p>Długotrwały stres powoduje zwiększone wydzielanie kortyzolu, który może wpływać na zdolność podejmowania decyzji.</p>
        <ul>
            <li>Zmniejszona aktywność kory przedczołowej</li>
            <li>Osłabienie pamięci roboczej</li>
            <li>Trudności w ocenie ryzyka</li>
        </ul>
        """,
        icon="🧠"
    )
    
    with tab3:
        # Przykład interaktywnych komponentów
        render_dashboard_header("Komponenty interaktywne", "Przyciski i elementy interaktywne")
        
        # Przyciski
        st.subheader("Przyciski")
        col1, col2, col3 = st.columns(3)
        with col1:
            if zen_button("Przycisk podstawowy", key="basic_button"):
                notification("Kliknięto przycisk podstawowy", "info")
        
        with col2:
            if zen_button("Zapisz zmiany", key="save_button"):
                notification("Zmiany zostały zapisane!", "success")
        
        with col3:
            if zen_button("Usuń dane", key="delete_button"):
                notification("Ta operacja jest niebezpieczna!", "warning")
        
        # Pasek postępu
        st.subheader("Pasek postępu")
        progress_value = st.slider("Wartość postępu", 0.0, 1.0, 0.7, 0.1)
        progress_bar(progress_value)
        
        # Powiadomienia
        st.subheader("Powiadomienia")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if zen_button("Info", key="info_notification"):
                notification("To jest informacja", "info")
        
        with col2:
            if zen_button("Sukces", key="success_notification"):
                notification("Operacja zakończona sukcesem", "success")
        
        with col3:
            if zen_button("Ostrzeżenie", key="warning_notification"):
                notification("Uwaga! To jest ostrzeżenie", "warning")
        
        with col4:
            if zen_button("Błąd", key="error_notification"):
                notification("Wystąpił błąd!", "error")
    
    with tab4:
        # Przykład układów
        render_dashboard_header("Układy (Layouts)", "Komponenty do organizacji treści")
        
        # Układ siatki
        st.subheader("Układ siatki responsywnej")
        st.write("Ta siatka automatycznie dostosowuje się do rozmiaru ekranu:")
        st.code("""
# Tworzenie responsywnej siatki
columns = responsive_grid(columns_desktop=3, columns_tablet=2, columns_mobile=1)

with columns[0]:
    # zawartość pierwszej kolumny
with columns[1]:
    # zawartość drugiej kolumny
with columns[2]:
    # zawartość trzeciej kolumny
        """)
        
        # Układ dwukolumnowy
        st.subheader("Układ dwukolumnowy")
        def left_column():
            st.write("### Lewa kolumna")
            st.write("Ta kolumna zawiera ważne informacje.")
            st.write("Może zawierać dane nawigacyjne lub filtry.")
        
        def right_column():
            st.write("### Prawa kolumna")
            st.write("Ta kolumna zawiera główną zawartość.")
            with st.expander("Rozwiń, aby zobaczyć więcej"):
                st.write("Szczegółowe informacje można ukryć w expanderze.")
            render_two_column_layout(left_column, right_column, left_width=1, right_width=2)
    
    with tab5:
        # Bridge mode demo
        render_dashboard_header("Tryb kompatybilności wstecznej", "Mostkowanie między starym a nowym systemem UI")
        
        # Wyjaśnienie
        st.markdown("""
        Tryb kompatybilności wstecznej (bridge mode) pozwala na stopniowe migrowanie aplikacji
        ze starego do nowego systemu UI. Funkcje mostkujące przyjmują te same parametry co stare
        komponenty, ale wewnętrznie używają nowego systemu UI.
        
        To pozwala zacząć korzystać z nowego systemu bez konieczności jednorazowej zmiany całego kodu.
        """)
        
        # Przykład mostu dla degen_card
        st.subheader("Przykład: bridge_degen_card")
        with st.expander("Zobacz kod"):
            st.code("""
# Stary kod
degen_card(
    title="Neurobiologia przywództwa", 
    description="Podstawy neuroprzywództwa", 
    icon="🧠", 
    progress=75, 
    status="in-progress"
)

# Nowy kod z mostkowaniem
bridge_degen_card(
    title="Neurobiologia przywództwa", 
    description="Podstawy neuroprzywództwa", 
    icon="🧠", 
    progress=75, 
    status="in-progress"
)
""")
        
        st.markdown("### Wynik mostkowania:")
        bridge_degen_card(
            title="Neurobiologia przywództwa", 
            description="Podstawy neuroprzywództwa w kontekście teorii decyzji i neurologicznych podstaw zarządzania zespołami", 
            icon="🧠", 
            progress=75, 
            status="in-progress"
        )
        
        # Przykład mostu dla stat_card
        st.subheader("Przykład: bridge_stat_card")
        with st.expander("Zobacz kod"):
            st.code("""
# Stary kod
stat_card(
    label="Ukończone lekcje", 
    value="24", 
    icon="📚",
    change="+3", 
    change_type="positive"
)

# Nowy kod z mostkowaniem
bridge_stat_card(
    label="Ukończone lekcje", 
    value="24", 
    icon="📚",
    change="+3", 
    change_type="positive"
)
""")
        
        st.markdown("### Wynik mostkowania:")
        cols = st.columns(3)
        with cols[0]:
            bridge_stat_card(
                label="Ukończone lekcje", 
                value="24", 
                icon="📚",
                change="+3", 
                change_type="positive"
            )
        
        # Jak wdrożyć bridge mode
        st.subheader("Wdrażanie trybu kompatybilności")
        st.markdown("""
        Aby wdrożyć tryb kompatybilności, wykonaj następujące kroki:
        
        1. Dodaj inicjalizację bridge mode na początku aplikacji:
        ```python
        from utils.ui.bridge import initialize_bridge
        
        # Na początku aplikacji
        initialize_bridge()
        ```
        
        2. Zmodyfikuj importy, używając funkcji mostkujących:
        ```python
        # Stary import
        from utils.components import degen_card, stat_card
        
        # Nowy import z mostkowaniem
        from utils.ui.bridge import bridge_degen_card as degen_card
        from utils.ui.bridge import bridge_stat_card as stat_card
        ```
        
        3. Stopniowo migruj komponenty do nowego systemu UI według potrzeb
        ```python
        # Bezpośrednie użycie nowych komponentów
        from utils.ui.components.cards import skill_card
        ```
        """)
    
    # Kod demonstracyjny
    st.markdown("---")
    st.subheader("Jak używać nowego systemu:")
    st.code('''
import streamlit as st
from utils.ui import initialize_ui
from utils.ui.components.cards import stat_card, skill_card
from utils.ui.components.text import zen_header, tip_block
from utils.ui.layouts.grid import render_dashboard_header, responsive_grid

# Inicjalizacja UI
initialize_ui()

# Nagłówek strony
render_dashboard_header("Moja strona", "Podtytuł strony")

# Wyświetl karty w responsywnej siatce
columns = responsive_grid(columns_desktop=3, columns_tablet=2, columns_mobile=1)
with columns[0]:
    stat_card("💰", "5000", "Punkty XP")
    
# Dodaj wskazówkę
tip_block("Ważna informacja dla użytkownika", type="info")
''')

if __name__ == "__main__":
    show_ui_demo()
