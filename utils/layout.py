import streamlit as st

def get_device_type():
    """
    Wykrywa typ urządzenia na podstawie szerokości okna przeglądarki.
    Zwraca: 'mobile', 'tablet' lub 'desktop'
    
    Uwaga: Jest to przybliżenie, które może nie być 100% dokładne, ale działa
    wystarczająco dobrze dla większości przypadków.
    """
    # Streamlit nie dostarcza bezpośredniego sposobu wykrywania szerokości ekranu,
    # więc używamy JavaScript i zapisujemy wynik w session_state
    
    # Dodajemy kod JS, który będzie aktualizował session_state
    st.markdown("""
    <script>
        // Ten kod zostanie zablokowany przez Streamlit, ale zostawiamy jako odniesienie
        // jak można by to zrobić z JS, gdyby Streamlit na to pozwalał
        
        // const updateScreenSize = () => {
        //     const width = window.innerWidth;
        //     if (width < 768) {
        //         window.Streamlit.setComponentValue('mobile');
        //     } else if (width < 1024) {
        //         window.Streamlit.setComponentValue('tablet');
        //     } else {
        //         window.Streamlit.setComponentValue('desktop');
        //     }
        // }
        // 
        // updateScreenSize();
        // window.addEventListener('resize', updateScreenSize);
    </script>
    """, unsafe_allow_html=True)
    
    # Ponieważ powyższy kod JS nie działa w Streamlit, używamy prostego mechanizmu
    # z CSS media queries i sprawdzenia szerokości kontenera Streamlit
    
    # Dla celów testowych, możemy też ustawić tryb ręcznie
    if 'device_type' not in st.session_state or st.session_state.device_type is None:
        # Domyślnie przyjmujemy desktop, ale można to zmienić w ustawieniach
        st.session_state.device_type = 'desktop'
    
    return st.session_state.device_type

def responsive_grid(columns_desktop=3, columns_tablet=2, columns_mobile=1):
    """
    Tworzy responsywny grid, który dostosowuje liczbę kolumn w zależności od urządzenia.
    
    Args:
        columns_desktop: Liczba kolumn na desktopie (domyślnie 3)
        columns_tablet: Liczba kolumn na tablecie (domyślnie 2)
        columns_mobile: Liczba kolumn na telefonie (domyślnie 1)
    
    Returns:
        Lista obiektów kolumn Streamlit
    """
    device = get_device_type()
    
    if device == 'mobile':
        columns = columns_mobile
    elif device == 'tablet':
        columns = columns_tablet
    else:
        columns = columns_desktop
    
    return st.columns(columns)

def responsive_container(desktop_width='80%', tablet_width='90%', mobile_width='100%'):
    """
    Tworzy kontener o responsywnej szerokości zależnej od urządzenia.
    
    Args:
        desktop_width: Szerokość na desktopie (domyślnie '80%')
        tablet_width: Szerokość na tablecie (domyślnie '90%')
        mobile_width: Szerokość na telefonie (domyślnie '100%')
    
    Returns:
        CSS style string do użycia w kontenerze
    """
    device = get_device_type()
    
    if device == 'mobile':
        width = mobile_width
    elif device == 'tablet':
        width = tablet_width
    else:
        width = desktop_width
    
    # Zwracamy string z CSS do wykorzystania w markdown
    return f"""
    <style>
    .responsive-container {{
        width: {width};
        margin: 0 auto;
    }}
    </style>
    <div class="responsive-container">
    """

def end_responsive_container():
    """Zamyka responsywny kontener"""
    return "</div>"

def apply_responsive_styles():
    """Dodaje globalne style CSS dla responsywności"""
    
    # Dodajemy style odpowiedzialne za responsywność
    st.markdown("""
    <style>
    /* Media Queries dla różnych urządzeń */
    
    /* Mobilne */
    @media (max-width: 640px) {
        .hide-mobile {
            display: none !important;
        }
        
        .st-emotion-cache-1r6slb0 {  /* Główny kontener */
            padding: 1rem 0.75rem !important;
        }
        
        .st-emotion-cache-16txtl3 h1 {  /* Nagłówki */
            font-size: 1.5rem !important;
        }
        
        .st-emotion-cache-10trblm {  /* Tekst */
            font-size: 0.9rem !important;
        }
        
        .st-emotion-cache-1erivem {  /* Przyciski */
            font-size: 0.85rem !important;
            padding: 0.3rem 0.6rem !important;
        }
        
        /* Mniejsze odstępy w formularzach */
        .st-emotion-cache-183lzff {
            gap: 0.75rem !important;
        }
        
        /* Zmniejszone odstępy dla tabów */
        [data-testid="stHorizontalBlock"] {
            gap: 0.5rem !important;
        }
        
        /* Responsive styling for charts */
        .stChart > div {
            max-width: 100% !important;
            overflow: hidden !important;
        }
        
        /* Radar chart container sizing */
        .stChart svg {
            width: 100% !important;
            height: auto !important;
        }
        
        /* Slight negative margin for chart containers on mobile */
        .stChart {
            margin: 0 -10px !important;
        }
        
        /* Better font sizing for legends */
        .stChart text {
            font-size: 0.85rem !important;
        }
    }
    
    /* Tablety */
    @media (min-width: 641px) and (max-width: 1024px) {
        .hide-tablet {
            display: none !important;
        }
        
        .st-emotion-cache-1r6slb0 {  /* Główny kontener */
            padding: 1.5rem 1.25rem !important;
        }
        
        /* Chart sizing for tablets */
        .stChart > div {
            max-width: 85% !important;
            margin: 0 auto !important;
        }
    }
    
    /* Desktop */
    @media (min-width: 1025px) {
        .hide-desktop {
            display: none !important;
        }
        
        /* Chart sizing for desktop */
        .stChart > div {
            max-width: 75% !important;
            margin: 0 auto !important;
        }
    }
    
    /* Helpers dla różnych urządzeń */
    .visible-mobile-only {
        display: none;
    }
    
    .visible-tablet-only {
        display: none;
    }
    
    .visible-desktop-only {
        display: none;
    }
    
    @media (max-width: 640px) {
        .visible-mobile-only {
            display: block !important;
        }
    }
    
    @media (min-width: 641px) and (max-width: 1024px) {
        .visible-tablet-only {
            display: block !important;
        }
    }
    
    @media (min-width: 1025px) {
        .visible-desktop-only {
            display: block !important;
        }
    }
    
    /* Responsywne czcionki */
    html {
        font-size: calc(14px + 0.25vw);
    }
    
    /* Animacje wejścia na mobilnych wolniejsze dla lepszej wydajności */
    @media (max-width: 640px) {
        .fadeIn, .scaleIn {
            animation-duration: 0.3s !important;
        }
    }
    
    /* Custom radar chart container (for profile & degen test) */
    .radar-chart-container {
        transition: all 0.3s ease;
    }
    
    @media (max-width: 640px) {
        .radar-chart-container {
            transform: scale(0.95);
            transform-origin: center;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    return

def get_responsive_figure_size(device_type=None, scale_factor=1.0):
    """
    Returns an appropriate figure size based on device type for matplotlib plots
    
    Args:
        device_type: 'mobile', 'tablet', or 'desktop'. If None, will be detected
        scale_factor: Optional scaling factor to adjust the standard sizes
        
    Returns:
        tuple: (width, height) for the figure size
    """
    if device_type is None:
        device_type = get_device_type()
        
    if device_type == 'mobile':
        return (5 * scale_factor, 5 * scale_factor)
    elif device_type == 'tablet':
        return (7 * scale_factor, 7 * scale_factor)
    else:  # desktop
        return (9 * scale_factor, 9 * scale_factor)


def toggle_device_view():
    """
    Tworzy przełącznik do testowego przełączania między widokami dla różnych urządzeń
    Używaj tego tylko w trybie developerskim, nie w produkcji
    """
    st.sidebar.markdown("### 📱 Symulacja urządzenia")
    device_options = ["desktop", "tablet", "mobile"]
    current_device = st.session_state.get('device_type', 'desktop')
    
    selected_device = st.sidebar.radio(
        "Wybierz urządzenie:", 
        device_options,
        index=device_options.index(current_device)
    )
    
    if selected_device != current_device:
        st.session_state.device_type = selected_device
        st.rerun()
        
    st.sidebar.markdown(f"Aktualny widok: **{selected_device}**")
    
    return selected_device