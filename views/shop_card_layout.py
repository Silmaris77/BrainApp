import streamlit as st
from data.users import load_user_data, save_user_data
import datetime
from datetime import timedelta
from utils.components import zen_header
from utils.material3_components import apply_material3_theme
from utils.card_layout import create_card, create_grid, zen_section, data_panel
from utils.layout import get_device_type

# Check if this module is being used to avoid duplicate rendering
_IS_SHOP_NEW_LOADED = False

def show_shop():
    """
    Wyświetla sklep z nowym układem kart
    """
    global _IS_SHOP_NEW_LOADED
    if _IS_SHOP_NEW_LOADED:
        return
    _IS_SHOP_NEW_LOADED = True  # Zaznacz, że moduł jest już załadowany
    
    # Aplikuj style Material 3
    
    # Pobierz dane użytkownika
    users_data = load_user_data()
    user_data = users_data.get(st.session_state.username, {})
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    # Nagłówek sekcji
    zen_section("Sklep Neuroliderów", "Wykorzystaj zdobyte DegenCoins, aby odblokować dodatkowe funkcje i nagrody", "🛒")
    
    # Wyświetl informację o dostępnych monetach
    st.markdown(f"""
    <div style='background-color: var(--primary-color); color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
        <h3 style='margin: 0; display: flex; align-items: center;'>
            <span style='font-size: 1.5em; margin-right: 10px;'>💰</span>
            Twoje DegenCoins: {user_data.get('degen_coins', 0)}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicjalizacja zakładek w sesji
    if 'shop_tab' not in st.session_state:
        st.session_state.shop_tab = 'avatars'
    
    # Opcje zakładek
    tab_options = ['Avatary', 'Tła', 'Specjalne lekcje', 'Boostery']
    tab_ids = ['avatars', 'backgrounds', 'special_lessons', 'boosters']
    
    # Wyświetl przyciski zakładek
    tab_cols = st.columns(len(tab_options))
    for i, (tab_name, tab_id) in enumerate(zip(tab_options, tab_ids)):
        with tab_cols[i]:
            button_type = "primary" if st.session_state.shop_tab == tab_id else "secondary"
            if st.button(tab_name, key=f"tab_{tab_id}", type=button_type):
                st.session_state.shop_tab = tab_id
                st.rerun()
    
    # Definicje przedmiotów w sklepie
    shop_items = {
        'avatars': [
            {
                'id': 'brain_master',
                'name': 'Brain Master',
                'icon': '🧠',
                'description': 'Avatar symbolizujący eksperta w dziedzinie neuroprzywództwa',
                'price': 50
            },
            {
                'id': 'decision_maker',
                'name': 'Decision Maker',
                'icon': '⚖️',
                'description': 'Avatar symbolizujący lidera podejmującego trafne decyzje',
                'price': 75
            },
            {
                'id': 'innovation_leader',
                'name': 'Innovation Leader',
                'icon': '💡',
                'description': 'Avatar symbolizujący innowacyjnego przywódcę',
                'price': 100
            },
            {
                'id': 'empathy_master',
                'name': 'Empathy Master',
                'icon': '❤️',
                'description': 'Avatar symbolizujący empatycznego lidera',
                'price': 125
            }
        ],
        'backgrounds': [
            {
                'id': 'neural_network',
                'name': 'Neural Network',
                'icon': '🔄',
                'description': 'Tło przedstawiające sieć neuronową',
                'price': 80
            },
            {
                'id': 'brain_waves',
                'name': 'Brain Waves',
                'icon': '〰️',
                'description': 'Tło z wizualizacją fal mózgowych',
                'price': 100
            },
            {
                'id': 'leadership_summit',
                'name': 'Leadership Summit',
                'icon': '🏔️',
                'description': 'Tło symbolizujące szczyt przywódczy',
                'price': 120
            }
        ],
        'special_lessons': [
            {
                'id': 'neuroscience_leadership',
                'name': 'Neuroscience of Leadership',
                'icon': '📚',
                'description': 'Specjalna lekcja o najnowszych odkryciach w dziedzinie neurobiologii przywództwa',
                'price': 150
            },
            {
                'id': 'emotional_intelligence',
                'name': 'Emotional Intelligence Masterclass',
                'icon': '🎓',
                'description': 'Zaawansowany kurs inteligencji emocjonalnej dla liderów',
                'price': 200
            },
            {
                'id': 'stress_management',
                'name': 'Leadership Stress Management',
                'icon': '🧘',
                'description': 'Techniki zarządzania stresem dla liderów oparte na neurobiologii',
                'price': 180
            }
        ],
        'boosters': [
            {
                'id': 'xp_boost',
                'name': 'XP Boost (24h)',
                'icon': '⚡',
                'description': 'Zwiększa zdobywane XP o 50% przez 24 godziny',
                'price': 100
            },
            {
                'id': 'coin_boost',
                'name': 'DegenCoin Boost (24h)',
                'icon': '💰',
                'description': 'Zwiększa zdobywane DegenCoins o 100% przez 24 godziny',
                'price': 150
            },
            {
                'id': 'insight_boost',
                'name': 'Insight Boost (24h)',
                'icon': '💎',
                'description': 'Odblokowuje dodatkowe wskazówki podczas lekcji przez 24 godziny',
                'price': 120
            }
        ]
    }
    
    # Pobierz inwentarz użytkownika (lub inicjalizuj pusty)
    user_inventory = user_data.get('inventory', {})
    
    # Pobierz aktywne boostery
    active_boosters = user_data.get('active_boosters', {})
    
    # Usuwaj wygasłe boostery
    current_time = datetime.datetime.now()
    expired_boosters = []
    
    for booster_id, expiry_time_str in active_boosters.items():
        expiry_time = datetime.datetime.fromisoformat(expiry_time_str)
        if current_time > expiry_time:
            expired_boosters.append(booster_id)
    
    # Usuń wygasłe boostery
    for booster_id in expired_boosters:
        active_boosters.pop(booster_id, None)
    
    # Zapisz zmiany
    if expired_boosters:
        save_user_data(users_data)
    
    # Dostosuj liczbę kolumn zależnie od urządzenia
    num_columns = 1 if device_type == "mobile" else 2
    
    # Wyświetl przedmioty wybranej kategorii w układzie kart
    selected_tab = st.session_state.shop_tab
    items = shop_items.get(selected_tab, [])
    
    # Przygotuj komunikat, jeśli kategoria jest pusta
    if not items:
        st.info(f"Brak przedmiotów w kategorii {selected_tab}")
    else:
        # Użyj układu siatki do wyświetlenia przedmiotów
        item_cols = create_grid(num_columns)
        
        for i, item in enumerate(items):
            # Sprawdź, czy użytkownik już posiada przedmiot
            item_type = selected_tab
            item_id = item['id']
            
            # Sprawdź, czy przedmiot jest już w inwentarzu
            has_item = item_id in user_inventory.get(item_type, [])
            
            # Dla boosterów sprawdź czy jest aktywny
            is_active = False
            time_remaining = ""
            
            if item_type == 'boosters' and item_id in active_boosters:
                is_active = True
                expiry_time = datetime.datetime.fromisoformat(active_boosters[item_id])
                time_delta = expiry_time - current_time
                hours = int(time_delta.total_seconds() // 3600)
                minutes = int((time_delta.total_seconds() % 3600) // 60)
                time_remaining = f"{hours}h {minutes}m"
            
            # Wyświetl przedmiot w karcie
            with item_cols[i % num_columns]:
                # Stan przedmiotu
                button_text = "Kup"
                button_class = "material-button"
                status_text = ""
                
                if has_item:
                    if item_type == 'boosters':
                        if is_active:
                            button_text = "Aktywny"
                            button_class = "material-button disabled"
                            status_text = f"<span style='color: #4CAF50;'>✓ Aktywny (pozostało: {time_remaining})</span>"
                        else:
                            button_text = "Aktywuj"
                            button_class = "material-button secondary"
                            status_text = "<span style='color: #2196F3;'>✓ W inwentarzu</span>"
                    else:
                        button_text = "Wybierz"
                        button_class = "material-button secondary"
                        status_text = "<span style='color: #2196F3;'>✓ Odblokowane</span>"
                
                # Wyświetl kartę przedmiotu
                create_card(
                    title=item['name'],
                    icon=item['icon'],
                    content=f"""
                    <div style='padding: 10px 0;'>
                        <p>{item['description']}</p>
                        <div style="display: flex; justify-content: space-between; margin-top: 10px; align-items: center;">
                            <span style="font-weight: bold;">💰 {item['price']} DegenCoins</span>
                            <span>{status_text}</span>
                        </div>
                        <div style='margin-top: 15px;'>
                            <button class='{button_class}' 
                                onclick="document.getElementById('btn-buy-{item_type}-{item_id}').click()">
                                {button_text}
                            </button>
                        </div>
                    </div>
                    """,
                    key=f"shop_item_{item_type}_{item_id}_card"
                )
                
                # Ukryty przycisk do obsługi kupna/wyboru/aktywacji
                if st.button(button_text, key=f"btn-buy-{item_type}-{item_id}", help="", label_visibility="collapsed"):
                    if has_item:
                        if item_type == 'boosters' and not is_active:
                            # Aktywuj booster
                            expiry_time = datetime.datetime.now() + timedelta(hours=24)
                            user_data['active_boosters'][item_id] = expiry_time.isoformat()
                            save_user_data(users_data)
                            st.success(f"Booster {item['name']} został aktywowany na 24 godziny!")
                            st.rerun()
                        elif item_type in ['avatars', 'backgrounds']:
                            # Wybierz avatar lub tło
                            user_data[f'selected_{item_type[:-1]}'] = item_id  # usuń 's' z końca (avatars -> avatar)
                            save_user_data(users_data)
                            st.success(f"{item['name']} został wybrany!")
                            st.rerun()
                        elif item_type == 'special_lessons':
                            # Przejdź do specjalnej lekcji
                            st.session_state.page = 'lesson'
                            st.session_state.lesson_id = item_id
                            st.rerun()
                    else:
                        # Kup przedmiot
                        success, message = buy_item(item_type, item_id, item['price'], user_data, users_data)
                        if success:
                            st.success(f"Pomyślnie zakupiono: {item['name']}!")
                        else:
                            st.error(message)
                        st.rerun()
    
    # Dodaj CSS dla przycisków
    st.markdown("""
    <style>
    .material-button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.3s;
    }
    
    .material-button:hover {
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        opacity: 0.9;
    }
    
    .material-button.secondary {
        background-color: #f0f0f0;
        color: #333;
    }
    
    .material-button.disabled {
        background-color: #e0e0e0;
        color: #999;
        cursor: not-allowed;
    }
    </style>
    """, unsafe_allow_html=True)

def buy_item(item_type, item_id, price, user_data, users_data):
    """
    Process the purchase of an item
    
    Parameters:
    - item_type: Type of the item (avatar, background, special_lesson, booster)
    - item_id: Unique identifier of the item
    - price: Cost in DegenCoins
    - user_data: User's data dictionary
    - users_data: All users' data dictionary
    
    Returns:
    - (success, message): Tuple with success status and message
    """
    # Sprawdź czy użytkownik ma wystarczającą ilość monet
    if user_data.get('degen_coins', 0) < price:
        return False, "Nie masz wystarczającej liczby DegenCoins!"
    
    # Odejmij monety
    user_data['degen_coins'] = user_data.get('degen_coins', 0) - price
    
    # Dodaj przedmiot do ekwipunku użytkownika
    if 'inventory' not in user_data:
        user_data['inventory'] = {}
    
    if item_type not in user_data['inventory']:
        user_data['inventory'][item_type] = []
    
    # Dodaj przedmiot do odpowiedniej kategorii (unikaj duplikatów)
    if item_id not in user_data['inventory'][item_type]:
        user_data['inventory'][item_type].append(item_id)
    
    # Dodaj specjalną obsługę dla boosterów (dodając datę wygaśnięcia)
    if item_type == 'booster':
        if 'active_boosters' not in user_data:
            user_data['active_boosters'] = {}
        
        # Ustawienie czasu wygaśnięcia na 24 godziny od teraz
        expiry_time = datetime.datetime.now() + timedelta(hours=24)
        user_data['active_boosters'][item_id] = expiry_time.isoformat()
    
    # Zapisz dane użytkownika
    save_user_data(users_data)
    
    return True, "Zakup dokonany pomyślnie!"
