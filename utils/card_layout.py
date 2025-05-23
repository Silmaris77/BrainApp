import streamlit as st
from config.settings import CARD_LAYOUT_CONFIG

def load_card_layout():
    """Load the card layout CSS."""
    with open("static/css/card_layout.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        
    # Apply dynamic styling based on configuration
    primary_color = CARD_LAYOUT_CONFIG.get("primary_color", "#4CAF50")
    
    # Add dynamic CSS variables
    st.markdown(f"""
    <style>
    :root {{
        --primary-color: {primary_color};
        --card-shadow: {CARD_LAYOUT_CONFIG.get("card_shadow", "0 2px 8px rgba(0,0,0,0.08)")};
        --card-hover-shadow: {CARD_LAYOUT_CONFIG.get("card_hover_shadow", "0 4px 12px rgba(0,0,0,0.12)")};
        --card-border-radius: {CARD_LAYOUT_CONFIG.get("card_border_radius", "8px")};
        --card-padding: {CARD_LAYOUT_CONFIG.get("card_padding", "1.5rem")};
    }}
    </style>
    """, unsafe_allow_html=True)

def create_card(title, content, icon=None, footer_content=None, key=None, on_click=None):
    """
    Create a card component with optional icon and footer.
    
    Parameters:
    - title: The card title
    - content: HTML or markdown content for the card body
    - icon: Emoji or icon to display in the header (optional)
    - footer_content: HTML content for the footer (optional)
    - key: Unique key for the card container
    - on_click: Function to call when the card is clicked
    
    Returns:
    - The card container for further customization
    """
    card_container = st.container(key=key)
    
    with card_container:
        st.markdown(f"""
        <div class="zen-card" id="card-{key}">
            <div class="zen-card-header">
                {f'<span class="icon">{icon}</span>' if icon else ''}
                {title}
            </div>
            <div class="zen-card-content">
                {content}
            </div>
            {f'<div class="zen-card-footer">{footer_content}</div>' if footer_content else ''}
        </div>
        """, unsafe_allow_html=True)
        
        if on_click:
            # Add JavaScript to make the entire card clickable
            st.markdown(f"""
            <script>
                document.getElementById("card-{key}").addEventListener("click", function() {{
                    // Trigger the click event on a Streamlit button
                    document.getElementById("btn-{key}").click();
                }});
            </script>
            """, unsafe_allow_html=True)
            
            # Hidden button to handle the click

            st.button("", key=f"btn-{key}", on_click=on_click, help="")
    
    return card_container

def create_grid(num_columns=2):
    """
    Creates a grid layout for cards.
    Since Streamlit doesn't fully support CSS grid, we use columns.
    
    Parameters:
    - num_columns: Number of columns in the grid
    
    Returns:
    - List of column objects that can be used to place cards
    """
    columns = st.columns(num_columns)
    return columns

def zen_section(title, description=None, icon=None):
    """Create a styled section header."""
    if icon:
        title = f"{icon} {title}"
        
    st.markdown(f"## {title}")
    
    if description:
        st.markdown(f"<p style='color: #666; margin-bottom: 1.5rem;'>{description}</p>", 
                   unsafe_allow_html=True)
    
    return st.container()

def data_panel(content, title=None, border_color=None):
    """Create a styled panel for data display."""
    style = f"border-left: 3px solid {border_color};" if border_color else ""
    
    st.markdown(f"""
    <div class="data-container" style="{style}">
        {f"<h4>{title}</h4>" if title else ""}
        {content}
    </div>
    """, unsafe_allow_html=True)

def responsive_layout(content_func):
    """
    Decorator that provides device-aware rendering to a view function.
    Will adjust layout based on screen size.
    
    Usage:
    @responsive_layout
    def show_my_view():
        # View implementation
    """
    def wrapper(*args, **kwargs):
        # Check if we're on mobile
        # This requires custom JavaScript via st.components.v1.html
        # For this implementation we'll just use a simple session state flag
        is_mobile = st.session_state.get('is_mobile', False)
        
        # You could add a toggle for testing
        if st.session_state.get('dev_mode', False):
            is_mobile = st.checkbox("Mobile View", value=is_mobile)
            st.session_state.is_mobile = is_mobile
        
        # Set session state for the content function to use
        st.session_state.layout_columns = 1 if is_mobile else 2
        
        # Call the original function
        return content_func(*args, **kwargs)
    
    return wrapper
