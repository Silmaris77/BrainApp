import streamlit as st
from PIL import Image
from data.test_questions import DEGEN_TYPES
from data.degen_details import degen_details
from utils.components import zen_header, content_section, quote_block, tip_block, notification, zen_button
from utils.material3_components import apply_material3_theme
from utils.layout import get_device_type, responsive_grid, responsive_container, toggle_device_view
from utils.card_layout import load_card_layout, create_card, create_grid, zen_section, data_panel
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
    wraz z ich szczegółowymi opisami, używając Card Layout.
    """
    # Zastosuj style Material 3
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    # Determine the layout grid size based on device type
    num_columns = 1 if device_type == 'mobile' else 2
    
    zen_header("Odkrywanie Typów Degenów")
    
    # Introduction card
    create_card(
        title="Poznaj różne style inwestycyjne",
        icon="🔍",
        content="""
        <div style="padding: 10px 0;">
            <p>Każdy inwestor ma unikalne podejście do rynków finansowych, uwarunkowane cechami osobowości,
            emocjami, strategiami i wzorcami zachowań.</p>
            
            <p style="margin-top: 10px;">Poniżej znajdziesz szczegółowe opisy wszystkich
            typów degenów, które pomogą Ci zrozumieć różne style inwestycyjne i ich implikacje.</p>
            
            <p style="margin-top: 10px;">Wybierz interesujący Cię typ degena z listy i odkryj:</p>
            <ul style="padding-left: 20px; margin-top: 5px;">
                <li>Charakterystykę głównych cech</li>
                <li>Profil emocjonalny</li>
                <li>Zachowania i postawy</li>
                <li>Neurobiologiczne podstawy</li>
                <li>Kluczowe wyzwania</li>
                <li>Ścieżkę rozwoju inwestorskiego</li>
            </ul>
        </div>
        """,
        key="intro_card"
    )
    
    # Type selector card
    create_card(
        title="Wybierz typ degena",
        icon="👇",
        content="""
        <p style="margin-bottom: 10px;">Wybierz typ degena do szczegółowej analizy:</p>
        """,
        key="selector_card"
    )
    
    # Type selection dropdown
    selected_type = st.selectbox(
        "Wybierz typ degena do szczegółowej analizy:",
        list(DEGEN_TYPES.keys()),
        format_func=lambda x: f"{x} - {DEGEN_TYPES[x]['description'][:50]}..."
    )
    
    if selected_type:
        # Type description card
        color = DEGEN_TYPES[selected_type]["color"]
        create_card(
            title=selected_type,
            icon="🎭",
            content=f"""
            <div style="padding: 10px 0;">
                <p style="font-size: 1.1rem; color: {color}; border-left: 3px solid {color}; padding-left: 10px;">
                    {DEGEN_TYPES[selected_type]["description"]}
                </p>
            </div>
            """,
            key="type_description_card"
        )
        
        # Create a grid for strengths and challenges
        cols = create_grid(num_columns)
        
        # Strengths card
        with cols[0]:
            create_card(
                title="Mocne strony",
                icon="💪",
                content="""
                <ul style="padding-left: 20px;">
                    {}
                </ul>
                """.format("\n".join([f"<li>✅ {strength}</li>" for strength in DEGEN_TYPES[selected_type]["strengths"]])),
                key="strengths_card"
            )
        
        # Challenges card
        with cols[1 if num_columns > 1 else 0]:
            create_card(
                title="Wyzwania",
                icon="🚧",
                content="""
                <ul style="padding-left: 20px;">
                    {}
                </ul>
                """.format("\n".join([f"<li>⚠️ {challenge}</li>" for challenge in DEGEN_TYPES[selected_type]["challenges"]])),
                key="challenges_card"
            )
        
        # Strategy card
        create_card(
            title="Rekomendowana strategia",
            icon="🎯",
            content=f"""
            <div style="padding: 10px 0; background-color: rgba(0,0,0,0.03); border-radius: 8px; padding: 15px;">
                <p>{clean_html(DEGEN_TYPES[selected_type]["strategy"])}</p>
            </div>
            """,
            key="strategy_card"
        )
        
        # Detailed description section
        zen_section("Szczegółowa analiza typu", icon="📚")
        
        if selected_type in degen_details:
            with st.expander("Rozwiń pełny opis", expanded=False):
                st.markdown(degen_details[selected_type])
        else:
            notification("Szczegółowy opis dla tego typu degena nie jest jeszcze dostępny.", type="warning")
        
        # Comparison section
        zen_section("Porównaj z innymi typami", icon="⚖️")
        
        # Type comparison selector
        comparison_type = st.selectbox(
            "Wybierz typ degena do porównania:",
            [t for t in DEGEN_TYPES.keys() if t != selected_type],
            format_func=lambda x: f"{x} - {DEGEN_TYPES[x]['description'][:50]}..."
        )
        
        if comparison_type:
            # Create a grid for comparison
            comp_cols = create_grid(num_columns)
            
            # First type card (selected)
            with comp_cols[0]:
                create_card(
                    title=selected_type,
                    icon="👤",
                    content=f"""
                    <div style="padding: 10px 0;">
                        <div style="margin-bottom: 15px;">
                            <h4 style="margin-bottom: 5px;">Opis:</h4>
                            <p>{DEGEN_TYPES[selected_type]['description']}</p>
                        </div>
                        
                        <div style="margin-bottom: 15px;">
                            <h4 style="margin-bottom: 5px;">Mocne strony:</h4>
                            <ul style="padding-left: 20px;">
                                {"".join([f"<li>✅ {strength}</li>" for strength in DEGEN_TYPES[selected_type]["strengths"]])}
                            </ul>
                        </div>
                        
                        <div style="margin-bottom: 15px;">
                            <h4 style="margin-bottom: 5px;">Wyzwania:</h4>
                            <ul style="padding-left: 20px;">
                                {"".join([f"<li>⚠️ {challenge}</li>" for challenge in DEGEN_TYPES[selected_type]["challenges"]])}
                            </ul>
                        </div>
                        
                        <div>
                            <h4 style="margin-bottom: 5px;">Strategia:</h4>
                            <p>{clean_html(DEGEN_TYPES[selected_type]["strategy"])}</p>
                        </div>
                    </div>
                    """,
                    key=f"compare_{selected_type}_card"
                )
            
            # Second type card (compared)
            with comp_cols[1 if num_columns > 1 else 0]:
                create_card(
                    title=comparison_type,
                    icon="👥",
                    content=f"""
                    <div style="padding: 10px 0;">
                        <div style="margin-bottom: 15px;">
                            <h4 style="margin-bottom: 5px;">Opis:</h4>
                            <p>{DEGEN_TYPES[comparison_type]['description']}</p>
                        </div>
                        
                        <div style="margin-bottom: 15px;">
                            <h4 style="margin-bottom: 5px;">Mocne strony:</h4>
                            <ul style="padding-left: 20px;">
                                {"".join([f"<li>✅ {strength}</li>" for strength in DEGEN_TYPES[comparison_type]["strengths"]])}
                            </ul>
                        </div>
                        
                        <div style="margin-bottom: 15px;">
                            <h4 style="margin-bottom: 5px;">Wyzwania:</h4>
                            <ul style="padding-left: 20px;">
                                {"".join([f"<li>⚠️ {challenge}</li>" for challenge in DEGEN_TYPES[comparison_type]["challenges"]])}
                            </ul>
                        </div>
                        
                        <div>
                            <h4 style="margin-bottom: 5px;">Strategia:</h4>
                            <p>{clean_html(DEGEN_TYPES[comparison_type]["strategy"])}</p>
                        </div>
                    </div>
                    """,
                    key=f"compare_{comparison_type}_card"
                )
    
    # Navigation buttons
    st.markdown("<hr style='margin: 2rem 0 1rem 0;'>", unsafe_allow_html=True)
    
    cols = create_grid(2)
    
    with cols[0]:
        if st.button("📋 Przejdź do testu typu degena", key="go_to_test", use_container_width=True):
            st.session_state.page = 'degen_test'
            st.rerun()
    
    with cols[1]:
        if st.button("🏠 Powrót do dashboardu", key="back_to_dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
