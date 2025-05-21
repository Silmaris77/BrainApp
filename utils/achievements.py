from config.settings import BADGES
from data.users import load_user_data, save_user_data
from datetime import datetime

def check_achievements(username):
    """Sprawdza osiągnięcia użytkownika i przyznaje nowe odznaki"""
    users_data = load_user_data()
    user_data = users_data.get(username, {})
    user_badges = user_data.get("badges", [])
    new_badges = []
    
    # Sprawdź każdą odznakę, której użytkownik jeszcze nie ma
    for badge_id, badge in BADGES.items():
        if badge_id not in user_badges:
            # Sprawdź warunki dla poszczególnych odznak
            if badge_id == "starter" and not user_badges:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "tester" and user_data.get("degen_type"):
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "learner" and user_data.get("completed_lessons"):
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "consistent" and user_data.get("login_streak", 0) >= 5:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            # Dodaj warunki dla nowych odznak
            elif badge_id == "streak_master" and user_data.get("login_streak", 0) >= 10:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
                
            elif badge_id == "daily_hero" and user_data.get("daily_missions_completed_in_day", 0) >= 5:
                user_badges.append(badge_id)
                new_badges.append(badge_id)
            
            # Pozostałe warunki dla innych odznak...
    
    # Zapisz aktualizację, jeśli przyznano nowe odznaki
    if new_badges:
        user_data["badges"] = user_badges
        users_data[username] = user_data
        save_user_data(users_data)
        
        # Przyznaj XP za nowe odznaki
        xp_per_badge = 50
        total_xp = len(new_badges) * xp_per_badge
        add_xp(username, total_xp)
        
    return new_badges

def add_xp(username, xp_amount):
    """Dodaj XP użytkownikowi i sprawdź, czy awansował na nowy poziom"""
    from config.settings import XP_LEVELS
    
    users_data = load_user_data()
    user_data = users_data.get(username, {})
    
    current_xp = user_data.get("xp", 0)
    current_level = user_data.get("level", 1)
    
    # Dodaj XP
    new_xp = current_xp + xp_amount
    user_data["xp"] = new_xp
    
    # Sprawdź, czy użytkownik awansował
    new_level = current_level
    for level, required_xp in sorted(XP_LEVELS.items()):
        if new_xp >= required_xp:
            new_level = level
    
    # Jeśli jest nowy poziom, zaktualizuj
    if new_level > current_level:
        user_data["level"] = new_level
        users_data[username] = user_data
        save_user_data(users_data)
        return True, new_level
    
    # Zapisz dane
    users_data[username] = user_data
    save_user_data(users_data)
    return False, current_level