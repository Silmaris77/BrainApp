import streamlit as st

def create_grid_container(columns=3):
    """
    Tworzy kontener z podziałem na kolumny.
    
    Parametry:
    - columns: Liczba kolumn w kontenerze
    
    Zwraca:
    - lista: Lista obiektów kolumn
    """
    return st.columns(columns)

def render_dashboard_header(title, subtitle=None):
    """
    Renderuje nagłówek dashboardu.
    
    Parametry:
    - title: Tytuł dashboardu
    - subtitle: Podtytuł dashboardu (opcjonalny)
    """
    from utils.ui.components.text import zen_header
    zen_header(title, subtitle)

def render_stats_section(stats_data):
    """
    Renderuje sekcję statystyk.
    
    Parametry:
    - stats_data: Lista krotek (icon, value, label)
    """
    from utils.ui.components.cards import stat_card
    
    st.markdown("<div class='stats-section'>", unsafe_allow_html=True)
    
    cols = st.columns(len(stats_data))
    for i, (icon, value, label) in enumerate(stats_data):
        with cols[i]:
            stat_card(icon, value, label)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_two_column_layout(left_content, right_content, left_width=1, right_width=1):
    """
    Renderuje układ dwukolumnowy.
    
    Parametry:
    - left_content: Funkcja renderująca zawartość lewej kolumny
    - right_content: Funkcja renderująca zawartość prawej kolumny
    - left_width: Szerokość lewej kolumny
    - right_width: Szerokość prawej kolumny
    """
    col1, col2 = st.columns([left_width, right_width])
    
    with col1:
        left_content()
    
    with col2:
        right_content()

def get_device_type():
    """
    Wykrywa typ urządzenia na podstawie szerokości ekranu.
    
    Zwraca:
    - str: 'mobile', 'tablet' lub 'desktop'
    """
    # Pobieramy informacje o sesji i szerokości ekranu
    session = st.session_state
    
    # Domyślnie zakładamy desktop, chyba że w sesji jest ustawiony inny typ urządzenia
    device_type = session.get('device_type', 'desktop')
    
    return device_type

def responsive_container(content_function):
    """
    Tworzy responsywny kontener i wywołuje w nim funkcję renderującą zawartość.
    
    Parametry:
    - content_function: Funkcja renderująca zawartość
    
    Zwraca:
    - Rezultat wywołania content_function
    """
    device_type = get_device_type()
    
    with st.container():
        # Dodaj klasę CSS odpowiednią dla typu urządzenia
        st.markdown(f'<div class="responsive-container {device_type}">', unsafe_allow_html=True)
        
        # Wywołaj funkcję renderującą zawartość
        result = content_function()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        return result

def responsive_grid(columns_desktop=3, columns_tablet=2, columns_mobile=1):
    """
    Tworzy responsywną siatkę dostosowaną do typu urządzenia.
    
    Parametry:
    - columns_desktop: Liczba kolumn na desktopie
    - columns_tablet: Liczba kolumn na tablecie
    - columns_mobile: Liczba kolumn na urządzeniu mobilnym
    
    Zwraca:
    - lista: Lista obiektów kolumn
    """
    device_type = get_device_type()
    
    if device_type == 'mobile':
        columns = columns_mobile
    elif device_type == 'tablet':
        columns = columns_tablet
    else:
        columns = columns_desktop
    
    return st.columns(columns)
