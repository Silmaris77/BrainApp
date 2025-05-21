from datetime import datetime, timedelta
from data.users import load_user_data, save_user_data

def reset_daily_missions():
    """Reset daily missions for all users at midnight"""
    users_data = load_user_data()
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    for username, user_data in users_data.items():
        if user_data.get('last_mission_reset') != current_date:
            user_data['daily_missions'] = []
            user_data['last_mission_reset'] = current_date
    
    save_user_data(users_data)

def complete_daily_mission(username, mission_title):
    """Mark a daily mission as completed for a user"""
    users_data = load_user_data()
    if username in users_data:
        if 'daily_missions' not in users_data[username]:
            users_data[username]['daily_missions'] = []
        
        # Check if the mission is not already completed
        if mission_title not in users_data[username]['daily_missions']:
            users_data[username]['daily_missions'].append(mission_title)
            
            # Find mission and add XP
            from config.settings import DAILY_MISSIONS
            for mission in DAILY_MISSIONS:
                if mission['title'] == mission_title:
                    users_data[username]['xp'] = users_data[username].get('xp', 0) + mission['xp']
                    break
            
            # Check if all missions are completed
            if len(users_data[username]['daily_missions']) == len(DAILY_MISSIONS):
                # Award badge for completing all missions
                from data.users import award_badge
                award_badge(username, 'daily_warrior')
                
                # Update streak
                current_date = datetime.now().strftime("%Y-%m-%d")
                last_completed_date = users_data[username].get('last_mission_complete_date', '')
                
                yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                
                # If yesterday was the last complete date, increment streak
                if last_completed_date == yesterday:
                    users_data[username]['mission_streak'] = users_data[username].get('mission_streak', 0) + 1
                # If there's a gap (not yesterday), reset streak to 1
                elif last_completed_date != current_date:
                    users_data[username]['mission_streak'] = 1
                
                # Set today as the last complete date
                users_data[username]['last_mission_complete_date'] = current_date
            
            save_user_data(users_data)
            return True
    return False

def get_daily_missions_progress(username):
    """Get progress of daily missions for a user"""
    users_data = load_user_data()
    if username in users_data:
        # Get completed mission titles
        completed_missions = users_data[username].get('daily_missions', [])
        from config.settings import DAILY_MISSIONS
        
        # Get the missions actually displayed to the user (first 3)
        displayed_missions = DAILY_MISSIONS[:3]
        total_missions = len(displayed_missions)
        
        # Count how many of the displayed missions are completed
        displayed_completed = [m for m in completed_missions if any(m == dm['title'] for dm in displayed_missions)]
        completed_count = len(displayed_completed)
        
        # Get the user's current streak
        streak = users_data[username].get('mission_streak', 0)
        
        return {
            'completed_ids': completed_missions,  # List of completed mission IDs (titles)
            'completed': completed_count,         # Count of completed missions
            'total': total_missions,
            'progress': (completed_count / total_missions) * 100 if total_missions > 0 else 0,
            'streak': streak
        }
    return {'completed_ids': [], 'completed': 0, 'total': 0, 'progress': 0, 'streak': 0}