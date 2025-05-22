import streamlit as st
import json
from utils.card_layout import create_card, create_grid_container, apply_card_layout
from utils.components import zen_header
from utils.session import get_user_data

# Instead of importing categories directly, import the whole module
import views.skills_new as skills_module

def show_skill_tree():
    # Apply card layout styling
    apply_card_layout()
    
    # Get user data
    user_data = get_user_data()
    user_skills = user_data.get('skills', {})
    
    # Display header
    zen_header("Mapa Rozwoju Neuroliderów 🧠")
    
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
    
    # Create a grid container for the blocks
    with create_grid_container(columns=3):
        for block_id, block in blocks.items():
            # Get categories for this block
            block_categories = [c for c_id, c in skills_module.get_categories().items() if c['block'] == block_id]
            completed_in_block = sum(user_skills.get(c['id'], {}).get('level', 0) for c in block_categories)
            total_in_block = len(block_categories) * 10  # Each category has 10 levels
            progress = int((completed_in_block / total_in_block) * 100) if total_in_block > 0 else 0
            
            create_card(
                title=f"{block['icon']} {block['name']}",
                content=f"""
                <div style="margin-bottom:10px;">Moduły: {len(block_categories)}</div>
                <div class="progress-bar-container">
                    <div class="progress-bar" style="width:{progress}%; background-color:{block['color']}"></div>
                </div>
                <div style="text-align:right; margin-top:5px;">{progress}% ukończone</div>
                """,
                color=block['color'],
                on_click=None
            )
    
    # Display categories for each block
    for block_id, block in blocks.items():
        st.markdown(f"""
        <h3 style="color:{block['color']}; margin-top:30px;">{block['icon']} {block['name']}</h3>
        """, unsafe_allow_html=True)
        
        # Create a grid container for the categories in this block
        with create_grid_container(columns=2):
            # Get categories for this block from the skills_module instead
            block_categories = {c_id: c for c_id, c in skills_module.get_categories().items() if c['block'] == block_id}
            
            for category_id, category in block_categories.items():
                # Calculate progress for this category
                level = user_skills.get(category['id'], {}).get('level', 0)
                progress = int((level / category['max_level']) * 100) if category['max_level'] > 0 else 0
                
                # Create a card for the category
                create_card(
                    title=f"{category['icon']} {category['name']}",
                    content=f"""
                    <div style="margin-bottom:10px;">{category['description']}</div>
                    <div class="progress-bar-container">
                        <div class="progress-bar" style="width:{progress}%; background-color:{block['color']}"></div>
                    </div>
                    <div style="text-align:right; margin-top:5px;">Poziom {level}/{category['max_level']}</div>
                    """,
                    color=block['color'],
                    on_click=lambda c_id=category_id: show_category_details(c_id)
                )

def show_category_details(category_id):
    # This would be implemented to show lessons for a category when a card is clicked
    st.session_state.selected_category = category_id
    st.session_state.page = 'lesson'
    st.rerun()
