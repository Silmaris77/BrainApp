import streamlit as st
from PIL import Image
from data.test_questions import DEGEN_TYPES
from data.degen_details import degen_details
from utils.components import zen_header, content_section, quote_block, tip_block, notification, zen_button
from utils.material3_components import apply_material3_theme
from utils.layout import get_device_type, responsive_grid, responsive_container, toggle_device_view
import re

# Poprawka dla funkcji clean_html, aby była bardziej skuteczna
def clean_html(text):
    """Usuwa wszystkie tagi HTML z tekstu i normalizuje białe znaki"""
    # Najpierw usuń wszystkie tagi HTML
    text_without_tags = re.sub(r'<.*?>', '', text)
    # Normalizuj białe znaki (zamień wiele spacji, tabulacji, nowych linii na pojedyncze spacje)
    normalized_text = re.sub(r'\s+', ' ', text_without_tags)
    return normalized_text.strip()

def show_degen_explorer():
    """
    Wyświetla stronę umożliwiającą eksplorację wszystkich typów degenów 
    wraz z ich szczegółowymi opisami.
    """    # Zastosuj style Material 3
    apply_material3_theme()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    zen_header("Odkrywanie Typów Degenów")
    
    # Wprowadzenie do typów degenów
    st.markdown("""
    ## 🔍 Poznaj różne style inwestycyjne
    
    Każdy inwestor ma unikalne podejście do rynków finansowych, uwarunkowane cechami osobowości,
    emocjami, strategiami i wzorcami zachowań. Poniżej znajdziesz szczegółowe opisy wszystkich
    typów degenów, które pomogą Ci zrozumieć różne style inwestycyjne i ich implikacje.
    
    Wybierz interesujący Cię typ degena z listy i odkryj:
    - Charakterystykę głównych cech
    - Profil emocjonalny
    - Zachowania i postawy
    - Neurobiologiczne podstawy
    - Kluczowe wyzwania
    - Ścieżkę rozwoju inwestorskiego
    """)
    
    # Wybór typu degena
    selected_type = st.selectbox(
        "Wybierz typ degena do szczegółowej analizy:",
        list(DEGEN_TYPES.keys()),
        format_func=lambda x: f"{x} - {DEGEN_TYPES[x]['description'][:50]}..."
    )
    if selected_type:
        # Tworzenie sekcji dla wybranego typu
        color = DEGEN_TYPES[selected_type]["color"]
        content_section(
            f"{selected_type}", 
            DEGEN_TYPES[selected_type]["description"],
            icon="🔍",
            border_color=color,
            collapsed=False
        )
          # Mocne strony i wyzwania w dwóch kolumnach
        col1, col2 = st.columns(2)
        with col1:
            content_section("Mocne strony:", 
                            "\n".join([f"- ✅ {strength}" for strength in DEGEN_TYPES[selected_type]["strengths"]]), 
                            icon="💪", 
                            collapsed=False)
        
        with col2:
            content_section("Wyzwania:", 
                           "\n".join([f"- ⚠️ {challenge}" for challenge in DEGEN_TYPES[selected_type]["challenges"]]), 
                           icon="🚧", 
                           collapsed=False)
        
        # Rekomendowana strategia jako tip_block
        tip_block(clean_html(DEGEN_TYPES[selected_type]["strategy"]), title="Rekomendowana strategia", icon="🎯")
          # Szczegółowy opis z degen_details.py
        st.markdown("---")
        st.subheader("Szczegółowa analiza typu")
        if selected_type in degen_details:
            content_section(
                "Pełny opis",
                degen_details[selected_type],
                icon="📚",
                collapsed=True
            )
        else:
            notification("Szczegółowy opis dla tego typu degena nie jest jeszcze dostępny.", type="warning")
        
        # Porównanie z innymi typami
        st.markdown("---")
        st.subheader("Porównaj z innymi typami")
        
        # Pozwól użytkownikowi wybrać drugi typ do porównania
        comparison_type = st.selectbox(
            "Wybierz typ degena do porównania:",
            [t for t in DEGEN_TYPES.keys() if t != selected_type],
            format_func=lambda x: f"{x} - {DEGEN_TYPES[x]['description'][:50]}..."
        )
        if comparison_type:
            # Tabela porównawcza
            col1, col2 = st.columns(2)
            
            # Przygotuj listy poza f-stringiem dla pierwszego typu
            strengths_list_1 = "\n".join([f"- ✅ {strength}" for strength in DEGEN_TYPES[selected_type]["strengths"]])
            challenges_list_1 = "\n".join([f"- ⚠️ {challenge}" for challenge in DEGEN_TYPES[selected_type]["challenges"]])
            strategy_text_1 = clean_html(DEGEN_TYPES[selected_type]["strategy"])
            
            # Dla pierwszego typu (wybranego)
            with col1:
                content_section(
                    selected_type,
                    f"""**Opis:** {DEGEN_TYPES[selected_type]['description']}
        
**Mocne strony:**
{strengths_list_1}

**Wyzwania:**
{challenges_list_1}

**Strategia:**
{strategy_text_1}
                    """,
                    icon="🔍",
                    border_color=DEGEN_TYPES[selected_type]["color"],
                    collapsed=False
                )
            
            # Przygotuj listy poza f-stringiem dla drugiego typu
            strengths_list_2 = "\n".join([f"- ✅ {strength}" for strength in DEGEN_TYPES[comparison_type]["strengths"]])
            challenges_list_2 = "\n".join([f"- ⚠️ {challenge}" for challenge in DEGEN_TYPES[comparison_type]["challenges"]])
            strategy_text_2 = clean_html(DEGEN_TYPES[comparison_type]["strategy"])
            
            # Dla drugiego typu (porównywanego)
            with col2:
                content_section(
                    comparison_type,
                    f"""**Opis:** {DEGEN_TYPES[comparison_type]['description']}
        
**Mocne strony:**
{strengths_list_2}

**Wyzwania:**
{challenges_list_2}

**Strategia:**
{strategy_text_2}
                    """,
                    icon="🔍",
                    border_color=DEGEN_TYPES[comparison_type]["color"],
                    collapsed=False
                )
      # Link powrotny do testu
    st.markdown("---")
    
    # Przyciski nawigacyjne w dwóch kolumnach
    col1, col2 = st.columns(2)
    with col1:
        if zen_button("📋 Przejdź do testu typu degena", key="go_to_test", use_container_width=True):
            st.session_state.page = 'degen_test'
            st.rerun()
    
    # Przycisk do powrotu do dashboardu
    with col2:
        if zen_button("🏠 Powrót do dashboardu", key="back_to_dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
