import streamlit as st
from functools import wraps

def lazy_load(key, loader_func, ttl_minutes=15):
    """
    Dekorator do leniwego ładowania komponentów.
    Używa cache do przechowywania załadowanych danych.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            from utils.cache import Cache
            
            # Sprawdź czy dane są w cache
            data = Cache.get(key, ttl_minutes=ttl_minutes)
            
            if data is None:
                # Pokaż loader podczas ładowania
                with st.spinner("Ładowanie..."):
                    data = loader_func()
                    Cache.set(key, data, ttl_minutes=ttl_minutes)
            
            # Wywołaj oryginalną funkcję z załadowanymi danymi
            return func(data, *args, **kwargs)
        return wrapper
    return decorator

def load_section_when_visible(section_key):
    """
    Dekorator do ładowania sekcji tylko gdy są widoczne.
    Używa sessionState do śledzenia stanu widoczności.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            visibility_key = f"visible_{section_key}"
            
            # Domyślnie ukryj sekcję
            if visibility_key not in st.session_state:
                st.session_state[visibility_key] = False
            
            # Przycisk do pokazania/ukrycia sekcji
            if st.button(
                "Pokaż" if not st.session_state[visibility_key] else "Ukryj",
                key=f"toggle_{section_key}"
            ):
                st.session_state[visibility_key] = not st.session_state[visibility_key]
            
            # Załaduj i pokaż sekcję tylko jeśli jest widoczna
            if st.session_state[visibility_key]:
                return func(*args, **kwargs)
        return wrapper
    return decorator

def paginate_content(items, items_per_page=5):
    """
    Generator do paginacji treści.
    Zwraca tuple (elementy_na_stronie, całkowita_liczba_stron, obecna_strona)
    """
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0
    
    total_items = len(items)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    
    # Przyciski nawigacji
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        if st.button("← Poprzednia", disabled=st.session_state.current_page == 0):
            st.session_state.current_page -= 1
    
    with col2:
        st.markdown(f"Strona {st.session_state.current_page + 1} z {total_pages}")
    
    with col3:
        if st.button("Następna →", disabled=st.session_state.current_page == total_pages - 1):
            st.session_state.current_page += 1
    
    # Wyznacz zakres elementów dla obecnej strony
    start_idx = st.session_state.current_page * items_per_page
    end_idx = min(start_idx + items_per_page, total_items)
    
    return (
        items[start_idx:end_idx],
        total_pages,
        st.session_state.current_page
    )