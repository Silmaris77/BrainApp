import streamlit as st
from data.users import load_user_data, save_user_data
import datetime

def activate_item(username, item_type, item_id):
    """
    Activate a purchased item (avatar, background, etc.)
    
    Parameters:
    - username: Username of the user
    - item_type: Type of the item ('avatar', 'background', etc.)
    - item_id: ID of the item to activate
    
    Returns:
    - (success, message): Tuple with success status and message
    """
    users_data = load_user_data()
    if username not in users_data:
        return False, "Użytkownik nie istnieje"
    
    user_data = users_data[username]
    
    # Check if item exists in user's inventory
    inventory_key = f"owned_{item_type}s"
    if inventory_key not in user_data or item_id not in user_data[inventory_key]:
        return False, f"Nie posiadasz tego przedmiotu ({item_id})"
    
    # Handle different item types
    if item_type == 'avatar':
        user_data['avatar'] = item_id
        
    elif item_type == 'background':
        user_data['background'] = item_id
        
    elif item_type == 'special_lesson':
        # Unlock the special lesson
        if 'unlocked_special_lessons' not in user_data:
            user_data['unlocked_special_lessons'] = []
        if item_id not in user_data['unlocked_special_lessons']:
            user_data['unlocked_special_lessons'].append(item_id)
    
    elif item_type == 'booster':
        # Set the booster as active
        if 'active_boosters' not in user_data:
            user_data['active_boosters'] = {}
        
        # Define booster durations
        booster_durations = {
            'double_xp': datetime.timedelta(hours=24),
            'extra_coins': datetime.timedelta(days=7),
            'vip_access': datetime.timedelta(days=30)
        }
        
        # Set activation time and expiration time
        expiration_date = datetime.datetime.now() + booster_durations.get(item_id, datetime.timedelta(days=1))
        user_data['active_boosters'][item_id] = {
            'expires_at': expiration_date.isoformat(),
            'activated_at': datetime.datetime.now().isoformat()
        }
    
    # Save the updated user data
    users_data[username] = user_data
    save_user_data(users_data)
    
    return True, f"Przedmiot {item_id} został aktywowany!"

def get_user_inventory(username):
    """
    Get the inventory of a user
    
    Parameters:
    - username: Username of the user
    
    Returns:
    - inventory: Dictionary with inventory items
    """
    users_data = load_user_data()
    if username not in users_data:
        return {}
    
    user_data = users_data[username]
    
    inventory = {
        'avatars': user_data.get('owned_avatars', []),
        'backgrounds': user_data.get('owned_backgrounds', []),
        'special_lessons': user_data.get('owned_special_lessons', []),
        'boosters': user_data.get('active_boosters', {})
    }
    
    return inventory

def is_booster_active(username, booster_id):
    """
    Check if a booster is active for a user
    
    Parameters:
    - username: Username of the user
    - booster_id: ID of the booster
    
    Returns:
    - is_active: Boolean indicating if the booster is active
    - expiration: Expiration date string or None
    """
    users_data = load_user_data()
    if username not in users_data:
        return False, None
    
    user_data = users_data[username]
    
    if 'active_boosters' not in user_data or booster_id not in user_data['active_boosters']:
        return False, None
    
    booster_data = user_data['active_boosters'][booster_id]
    expiration_str = booster_data.get('expires_at')
    
    if not expiration_str:
        return False, None
    
    try:
        expiration_date = datetime.datetime.fromisoformat(expiration_str)
        is_active = datetime.datetime.now() < expiration_date
        return is_active, expiration_str
    except:
        return False, None

def format_time_remaining(expiration_str):
    """
    Format the time remaining for a booster
    
    Parameters:
    - expiration_str: Expiration date string in ISO format
    
    Returns:
    - formatted_time: Formatted time string
    """
    try:
        expiration_date = datetime.datetime.fromisoformat(expiration_str)
        time_remaining = expiration_date - datetime.datetime.now()
        
        days = time_remaining.days
        hours, remainder = divmod(time_remaining.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        if days > 0:
            return f"{days}d {hours}h pozostało"
        elif hours > 0:
            return f"{hours}h {minutes}m pozostało"
        else:
            return f"{minutes}m pozostało"
    except:
        return "Nieznany czas"
