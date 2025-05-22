import streamlit as st
import json
from utils.ui import initialize_ui
from utils.ui.components.interactive import zen_button, notification
from utils.ui.components.text import zen_header, content_section
from utils.ui.layouts.grid import responsive_grid, render_dashboard_header
from utils.session import get_user_data

# Importuj moduł skills_new tak samo jak w oryginalnym pliku
import views.skills_new as skills_module

def show_skill_tree():
    """
    Wyświetla drzewo umiejętności używając nowego systemu UI zgodnego z CSP
    """
    # Inicjalizacja UI
    initialize_ui()
    
    # Get user data
    user_data = get_user_data()
    user_skills = user_data.get('skills', {})
    
    # Nagłówek
    render_dashboard_header("Mapa Rozwoju Neuroliderów 🧠")
    
    # Introduction text
    st.markdown("""
    Rozwijaj swoje umiejętności neuroliderskie poprzez ukończenie lekcji w każdym module.
    Każdy moduł zawiera 10 lekcji zaprojektowanych, aby pomóc Ci stać się lepszym liderem.
    """)
    
    # Define blocks with colors (using the same blocks as in the original file)
    blocks = {
        1: {"name": "Neurobiologia przywództwa", "color": "#3498db", "icon": "🧠"},
        2: {"name": "Procesy decyzyjne lidera", "color": "#e74c3c", "icon": "⚖️"},
        3: {"name": "Psychologia i motywacja w przywództwie", "color": "#2ecc71", "icon": "🌍"},
        4: {"name": "Praktyczne aspekty neuroprzywództwa", "color": "#f39c12", "icon": "💪"},
        5: {"name": "Przyszłość neuroprzywództwa", "color": "#9b59b6", "icon": "🌍"}
    }
    
    # Display the blocks in a grid
    st.subheader("Bloki tematyczne")
    
    # Używamy responsywnej siatki zamiast create_grid_container
    block_cols = responsive_grid(columns_desktop=3, columns_tablet=2, columns_mobile=1)
    
    # Wyświetl bloki w siatce
    for i, (block_id, block) in enumerate(blocks.items()):
        # Oblicz postęp dla tego bloku
        block_categories = []
        for c_id, c in skills_module.get_categories().items():
            if c['block'] == block_id:
                # Dodaj klucz 'id' do kategorii
                category = c.copy()
                category['id'] = c_id
                block_categories.append(category)
        
        completed_in_block = sum(user_skills.get(c['id'], {}).get('level', 0) for c in block_categories)
        total_in_block = len(block_categories) * 10  # Each category has 10 levels
        progress = int((completed_in_block / total_in_block) * 100) if total_in_block > 0 else 0
        
        with block_cols[i % len(block_cols)]:
            # Wyświetl blok jako kartę
            st.markdown(f"""
            <div style="padding: 20px; background-color: rgba(255, 255, 255, 0.05); border-radius: 10px; margin-bottom: 15px; border-left: 5px solid {block['color']};">
                <h3 style="color: {block['color']};">{block['icon']} {block['name']}</h3>
                <div style="margin-bottom:10px;">Moduły: {len(block_categories)}</div>
                <div style="width: 100%; background-color: rgba(255, 255, 255, 0.1); border-radius: 5px; height: 10px; margin: 10px 0;">
                    <div style="width: {progress}%; background-color: {block['color']}; height: 10px; border-radius: 5px;"></div>
                </div>
                <div style="text-align:right, margin-top:5px;">{progress}% ukończone</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Wyświetl kategorie dla każdego bloku
    for block_id, block in blocks.items():
        st.markdown(f"""
        <h3 style="color:{block['color']}; margin-top:30px;">{block['icon']} {block['name']}</h3>
        """, unsafe_allow_html=True)
        
        # Używamy responsywnej siatki
        category_cols = responsive_grid(columns_desktop=2, columns_tablet=1, columns_mobile=1)
        
        # Get categories for this block from the skills_module
        block_categories = {}
        for c_id, c in skills_module.get_categories().items():
            if c['block'] == block_id:
                category = c.copy()
                category['id'] = c_id  # Dodaj klucz 'id'
                block_categories[c_id] = category
        
        # Rozmieść kategorie w kolumnach
        for i, (category_id, category) in enumerate(block_categories.items()):
            # Calculate progress for this category
            level = user_skills.get(category['id'], {}).get('level', 0)
            # Używamy metody get() z wartością domyślną 10 dla 'max_level'
            max_level = category.get('max_level', 10)  # Domyślnie 10 poziomów
            progress = int((level / max_level) * 100) if max_level > 0 else 0
            
            with category_cols[i % len(category_cols)]:
                # Wyświetl kategorię jako kartę
                st.markdown(f"""
                <div style="padding: 20px; background-color: rgba(255, 255, 255, 0.05); border-radius: 10px; margin-bottom: 15px; border-left: 5px solid {block['color']};">
                    <h3>{category['icon']} {category['name']}</h3>
                    <p>{category['description']}</p>
                    <div style="width: 100%; background-color: rgba(255, 255, 255, 0.1); border-radius: 5px; height: 10px; margin: 10px 0;">
                        <div style="width: {progress}%; background-color: {block['color']}; height: 10px; border-radius: 5px;"></div>
                    </div>
                    <div style="text-align:right, margin-top:5px;">Poziom {level}/{max_level}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Przycisk przejścia do lekcji kategorii
                if zen_button(f"Przeglądaj lekcje", key=f"view_category_{category_id}"):
                    show_category_details(category_id)

def show_category_details(category_id):
    """
    Przejście do lekcji dla wybranej kategorii
    """
    # Ta sama funkcjonalność jak w oryginalnym pliku
    st.session_state.selected_category = category_id
    st.session_state.page = 'lesson'
    st.rerun()
