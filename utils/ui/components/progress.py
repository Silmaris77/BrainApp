import streamlit as st

def progress_bar(progress, text=None, color="#4CAF50"):
    """
    Display a custom styled progress bar.
    
    Args:
        progress: Percentage value (0-100)
        text: Optional text to display with the progress bar
        color: Color of the progress bar
    """
    # Ensure progress is within bounds
    progress = max(0, min(100, progress))
    
    # Style for the progress container
    container_style = f"""
        display: flex;
        flex-direction: column;
        width: 100%;
        margin: 0.5rem 0 1rem 0;
    """
    
    # Style for the progress bar
    progress_style = f"""
        width: 100%;
        height: 10px;
        background-color: #e0e0e0;
        border-radius: 5px;
        overflow: hidden;
    """
    
    # Style for the progress indicator
    indicator_style = f"""
        width: {progress}%;
        height: 100%;
        background-color: {color};
        border-radius: 5px;
        transition: width 0.5s ease;
    """
    
    # Text style
    text_style = """
        font-size: 0.9rem;
        color: #555;
        margin-bottom: 0.3rem;
    """
    
    # HTML for the progress component
    html = f"""
    <div style='{container_style}'>
    """
    
    # Add text if provided
    if text:
        html += f"<div style='{text_style}'>{text}</div>"
    
    # Add the progress bar
    html += f"""
        <div style='{progress_style}'>
            <div style='{indicator_style}'></div>
        </div>
    </div>
    """
    
    # Render the HTML
    st.markdown(html, unsafe_allow_html=True)
    
    return progress
