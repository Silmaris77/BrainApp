import streamlit as st
from utils.ui import initialize_ui
from utils.ui.components.interactive import zen_button, notification
from utils.ui.components.text import content_section, zen_header
from utils.ui.layouts.grid import responsive_grid, render_dashboard_header

def show_shop_ui():
    """
    Wyświetla sklep używając nowego systemu UI zgodnego z CSP
    """
    # Inicjalizacja UI
    initialize_ui()
    
    # Nagłówek sklepu
    render_dashboard_header("Sklep Neuroliderów", "Zdobywaj nagrody i ulepszenia za DegenCoins")
    
    # Filtrowanie produktów
    st.markdown("### Kategorie produktów")
    
    # Zakładki kategorii
    categories = ["Wszystkie", "Avatary", "Tytuły", "Kolory", "Inne"]
    selected_category = st.radio("Wybierz kategorię", categories, horizontal=True, label_visibility="collapsed")
    
    # Lista produktów
    show_shop_items(selected_category.lower())

def show_shop_items(category="wszystkie"):
    """
    Wyświetla przedmioty w sklepie z danej kategorii
    """
    # Przykładowe dane przedmiotów (w prawdziwej aplikacji pobierane z bazy)
    shop_items = get_shop_items()
    
    # Filtrowanie przedmiotów według kategorii
    if category != "wszystkie":
        filtered_items = [(item_type, item_id, item) for item_type, item_id, item in shop_items if item.get('category', '').lower() == category]
    else:
        filtered_items = shop_items
    
    # Wyświetlanie przedmiotów w siatce
    if not filtered_items:
        st.markdown("Brak przedmiotów w tej kategorii.")
        return
    
    # Użyj responsywnej siatki
    cols = responsive_grid(columns_desktop=3, columns_tablet=2, columns_mobile=1)
    
    # Podziel przedmioty na kolumny
    items_per_column = (len(filtered_items) + len(cols) - 1) // len(cols)
    
    # Rozmieść przedmioty w kolumnach
    for i, column in enumerate(cols):
        with column:
            start_idx = i * items_per_column
            end_idx = min(start_idx + items_per_column, len(filtered_items))
            
            for j in range(start_idx, end_idx):
                item_type, item_id, item = filtered_items[j]
                render_shop_item(item_type, item_id, item)

def render_shop_item(item_type, item_id, item):
    """
    Renderuje pojedynczy przedmiot w sklepie
    """
    # Sprawdź status przedmiotu u użytkownika
    user_inventory = get_user_inventory()
    owned = item_id in user_inventory.get(item_type, [])
    is_active = item_id in user_inventory.get(f'active_{item_type}', [])
    
    # Tekst statusu i klasa przycisku
    if owned:
        if is_active:
            status_text = "Aktywny"
            button_text = "Dezaktywuj"
            button_class = "warning-button"
        else:
            status_text = "Posiadany"
            button_text = "Aktywuj"
            button_class = "secondary-button"
    else:
        status_text = "Nie posiadasz"
        button_text = f"Kup za {item['price']} 💰"
        button_class = "primary-button"
    
    # Wyświetl kartę przedmiotu
    with st.container():
        st.markdown(f"""
        <div style='padding: 15px; background-color: rgba(255, 255, 255, 0.05); border-radius: 10px; margin-bottom: 15px;'>
            <div style='font-weight: bold; font-size: 18px;'>{item['name']}</div>
            <div style='margin: 10px 0; color: rgba(255, 255, 255, 0.8);'>{item['description']}</div>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='font-weight: bold;'>💰 {item['price']} DegenCoins</span>
                <span>{status_text}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Przycisk kupna/aktywacji
        if zen_button(button_text, key=f"btn-buy-{item_type}-{item_id}"):
            # Logika zakupu lub aktywacji przedmiotu
            handle_shop_item_action(item_type, item_id, item, owned, is_active)

def handle_shop_item_action(item_type, item_id, item, owned, is_active):
    """
    Obsługuje akcję związaną z przedmiotem w sklepie
    """
    user_data = get_user_data()
    user_coins = user_data.get('degen_coins', 0)
    
    if not owned:
        # Logika zakupu
        if user_coins >= item['price']:
            # Odejmij monety
            user_data['degen_coins'] = user_coins - item['price']
            
            # Dodaj przedmiot do ekwipunku
            if item_type not in user_data.get('inventory', {}):
                user_data.setdefault('inventory', {})[item_type] = []
            
            user_data['inventory'][item_type].append(item_id)
            
            # Zaktualizuj dane użytkownika
            save_user_data(user_data)
            
            notification(f"Zakupiono przedmiot: {item['name']}", "success")
        else:
            notification("Nie masz wystarczającej liczby DegenCoins", "error")
    else:
        # Logika aktywacji/dezaktywacji
        if not is_active:
            # Aktywuj przedmiot
            active_key = f'active_{item_type}'
            if active_key not in user_data.get('inventory', {}):
                user_data.setdefault('inventory', {})[active_key] = []
            
            user_data['inventory'][active_key].append(item_id)
            notification(f"Aktywowano przedmiot: {item['name']}", "success")
        else:
            # Dezaktywuj przedmiot
            active_key = f'active_{item_type}'
            user_data['inventory'][active_key].remove(item_id)
            notification(f"Dezaktywowano przedmiot: {item['name']}", "info")
        
        # Zaktualizuj dane użytkownika
        save_user_data(user_data)

# Funkcje pomocnicze do pobierania danych
def get_shop_items():
    """
    Pobiera dostępne przedmioty w sklepie
    """
    # W prawdziwej aplikacji dane byłyby pobierane z bazy
    return [
        ('avatar', 'avatar1', {'name': 'Avatar Programisty', 'description': 'Specjalny avatar dla pasjonatów kodowania', 'price': 100, 'category': 'avatary'}),
        ('avatar', 'avatar2', {'name': 'Avatar Stratega', 'description': 'Avatar dla osób o strategicznym myśleniu', 'price': 150, 'category': 'avatary'}),
        ('title', 'title1', {'name': 'Tytuł: Neuromistrz', 'description': 'Prestiżowy tytuł dla najlepszych neuroinżynierów', 'price': 200, 'category': 'tytuły'}),
        ('title', 'title2', {'name': 'Tytuł: Degen Lord', 'description': 'Tytuł dla prawdziwych koneserów rynków krypto', 'price': 250, 'category': 'tytuły'}),
        ('color', 'blue', {'name': 'Niebieski motyw', 'description': 'Zmień kolor interfejsu na niebieski', 'price': 50, 'category': 'kolory'}),
        ('color', 'purple', {'name': 'Fioletowy motyw', 'description': 'Zmień kolor interfejsu na fioletowy', 'price': 50, 'category': 'kolory'}),
        ('item', 'boost1', {'name': 'Wzmacniacz XP', 'description': 'Zwiększa zdobywane XP o 10% przez tydzień', 'price': 300, 'category': 'inne'})
    ]

def get_user_inventory():
    """
    Pobiera ekwipunek użytkownika
    """
    user_data = get_user_data()
    return user_data.get('inventory', {})

def get_user_data():
    """
    Pobiera dane użytkownika
    """
    # W prawdziwej aplikacji dane byłyby pobierane z bazy
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {
            'username': 'testuser',
            'degen_coins': 500,
            'inventory': {
                'avatar': ['avatar1'],
                'active_avatar': ['avatar1']
            }
        }
    return st.session_state.user_data

def save_user_data(user_data):
    """
    Zapisuje dane użytkownika
    """
    # W prawdziwej aplikacji dane byłyby zapisywane do bazy
    st.session_state.user_data = user_data
