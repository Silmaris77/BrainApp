import streamlit as st
from PIL import Image
from data.neuroleader_types import NEUROLEADER_TYPES
from data.neuroleader_details import neuroleader_details
from utils.ui import initialize_ui
from utils.ui.components.interactive import zen_button, notification
from utils.ui.components.text import content_section, zen_header, quote_block, tip_block
from utils.ui.layouts.grid import responsive_grid, responsive_container
from utils.ui.layouts.responsive import get_device_type
import re

def clean_html(text):
    """Removes all HTML tags from text and normalizes whitespace"""
    # First remove all HTML tags
    text_without_tags = re.sub(r'<.*?>', '', text)
    # Normalize whitespace (replace multiple spaces, tabs, newlines with single space)
    normalized_text = re.sub(r'\s+', ' ', text_without_tags)
    return normalized_text.strip()

def show_neuroleader_explorer():
    """
    Display the page for exploring all neuroleader types
    with their detailed descriptions.
    """
    # Initialize UI
    initialize_ui()
    
    # Header
    zen_header("Odkrywanie Typów Neuroliderów", "Poznaj różne style przywództwa")
    
    st.markdown("## Poznaj różne style przywództwa neurobiologicznego")
    # Introduction to neuroleader types
    st.markdown("""
    Każdy typ neuroliderera ma unikalne podejście do przewodzenia zespołowi, uwarunkowane cechami osobowości,
    wzorcami aktywności mózgu, emocjami i strategiami działania. Odkryj różne style przywództwa i ich neurobiologiczne podstawy.
    """)
        
        # Button for taking the test
    if st.session_state.get('tests', {}).get('neuroleader', {}).get('type'):
        user_type = st.session_state.get('tests', {}).get('neuroleader', {}).get('type')
        st.info(f"Twój typ Neuroliderera: **{user_type}**")
    else:
        if zen_button("Wykonaj test i odkryj swój typ", key="go_to_test_button"):
            st.session_state.page = "neuroleader_test"
            st.rerun()
    
    # Types selection
    st.markdown("## Wybierz typ do eksploracji")
    # Create tabs for all neuroleader types
    tabs = st.tabs(NEUROLEADER_TYPES)
    
    # Display content for each type
    for i, neuroleader_type in enumerate(NEUROLEADER_TYPES):
        with tabs[i]:
            show_neuroleader_type_details(neuroleader_type)

def show_neuroleader_type_details(neuroleader_type):
    """
    Display detailed information about a specific neuroleader type
    
    Args:
        neuroleader_type: The neuroleader type to display
    """
    if neuroleader_type in neuroleader_details:
        type_details = neuroleader_details[neuroleader_type]
        
        # Sprawdź, czy type_details jest słownikiem
        if isinstance(type_details, dict):
            # Main description section
            st.markdown(f"## {type_details.get('name', neuroleader_type)}")
            
            # Two-column layout for desktop/tablet
            cols = responsive_grid(2, mobile_cols=1)
            
            # Left column - description and strengths
            with cols[0]:
                st.markdown("### Opis")
                st.markdown(type_details.get('description', 'Brak opisu'))
                
                st.markdown("### Mocne strony")
                for strength in type_details.get('strengths', []):
                    st.markdown(f"- {clean_html(strength)}")
                
                st.markdown("### Wyzwania")
                for challenge in type_details.get('challenges', []):
                    st.markdown(f"- {clean_html(challenge)}")
            
            # Right column - leadership style, team dynamics, quote
            with cols[1]:
                st.markdown("### Styl przywództwa")
                st.markdown(type_details.get('leadership_style', 'Brak informacji'))
                
                st.markdown("### Dynamika zespołu")
                st.markdown(type_details.get('team_dynamics', 'Brak informacji'))
                
                # Quote
                if 'quote' in type_details and type_details['quote']:
                    with quote_block():
                        st.markdown(f"*\"{type_details['quote']}\"*")
                        if 'quote_author' in type_details and type_details['quote_author']:
                            st.markdown(f"— {type_details['quote_author']}")
            
            # Tips section
            st.markdown("### Wskazówki rozwojowe")
            with tip_block():
                st.markdown(type_details.get('development_tips', 'Brak wskazówek'))
            
            # Compatibility section
            st.markdown("### Kompatybilność z innymi typami")
            compatibility_cols = responsive_grid(len(NEUROLEADER_TYPES), mobile_cols=2)
            
            for i, other_type in enumerate(NEUROLEADER_TYPES):
                with compatibility_cols[i]:
                    if other_type == neuroleader_type:
                        st.markdown(f"**{other_type}**")
                        st.markdown("*To Ty!*")
                    else:
                        compatibility = type_details.get('compatibility', {}).get(other_type, "Brak danych")
                        st.markdown(f"**{other_type}**")
                        st.markdown(f"{compatibility}")
        else:
            # Jeśli type_details jest stringiem, po prostu go wyświetl
            st.markdown(f"## {neuroleader_type}")
            st.markdown(type_details)
    else:
        st.error(f"Nie znaleziono informacji dla typu {neuroleader_type}")

if __name__ == "__main__":
    # Test the module
    show_neuroleader_explorer()
