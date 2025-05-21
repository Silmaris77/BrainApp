import streamlit as st
from data.users import load_user_data, save_user_data
import datetime
from datetime import timedelta
from utils.components import zen_header
from utils.material3_components import apply_material3_theme

# Check if this module is being used to avoid duplicate rendering
_IS_SHOP_NEW_LOADED = False

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
    
    # Zapisz zmiany w danych użytkownika
    users_data[user_data['username']] = user_data
    save_user_data(users_data)
    
    return True, f"Pomyślnie zakupiono przedmiot za {price} DegenCoins!"

def show_shop():
    """
    Wyświetla sklep z przedmiotami do zakupu.
    """
        # Zastosuj style Material 3
    apply_material3_theme()
    
    global _IS_SHOP_NEW_LOADED
    
    # Unikaj podwójnego renderowania
    if _IS_SHOP_NEW_LOADED:
        return
    _IS_SHOP_NEW_LOADED = True
    
    # Załaduj dane użytkownika
    users_data = load_user_data()
    user_data = users_data.get(st.session_state.username, {})
    
    # Wyświetl główną zawartość (bez używania sidebara)
    # Struktura kontentu dokładnie taka jak w innych zakładkach
    zen_header("Sklep 🛒")  # Używaj zen_header zamiast st.markdown dla spójności
    
    # Wyświetl ilość monet użytkownika
    st.markdown(f"### Twoje DegenCoins: <span style='color: #FFA500;'>🪙 {user_data.get('degen_coins', 0)}</span>", unsafe_allow_html=True)
    
    # Zakładki sklepu
    tab_avatars, tab_backgrounds, tab_special_lessons, tab_boosters = st.tabs(["Awatary", "Tła", "Specjalne Lekcje", "Boostery"])
    
    # Awatary
    with tab_avatars:
        st.markdown("# Awatary 🔗")
        
        # Lista dostępnych awatarów
        avatars = {
            "diamond_degen": {
                "name": "💎 Diamond Degen",
                "price": 500,
                "description": "Pokazuje twoje zaangażowanie w rozwój jako inwestor."
            },
            "crypto_wizard": {
                "name": "🧙 Crypto Wizard",
                "price": 750,
                "description": "Awatar dla tych, którzy mistrzowsko opanowali sztukę inwestowania."
            },
            "moon_hunter": {
                "name": "🌕 Moon Hunter",
                "price": 1000,
                "description": "Dla tych, którzy zawsze celują wysoko."
            }
        }
        
        # Wyświetl dostępne awatary w trzech kolumnach
        cols = st.columns(3)
        
        for i, (avatar_id, avatar) in enumerate(avatars.items()):
            with cols[i % 3]:
                st.markdown(f"## {avatar['name']}")
                st.markdown(f"Cena: 🪙 {avatar['price']}")
                
                # Sprawdź czy użytkownik posiada już ten awatar
                user_has_item = 'inventory' in user_data and 'avatar' in user_data.get('inventory', {}) and avatar_id in user_data['inventory']['avatar']
                
                if user_has_item:
                    # Sprawdź czy awatar jest aktualnie używany
                    is_active = user_data.get('active_avatar') == avatar_id
                    
                    if is_active:
                        st.success("Ten awatar jest aktualnie używany")
                    else:
                        if st.button(f"Użyj {avatar['name']}", key=f"use_{avatar_id}"):
                            user_data['active_avatar'] = avatar_id
                            users_data[st.session_state.username] = user_data
                            save_user_data(users_data)
                            st.success(f"Ustawiono {avatar['name']} jako aktywny awatar!")
                            st.rerun()
                else:
                    # Przycisk do zakupu
                    if st.button(f"Kup {avatar['name']}", key=f"buy_{avatar_id}"):
                        success, message = buy_item('avatar', avatar_id, avatar['price'], user_data, users_data)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
    
    # Tła
    with tab_backgrounds:
        st.markdown("# Tła")
        
        # Lista dostępnych teł
        backgrounds = {
            "crypto_city": {
                "name": "🏙️ Crypto City",
                "price": 300,
                "description": "Nowoczesne miasto przyszłości."
            },
            "zen_garden": {
                "name": "🌿 Zen Garden",
                "price": 400,
                "description": "Spokojny ogród dla zrównoważonych inwestorów."
            },
            "space_station": {
                "name": "🚀 Space Station",
                "price": 600,
                "description": "Dla inwestorów, którzy sięgają gwiazd."
            }
        }
        
        # Wyświetl dostępne tła w trzech kolumnach
        cols = st.columns(3)
        
        for i, (bg_id, bg) in enumerate(backgrounds.items()):
            with cols[i % 3]:
                st.markdown(f"## {bg['name']}")
                st.markdown(f"Cena: 🪙 {bg['price']}")
                
                # Sprawdź czy użytkownik posiada już to tło
                user_has_item = 'inventory' in user_data and 'background' in user_data.get('inventory', {}) and bg_id in user_data['inventory']['background']
                
                if user_has_item:
                    # Sprawdź czy tło jest aktualnie używane
                    is_active = user_data.get('active_background') == bg_id
                    
                    if is_active:
                        st.success("To tło jest aktualnie używane")
                    else:
                        if st.button(f"Użyj {bg['name']}", key=f"use_{bg_id}"):
                            user_data['active_background'] = bg_id
                            users_data[st.session_state.username] = user_data
                            save_user_data(users_data)
                            st.success(f"Ustawiono {bg['name']} jako aktywne tło!")
                            st.rerun()
                else:
                    # Przycisk do zakupu
                    if st.button(f"Kup {bg['name']}", key=f"buy_{bg_id}"):
                        success, message = buy_item('background', bg_id, bg['price'], user_data, users_data)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
    
    # Specjalne lekcje
    with tab_special_lessons:
        st.markdown("# Specjalne Lekcje")
        
        # Lista dostępnych specjalnych lekcji
        special_lessons = {
            "market_psychology": {
                "name": "📊 Psychologia Rynku Zaawansowana",
                "price": 800,
                "description": "Zaawansowane techniki psychologii rynku."
            },
            "risk_management": {
                "name": "🛡️ Zarządzanie Ryzykiem Pro",
                "price": 700,
                "description": "Profesjonalne techniki zarządzania ryzykiem."
            },
            "trading_mastery": {
                "name": "🧠 Mistrzostwo Tradingowe",
                "price": 1200,
                "description": "Odkryj sekrety mistrzów tradingu."
            }
        }
        
        # Wyświetl dostępne lekcje w trzech kolumnach
        cols = st.columns(3)
        
        for i, (lesson_id, lesson) in enumerate(special_lessons.items()):
            with cols[i % 3]:
                st.markdown(f"## {lesson['name']}")
                st.markdown(f"Cena: 🪙 {lesson['price']}")
                st.markdown(lesson['description'])
                
                # Sprawdź czy użytkownik posiada już tę lekcję
                user_has_item = 'inventory' in user_data and 'special_lesson' in user_data.get('inventory', {}) and lesson_id in user_data['inventory']['special_lesson']
                
                if user_has_item:
                    if st.button(f"Rozpocznij lekcję {lesson['name']}", key=f"start_{lesson_id}"):
                        st.session_state.page = 'lesson'
                        st.session_state.lesson_id = f"special_{lesson_id}"
                        st.rerun()
                else:
                    # Przycisk do zakupu
                    if st.button(f"Kup {lesson['name']}", key=f"buy_{lesson_id}"):
                        success, message = buy_item('special_lesson', lesson_id, lesson['price'], user_data, users_data)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
    
    # Boostery
    with tab_boosters:
        st.markdown("# Boostery")
        
        # Lista dostępnych boosterów
        boosters = {
            "xp_boost": {
                "name": "⚡ XP Boost",
                "price": 200,
                "description": "Zwiększa ilość zdobywanego XP o 50% przez 24 godziny."
            },
            "coin_boost": {
                "name": "🪙 Coin Boost",
                "price": 300,
                "description": "Zwiększa ilość zdobywanych monet o 50% przez 24 godziny."
            },
            "focus_boost": {
                "name": "🎯 Focus Boost",
                "price": 250,
                "description": "Zwiększa szybkość ukończenia lekcji o 30% przez 24 godziny."
            }
        }
        
        # Wyświetl dostępne boostery w trzech kolumnach
        cols = st.columns(3)
        
        for i, (booster_id, booster) in enumerate(boosters.items()):
            with cols[i % 3]:
                st.markdown(f"## {booster['name']}")
                st.markdown(f"Cena: 🪙 {booster['price']}")
                st.markdown(booster['description'])
                
                # Sprawdź czy booster jest aktywny
                is_active = False
                remaining_time = None
                
                if 'active_boosters' in user_data and booster_id in user_data.get('active_boosters', {}):
                    expiry_time = datetime.datetime.fromisoformat(user_data['active_boosters'][booster_id])
                    now = datetime.datetime.now()
                    
                    if expiry_time > now:
                        is_active = True
                        remaining_seconds = (expiry_time - now).total_seconds()
                        remaining_hours = int(remaining_seconds // 3600)
                        remaining_minutes = int((remaining_seconds % 3600) // 60)
                        remaining_time = f"{remaining_hours}h {remaining_minutes}m"
                
                if is_active:
                    st.success(f"Aktywny! Pozostały czas: {remaining_time}")
                else:
                    # Przycisk do zakupu
                    if st.button(f"Kup {booster['name']}", key=f"buy_{booster_id}"):
                        success, message = buy_item('booster', booster_id, booster['price'], user_data, users_data)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
