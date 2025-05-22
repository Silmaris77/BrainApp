import streamlit as st

def zen_button(label, on_click=None, key=None, disabled=False, help=None, use_container_width=False):
    """
    Tworzy stylizowany przycisk Zen.
    
    Parametry:
    - label: Etykieta przycisku
    - on_click: Funkcja do wykonania po kliknięciu
    - key: Unikalny klucz przycisku
    - disabled: Czy przycisk jest wyłączony
    - help: Tekst pomocy pokazywany po najechaniu
    - use_container_width: Czy przycisk ma używać pełnej szerokości kontenera
    
    Zwraca:
    - Bool: True jeśli przycisk został kliknięty
    """
    return st.button(
        label, 
        on_click=on_click, 
        key=key, 
        disabled=disabled, 
        help=help, 
        use_container_width=use_container_width
    )

def notification(message, type="info"):
    """
    Wyświetla powiadomienie.
    
    Parametry:
    - message: Treść powiadomienia
    - type: Typ powiadomienia (info, success, warning, error)
    """
    if type == "info":
        st.info(message)
    elif type == "success":
        st.success(message)
    elif type == "warning":
        st.warning(message)
    elif type == "error":
        st.error(message)
        
def progress_bar(progress, color="#4CAF50"):
    """
    Wyświetla pasek postępu z niestandardowym stylem.
    
    Args:
        progress (float): Wartość postępu od 0.0 do 1.0
        color (str): Kolor paska postępu w formacie HEX
    """
    # Upewnij się, że progress jest w zakresie [0.0, 1.0]
    progress = min(max(progress, 0.0), 1.0)
    
    # Zastosuj niestandardowy styl bez używania inline JavaScript
    bar_style = f"""
    <style>
    .stProgress > div > div > div > div {{
        background-color: {color};
    }}
    </style>
    """
    st.markdown(bar_style, unsafe_allow_html=True)
    
    # Wyświetl pasek postępu
    st.progress(progress)
