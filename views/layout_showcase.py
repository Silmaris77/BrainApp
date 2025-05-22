import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils.components import zen_header
from utils.card_layout import load_card_layout, create_card, create_grid, zen_section, data_panel
from utils.material3_components import apply_material3_theme
from utils.layout import get_device_type
from config.settings import CARD_LAYOUT_CONFIG

def show_layout_showcase():
    """
    Showcase page demonstrating all card layout components with documentation.
    This page serves as both documentation and a testing ground for the Card-Based Grid + Sidebar layout.
    """
    # Apply Material 3 theme
    apply_material3_theme()
    
    # Load card layout CSS
    load_card_layout()
    
    # Header
    zen_header("Card Layout Showcase")
    
    # Introduction
    st.markdown("""
    # Card-Based Grid + Sidebar Layout
    
    This page demonstrates all components and styles available in the Card-Based Grid + Sidebar layout system
    designed specifically for the Neuroliderzy application targeting managers and experienced professionals.
    
    The layout combines elements of:
    - **Flat Design**: Clean, minimal aesthetic
    - **Material Design**: Elevation, transitions, and consistent components
    - **Card-Based UI**: Content organized in distinct cards
    - **Responsive Grid**: Adapts to different screen sizes
    
    ## Current Configuration
    """)
    
    # Display current configuration
    st.json(CARD_LAYOUT_CONFIG)
    
    # Sections showcase
    zen_section(
        "Section Headers", 
        "Zen sections provide clear visual structure to your page", 
        "📚"
    )
    
    st.markdown("""
    Section headers help organize content into logical groups. They include:
    - A primary title
    - An optional subtitle/description
    - An optional icon
    
    **Usage:**
    ```python
    zen_section("Section Title", "Optional description", "Optional icon")
    ```
    """)
    
    # Card showcase
    zen_section(
        "Cards", 
        "The core building blocks of the layout", 
        "🃏"
    )
    
    # Basic card example
    create_card(
        title="Basic Card",
        icon="📝",
        content="""
        <p>This is a basic card with title, content, and an icon.</p>
        <p>Cards provide a clean, contained way to present information.</p>
        """,
        key="basic_card"
    )
    
    # Show code example
    st.code("""
    create_card(
        title="Basic Card",
        icon="📝",
        content=\"\"\"
        <p>This is a basic card with title, content, and an icon.</p>
        <p>Cards provide a clean, contained way to present information.</p>
        \"\"\",
        key="basic_card"
    )
    """, language="python")
    
    # Card with footer
    create_card(
        title="Card with Footer",
        icon="👣",
        content="""
        <p>This card includes a footer section with buttons or actions.</p>
        <p>Footers are useful for adding actions related to the card content.</p>
        """,
        footer_content="""
        <button class="zen-button">Primary Action</button>
        <button class="zen-button secondary">Secondary</button>
        """,
        key="footer_card"
    )
    
    # Interactive card
    create_card(
        title="Interactive Card",
        icon="🖱️",
        content="""
        <p>This entire card is clickable and will trigger an action.</p>
        <p>Click anywhere on this card to see the effect.</p>
        """,
        key="interactive_card",
        on_click=lambda: st.session_state.update({"card_clicked": True})
    )
    
    if st.session_state.get("card_clicked", False):
        st.success("Card was clicked!")
        if st.button("Reset"):
            st.session_state.pop("card_clicked")
            st.rerun()
    
    # Grid layout showcase
    zen_section(
        "Grid Layout", 
        "Organize cards in responsive grids", 
        "📏"
    )
    
    st.markdown("""
    Grid layouts automatically adjust based on screen size:
    - Desktop: Multiple columns
    - Mobile: Single column
    
    **Usage:**
    ```python
    columns = create_grid(num_columns=2)
    with columns[0]:
        create_card(...)
    with columns[1]:
        create_card(...)
    ```
    """)
    
    # Create a grid demonstration
    device_type = get_device_type()
    num_columns = 1 if device_type == 'mobile' else 3
    columns = create_grid(num_columns)
    
    for i in range(3):
        with columns[i % len(columns)]:
            create_card(
                title=f"Grid Card {i+1}",
                icon="🔢",
                content=f"<p>This is card {i+1} in the grid demonstration.</p>",
                key=f"grid_card_{i}"
            )
    
    # Data presentation
    zen_section(
        "Data Presentation", 
        "Specialized components for data visualization", 
        "📊"
    )
    
    # Create a sample dataframe
    df = pd.DataFrame(
        np.random.randn(5, 3),
        columns=['A', 'B', 'C']
    )
    
    # Create a chart
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(df.index, df['A'], label='A')
    ax.bar(df.index, df['B'], bottom=df['A'], label='B')
    ax.bar(df.index, df['C'], bottom=df['A'] + df['B'], label='C')
    ax.legend()
    ax.set_title('Sample Stacked Bar Chart')
    
    # Data panel with chart
    data_panel(
        f"""
        <h3>Sales Performance</h3>
        <p>This panel shows data with a styled border and background.</p>
        """,
        title="Quarterly Results",
        border_color="#4CAF50"
    )
    
    # Display the chart
    st.pyplot(fig)
    
    # Typography and colors
    zen_section(
        "Typography & Colors", 
        "Consistent text styling and color usage", 
        "🎨"
    )
    
    st.markdown("""
    ### Heading 3
    #### Heading 4
    ##### Heading 5
    
    Regular paragraph text with **bold emphasis** and *italic text* for visual hierarchy.
    
    - List item one
    - List item two
    - List item three
    
    > Blockquote for highlighted information or quotes
    """)
    
    # Display color palette
    st.markdown("### Color Palette")
    
    cols = st.columns(5)
    colors = ["#4CAF50", "#2196F3", "#FFC107", "#9C27B0", "#F44336"]
    names = ["Primary", "Info", "Warning", "Accent", "Error"]
    
    for i, (col, color, name) in enumerate(zip(cols, colors, names)):
        with col:
            st.markdown(f"""
            <div style="background-color: {color}; height: 50px; border-radius: 4px; color: white; 
                        display: flex; align-items: center; justify-content: center; margin-bottom: 5px;">
                {name}
            </div>
            <code>{color}</code>
            """, unsafe_allow_html=True)
            
    # Best practices
    zen_section(
        "Best Practices", 
        "Guidelines for using this layout system", 
        "✅"
    )
    
    st.markdown("""
    ### Do's:
    - Group related information in cards
    - Use consistent styling across cards
    - Include clear call-to-action buttons
    - Ensure adequate spacing between elements
    - Use the grid system for organizing content
    
    ### Don'ts:
    - Overcrowd cards with too much information
    - Mix too many different design styles
    - Use too many colors or fonts
    - Create cards without clear purpose
    - Neglect mobile responsiveness
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
    Card-Based Grid + Sidebar Layout for Neuroliderzy App • 
    Designed for professional manager-focused applications
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_layout_showcase()
