import streamlit as st
from PIL import Image
from data.neuroleader_types import NEUROLEADER_TYPES
from data.neuroleader_details import neuroleader_details
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

def show_neuroleader_explorer():
    """
    Wyświetla stronę umożliwiającą eksplorację wszystkich typów neuroliderów
    wraz z ich szczegółowymi opisami.
    """
    # Zastosuj style Material 3
    apply_material3_theme()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    zen_header("Odkrywanie Typów Neuroliderów")
    
    # Wprowadzenie do typów neuroliderów
    st.markdown("""
    ## 🔍 Poznaj różne style przywództwa neurobiologicznego
    
    Każdy neurolider ma unikalne podejście do przewodzenia zespołowi, uwarunkowane cechami osobowości,
    wzorcami aktywności mózgu, emocjami i strategiami działania. Poniżej znajdziesz szczegółowe opisy wszystkich
    typów neuroliderów, które pomogą Ci zrozumieć różne style przywództwa i ich neurobiologiczne podstawy.
    
    Wybierz interesujący Cię typ neuroliderera z listy i odkryj:
    - Charakterystykę głównych cech
    - Profil emocjonalny
    - Zachowania i postawy
    - Neurobiologiczne podstawy
    - Kluczowe wyzwania
    - Ścieżkę rozwoju przywódczego
    """)
    
    # Wybór typu neuroliderera
    selected_type = st.selectbox(
        "Wybierz typ neuroliderera do szczegółowej analizy:",
        list(NEUROLEADER_TYPES.keys()),
        format_func=lambda x: f"{x} - {NEUROLEADER_TYPES[x]['description'][:50]}..."
    )
    
    if selected_type:
        # Tworzenie sekcji dla wybranego typu
        color = NEUROLEADER_TYPES[selected_type]["color"]
        content_section(
            f"{selected_type}", 
            NEUROLEADER_TYPES[selected_type]["description"],
            icon="🔍",
            border_color=color,
            collapsed=False
        )
        
        # Mocne strony i wyzwania w dwóch kolumnach
        col1, col2 = st.columns(2)
        with col1:
            content_section("Mocne strony:", 
                            "\n".join([f"- ✅ {strength}" for strength in NEUROLEADER_TYPES[selected_type]["strengths"]]), 
                            icon="💪", 
                            collapsed=False)
        
        with col2:
            content_section("Wyzwania:", 
                           "\n".join([f"- ⚠️ {challenge}" for challenge in NEUROLEADER_TYPES[selected_type]["challenges"]]), 
                           icon="🚧", 
                           collapsed=False)
        
        # Rekomendowana strategia jako tip_block
        tip_block(clean_html(NEUROLEADER_TYPES[selected_type]["strategy"]), title="Rekomendowana strategia", icon="🎯")
        
        # Szczegółowy opis z neuroleader_details.py
        st.markdown("---")
        st.subheader("Szczegółowa analiza typu")
        if selected_type in neuroleader_details:
            content_section(
                "Pełny opis",
                neuroleader_details[selected_type],
                icon="📚",
                collapsed=True
            )
        else:
            notification("Szczegółowy opis dla tego typu neuroliderera nie jest jeszcze dostępny.", type="warning")
        
        # Porównanie z innymi typami
        st.markdown("---")
        st.subheader("Porównaj z innymi typami")
        
        # Pozwól użytkownikowi wybrać drugi typ do porównania
        comparison_type = st.selectbox(
            "Wybierz typ neuroliderera do porównania:",
            [t for t in NEUROLEADER_TYPES.keys() if t != selected_type],
            format_func=lambda x: f"{x} - {NEUROLEADER_TYPES[x]['description'][:50]}..."
        )
        
        if comparison_type:
            # Tabela porównawcza
            col1, col2 = st.columns(2)
            
            # Przygotuj listy poza f-stringiem dla pierwszego typu
            strengths_list_1 = "\n".join([f"- ✅ {strength}" for strength in NEUROLEADER_TYPES[selected_type]["strengths"]])
            challenges_list_1 = "\n".join([f"- ⚠️ {challenge}" for challenge in NEUROLEADER_TYPES[selected_type]["challenges"]])
            strategy_text_1 = clean_html(NEUROLEADER_TYPES[selected_type]["strategy"])
            
            # Dla pierwszego typu (wybranego)
            with col1:
                content_section(
                    selected_type,
                    f"""**Opis:** {NEUROLEADER_TYPES[selected_type]['description']}
        
**Mocne strony:**
{strengths_list_1}

**Wyzwania:**
{challenges_list_1}

**Strategia:**
{strategy_text_1}
                    """,
                    icon="🔍",
                    border_color=NEUROLEADER_TYPES[selected_type]["color"],
                    collapsed=False
                )
            
            # Przygotuj listy poza f-stringiem dla drugiego typu
            strengths_list_2 = "\n".join([f"- ✅ {strength}" for strength in NEUROLEADER_TYPES[comparison_type]["strengths"]])
            challenges_list_2 = "\n".join([f"- ⚠️ {challenge}" for challenge in NEUROLEADER_TYPES[comparison_type]["challenges"]])
            strategy_text_2 = clean_html(NEUROLEADER_TYPES[comparison_type]["strategy"])
            
            # Dla drugiego typu (porównywanego)
            with col2:
                content_section(
                    comparison_type,
                    f"""**Opis:** {NEUROLEADER_TYPES[comparison_type]['description']}
        
**Mocne strony:**
{strengths_list_2}

**Wyzwania:**
{challenges_list_2}

**Strategia:**
{strategy_text_2}
                    """,
                    icon="🔍",
                    border_color=NEUROLEADER_TYPES[comparison_type]["color"],
                    collapsed=False
                )
      # Link powrotny do testu
    st.markdown("---")
    
    # Przyciski nawigacyjne w dwóch kolumnach
    col1, col2 = st.columns(2)
    with col1:        
        if zen_button("📋 Przejdź do testu typu neuroliderera", key="go_to_test", use_container_width=True):
            st.session_state.page = 'neuroleader_test'
            st.rerun()
    
    # Przycisk do powrotu do dashboardu
    with col2:
        if zen_button("🏠 Powrót do dashboardu", key="back_to_dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
