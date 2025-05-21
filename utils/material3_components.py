import streamlit as st
import os
from utils.layout import get_device_type, apply_responsive_styles

def load_extended_material3_css():
    """Ładuje rozszerzony zestaw stylów Material 3"""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "css", "material3_extended.css")
    
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"Nie można znaleźć pliku css: {css_path}")

def m3_button_styles():
    """Dodaje style przycisków Material 3 do interfejsu"""
    return st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    
    /* Material 3 Button Styles */
    .stButton button {
        background-color: #2196F3 !important;
        color: white !important;
        border-radius: 24px !important;
        font-family: 'Roboto', sans-serif !important;
        font-weight: 500 !important;
        padding: 10px 16px !important;
        border: none !important;
        box-shadow: 0 3px 5px rgba(33, 150, 243, 0.3) !important;
        transition: all 0.3s !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton button:hover {
        background-color: #1976D2 !important;
        box-shadow: 0 4px 8px rgba(33, 150, 243, 0.4) !important;
        transform: translateY(-1px) !important;
    }
    
    .stButton button:active {
        background-color: #0D47A1 !important;
        box-shadow: 0 2px 4px rgba(33, 150, 243, 0.3) !important;
        transform: translateY(1px) !important;
    }
    
    .stButton button:disabled {
        background-color: #BDBDBD !important;
        box-shadow: none !important;
        color: #757575 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def m3_lesson_card_styles():
    """Dodaje style kart lekcji Material 3 do interfejsu"""
    return st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    
    /* Material 3 Card Styles */
    .m3-lesson-card {
        background-color: white;
        color: #333;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
        transition: all 0.3s;
        position: relative;
        overflow: hidden;
        font-family: 'Roboto', sans-serif;
    }
    
    .m3-lesson-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #2196F3, #673AB7);
        opacity: 0.8;
    }
    
    .m3-lesson-card:hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.16);
        transform: translateY(-2px);
    }
    
    /* Responsywne style dla kart lekcji */
    @media (max-width: 640px) {
        .m3-lesson-card {
            padding: 16px;
            margin-bottom: 12px;
        }
        
        .m3-lesson-card h3 {
            font-size: 1.2rem;
            margin-bottom: 8px;
        }
        
        .m3-description {
            font-size: 14px;
            margin: 10px 0;
        }
        
        .m3-lesson-badges {
            gap: 6px;
            margin: 10px 0;
        }
        
        .m3-badge {
            padding: 4px 8px;
            font-size: 12px;
        }
    }
    
    .m3-lesson-card-completed::before {
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
    }
    
    .m3-card-content {
        position: relative;
    }
    
    .m3-lesson-card h3 {
        font-size: 1.5rem;
        font-weight: 500;
        margin-bottom: 16px;
        color: #1A237E;
    }
    
    .m3-lesson-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin: 16px 0;
    }
    
    .m3-badge {
        padding: 6px 12px;
        border-radius: 24px;
        font-size: 14px;
        font-weight: 500;
        color: white;
        display: inline-flex;
        align-items: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .m3-badge-xp {
        background-color: #FFD700;
        color: #333;
    }
    
    .m3-badge-category {
        background-color: #673AB7;
    }
    
    .m3-description {
        font-size: 16px;
        line-height: 1.5;
        color: #555;
        margin: 16px 0;
    }
    
    .m3-completion-status {
        font-size: 14px;
        font-weight: 500;
        color: #757575;
        margin-top: 16px;
        display: flex;
        align-items: center;
    }
    
    .m3-completed {
        color: #4CAF50;
    }
    
    .m3-completion-status::before {
        content: '';
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: #757575;
        margin-right: 8px;
    }
    
    .m3-completed::before {
        background-color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

def apply_material3_theme():
    """Aplikuje wszystkie style Material 3 w aplikacji"""
    # Ładuj rozszerzony zestaw stylów Material 3
    load_extended_material3_css()
    
    # Zastosuj style responsywne
    apply_responsive_styles()
    
    # Podstawowe style
    m3_button_styles()
    m3_lesson_card_styles()
    
    # Dodatkowe globalne style Material 3
    st.markdown("""
    <style>
    /* Global Material 3 styles */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }
    
    h1, h2, h3 {
        color: #1A237E;
        font-weight: 500;
    }
    
    /* Material 3 inspired animations */
    @keyframes m3-ripple {
        0% { transform: scale(0); opacity: 1; }
        100% { transform: scale(2); opacity: 0; }
    }
    
    .m3-animation-ripple {
        position: relative;
        overflow: hidden;
    }
    
    .m3-animation-ripple::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        transform: scale(0);
        animation: m3-ripple 0.6s;
        pointer-events: none;
    }
    
    /* Dodatkowe ulepszenia Material 3 */
    .streamlit-expanderHeader {
        border-radius: 12px !important;
        transition: background-color 0.3s;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: rgba(33, 150, 243, 0.08) !important;
    }
    
    /* Poprawa wyglądu pól tekstowych */
    .stTextInput > div > div > input {
        border-radius: 8px !important;
        border: 1px solid #E0E0E0 !important;
        padding: 10px 14px !important;
        transition: border-color 0.3s, box-shadow 0.3s !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2196F3 !important;
        box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2) !important;
    }
    
    /* Ulepszone selectboxy */
    .stSelectbox > div > div {
        border-radius: 8px !important;
        transition: border-color 0.3s, box-shadow 0.3s !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #BBBBBB !important;
    }
    
    .stSelectbox > div > div:focus {
        border-color: #2196F3 !important;
        box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2) !important;
    }
    
    /* Ulepszony wygląd zakładek */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0 !important;
        padding: 10px 16px !important;
        transition: background-color 0.3s !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(33, 150, 243, 0.1) !important;
        font-weight: 500 !important;
    }
    
    /* Animacje przejścia stron */
    .main .block-container {
        animation: fadeIn 0.5s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)

def m3_card(title, content, badge=None, icon=None):
    """Renderuje prostą kartę w stylu Material 3"""
    icon_html = f'<span style="font-size: 24px; margin-right: 12px;">{icon}</span>' if icon else ""
    badge_html = f'<div class="m3-badge" style="background-color: #673AB7; margin-left: auto;">{badge}</div>' if badge else ""
    
    card_html = f"""
    <div class="m3-lesson-card">
        <div class="m3-card-content">
            <div style="display: flex; align-items: center;">
                {icon_html}
                <h3 style="margin: 0; flex-grow: 1;">{title}</h3>
                {badge_html}
            </div>
            <p class="m3-description">{content}</p>
        </div>
    </div>
    """
    
    m3_lesson_card_styles()  # Upewnij się, że style są załadowane
    return st.markdown(card_html, unsafe_allow_html=True)

def m3_chip(label, icon=None, is_selected=False, color="#E0E0E0", text_color="#000000"):
    """Renderuje chip w stylu Material 3"""
    icon_html = f'<span style="margin-right: 6px;">{icon}</span>' if icon else ""
    selected_class = "m3-chip-selected" if is_selected else ""
    
    chip_html = f"""
    <style>
    .m3-chip {{
        display: inline-flex;
        align-items: center;
        height: 32px;
        padding: 0 12px;
        border-radius: 16px;
        background-color: {color};
        color: {text_color};
        font-size: 13px;
        font-weight: 500;
        margin: 4px;
        transition: background-color 0.3s;
    }}
    
    .m3-chip:hover {{
        filter: brightness(0.95);
    }}
    
    .m3-chip-selected {{
        background-color: #2196F3;
        color: white;
    }}
    </style>
    
    <span class="m3-chip {selected_class}">
        {icon_html}
        {label}
    </span>
    """
    
    return st.markdown(chip_html, unsafe_allow_html=True)

def m3_segmented_button(options, callback=None):
    """Tworzy przycisk segmentowany w stylu Material 3"""
    if "m3_segmented_selected" not in st.session_state:
        st.session_state.m3_segmented_selected = 0
    
    st.markdown("""
    <style>
    .m3-segmented-container {
        display: flex;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        margin: 8px 0;
    }
    
    .m3-segment {
        flex: 1;
        text-align: center;
        padding: 8px 12px;
        background-color: white;
        cursor: pointer;
        transition: background-color 0.3s, color 0.3s;
        border-right: 1px solid rgba(0,0,0,0.1);
        font-family: 'Roboto', sans-serif;
        font-size: 14px;
    }
    
    .m3-segment:last-child {
        border-right: none;
    }
    
    .m3-segment:hover {
        background-color: rgba(33, 150, 243, 0.1);
    }
    
    .m3-segment-selected {
        background-color: #2196F3 !important;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    cols = st.columns(len(options))
    for i, (col, option) in enumerate(zip(cols, options)):
        with col:
            button_key = f"m3_segment_{i}"
            selected_class = "m3-segment-selected" if st.session_state.m3_segmented_selected == i else ""
            
            if st.button(option, key=button_key):
                st.session_state.m3_segmented_selected = i
                if callback:
                    callback(i)
            
            # Dodaj klasę stylu do przycisku
            st.markdown(f"""
            <script>
                const button = document.querySelector('button[kind="secondary"][data-testid="{button_key}"]');
                if (button) {{
                    button.classList.add('m3-segment');
                    button.classList.add('{selected_class}');
                }}
            </script>
            """, unsafe_allow_html=True)
    
    return st.session_state.m3_segmented_selected

def m3_text_field(label, value="", key=None, type="text", help=None):
    """Renderuje pole tekstowe w stylu Material 3"""
    field_key = key or f"m3_text_field_{label}"
    
    st.markdown(f"""
    <style>
    .m3-text-field {{
        position: relative;
        margin-bottom: 16px;
        padding-top: 16px;
    }}
    
    .m3-text-field input {{
        width: 100%;
        padding: 12px 16px;
        font-size: 16px;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        background-color: transparent;
        transition: border-color 0.3s, box-shadow 0.3s;
    }}
    
    .m3-text-field input:focus {{
        outline: none;
        border-color: #2196F3;
        box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
    }}
    
    .m3-text-field label {{
        position: absolute;
        left: 16px;
        top: 0;
        font-size: 12px;
        color: #757575;
    }}
    
    .m3-text-field-help {{
        font-size: 12px;
        color: #757575;
        margin-top: 4px;
    }}
    </style>
    
    <div class="m3-text-field">
        <label for="{field_key}">{label}</label>
    </div>
    """, unsafe_allow_html=True)
    
    if type == "password":
        result = st.text_input("", key=field_key, type="password")
    else:
        result = st.text_input("", key=field_key)

    if value:  # Jeśli wartość jest określona, ustaw ją po inicjalizacji
        st.session_state[field_key] = value
    
    if help:
        st.markdown(f'<div class="m3-text-field-help">{help}</div>', unsafe_allow_html=True)
    
    return result

def m3_avatar(image_url=None, text=None, size=40, bg_color="#2196F3"):
    """Renderuje awatar w stylu Material 3"""
    if not image_url and not text:
        text = "U"
    
    if text and len(text) > 2:
        text = text[:2]
    
    avatar_html = f"""
    <style>
    .m3-avatar {{
        width: {size}px;
        height: {size}px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: {size//2.5}px;
        font-weight: 500;
        color: white;
        background-color: {bg_color};
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }}
    </style>
    
    <div class="m3-avatar">
    """
    
    if image_url:
        avatar_html += f'<img src="{image_url}" width="{size}" height="{size}" style="object-fit: cover;">'
    else:
        avatar_html += f'{text}'
    
    avatar_html += "</div>"
    
    return st.markdown(avatar_html, unsafe_allow_html=True)
