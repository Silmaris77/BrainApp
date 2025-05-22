import streamlit as st
from PIL import Image
from data.neuroleader_types import NEUROLEADER_TYPES
from data.neuroleader_details import neuroleader_details
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

def show_neuroleader_explorer():
    """
    Wyświetla stronę umożliwiającą eksplorację wszystkich typów neuroliderów
    wraz z ich szczegółowymi opisami.
    """
    # Zastosuj style Material 3
    
    # Load card layout CSS
    load_card_layout()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    zen_header("Odkrywanie Typów Neuroliderów")
    
    # Wprowadzenie do typów neuroliderów
    zen_section(
        "Poznaj różne style przywództwa neurobiologicznego", 
        "Każdy neurolider ma unikalne podejście do przewodzenia zespołowi", 
        "🔍"
    )
    
    st.markdown("""
    Każdy typ neuroliderera ma unikalne podejście do przewodzenia zespołowi, uwarunkowane cechami osobowości,
    wzorcami aktywności mózgu, emocjami i strategiami działania. Odkryj różne style przywództwa i ich neurobiologiczne podstawy.
    """)
    
    # Przycisk do testu
    col1, col2 = st.columns([3, 1])
    with col2:
        if zen_button("📋 Wykonaj test", key="go_to_test", use_container_width=True):
            st.session_state.page = 'neuroleader_test'
            st.rerun()
    
    # Display neuroleader types in a card grid
    st.markdown("### Typy Neuroliderów")
    
    # Create a grid based on device type
    num_columns = 1 if device_type == 'mobile' else 2
    columns = create_grid(num_columns)
    
    # Display each neuroleader type in a card
    for i, (type_name, type_data) in enumerate(NEUROLEADER_TYPES.items()):
        col_idx = i % len(columns)
        
        with columns[col_idx]:
            # Create card with neuroleader type info
            create_card(
                title=type_name,
                icon="🧠",
                content=f"""
                <div style="padding: 10px 0;">
                    <p style="color: {type_data['color']}; font-weight: 500;">{type_data['description']}</p>
                    
                    <h4>Mocne strony:</h4>
                    <ul>
                        {"".join([f"<li>✅ {strength}</li>" for strength in type_data['strengths'][:3]])}
                    </ul>
                    
                    <h4>Wyzwania:</h4>
                    <ul>
                        {"".join([f"<li>⚠️ {challenge}</li>" for challenge in type_data['challenges'][:3]])}
                    </ul>
                </div>
                """,
                footer_content=f"""
                <button class="zen-button" id="btn-details-{type_name.replace(' ', '-')}">Szczegóły</button>
                """,
                key=f"type_{type_name.replace(' ', '_')}",
                on_click=lambda type_name=type_name: st.session_state.update({
                    'selected_neuroleader_type': type_name,
                    'show_neuroleader_details': True
                })
            )
    
    # Display detailed information for selected type
    if st.session_state.get('show_neuroleader_details', False):
        selected_type = st.session_state.get('selected_neuroleader_type')
        
        if selected_type in NEUROLEADER_TYPES:
            type_data = NEUROLEADER_TYPES[selected_type]
            
            st.markdown("---")
            zen_section(
                f"Szczegółowa analiza: {selected_type}", 
                "Poznaj dokładnie cechy, mocne strony i wyzwania tego typu neuroliderera", 
                "📊"
            )
            
            # Main info card
            create_card(
                title=f"{selected_type}",
                icon="🧠",
                content=f"""
                <div style="padding: 10px 0;">
                    <p style="color: {type_data['color']}; font-weight: 500; font-size: 1.1rem;">{type_data['description']}</p>
                </div>
                """,
                key="selected_type_main_card"
            )
            
            # Strengths and challenges in two columns
            col1, col2 = st.columns(2) if device_type != 'mobile' else [st.container(), st.container()]
            
            with col1:
                create_card(
                    title="Mocne strony",
                    icon="💪",
                    content=f"""
                    <ul>
                        {"".join([f"<li>✅ {strength}</li>" for strength in type_data['strengths']])}
                    </ul>
                    """,
                    key="selected_type_strengths"
                )
            
            with col2:
                create_card(
                    title="Wyzwania",
                    icon="🚧",
                    content=f"""
                    <ul>
                        {"".join([f"<li>⚠️ {challenge}</li>" for challenge in type_data['challenges']])}
                    </ul>
                    """,
                    key="selected_type_challenges"
                )
            
            # Strategy card
            create_card(
                title="Rekomendowana strategia",
                icon="🎯",
                content=f"""
                <div style="padding: 10px 0;">
                    <p>{clean_html(type_data['strategy'])}</p>
                </div>
                """,
                key="selected_type_strategy"
            )
            
            # Detailed description if available
            if selected_type in neuroleader_details:
                with st.expander("Szczegółowy opis neurobiologiczny", expanded=False):
                    st.markdown(neuroleader_details[selected_type])
            
            # Button to clear selection
            if zen_button("← Powrót do wszystkich typów", key="back_to_all_types"):
                st.session_state.pop('selected_neuroleader_type', None)
                st.session_state.pop('show_neuroleader_details', None)
                st.rerun()
    
    # Navigation buttons at the bottom
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if zen_button("📋 Przejdź do testu typu neuroliderera", key="go_to_test_bottom", use_container_width=True):
            st.session_state.page = 'neuroleader_test'
            st.rerun()
    
    with col2:
        if zen_button("🏠 Powrót do dashboardu", key="back_to_dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
