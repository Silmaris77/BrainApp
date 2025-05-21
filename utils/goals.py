from datetime import datetime
from data.users import load_user_data, save_user_data
from utils.notifications import show_notification, show_achievement_notification

def update_goal_progress(username, goal_id, progress):
    """Update progress of a specific goal"""
    users_data = load_user_data()
    if username not in users_data or 'goals' not in users_data[username]:
        return False
    
    for goal in users_data[username]['goals']:
        if goal['id'] == goal_id:
            old_progress = goal['progress']
            goal['progress'] = progress
            goal['completed'] = progress >= 100
            
            if goal['completed'] and not old_progress >= 100:
                # Cel został właśnie ukończony
                show_achievement_notification(f"Cel ukończony: {goal['title']}", 100)
                users_data[username]['xp'] = users_data[username].get('xp', 0) + 100
            elif progress > old_progress:
                # Postęp w celu
                show_notification(
                    f"🎯 Zaktualizowano postęp celu: {goal['title']} ({progress}%)",
                    "info"
                )
            
            save_user_data(users_data)
            return True
    return False

def add_user_goal(username, goal_title, goal_description, target_date, goal_type):
    """Add a new learning goal for the user"""
    users_data = load_user_data()
    if username not in users_data:
        return False
    
    if 'goals' not in users_data[username]:
        users_data[username]['goals'] = []
    
    goal_id = len(users_data[username]['goals'])
    
    new_goal = {
        'id': goal_id,
        'title': goal_title,
        'description': goal_description,
        'target_date': target_date,
        'type': goal_type,
        'created_at': datetime.now().strftime("%Y-%m-%d"),
        'completed': False,
        'progress': 0
    }
    
    users_data[username]['goals'].append(new_goal)
    save_user_data(users_data)
    
    show_notification(
        f"🎯 Dodano nowy cel: {goal_title}",
        "success"
    )
    return True

def delete_goal(username, goal_id):
    """Delete a specific goal"""
    users_data = load_user_data()
    if username not in users_data or 'goals' not in users_data[username]:
        return False
    
    # Znajdź cel przed usunięciem
    goal_title = None
    for goal in users_data[username]['goals']:
        if goal['id'] == goal_id:
            goal_title = goal['title']
            break
    
    users_data[username]['goals'] = [
        goal for goal in users_data[username]['goals'] 
        if goal['id'] != goal_id
    ]
    save_user_data(users_data)
    
    if goal_title:
        show_notification(
            f"🗑️ Usunięto cel: {goal_title}",
            "info"
        )
    return True

def get_user_goals(username):
    """Get all goals for a user"""
    users_data = load_user_data()
    if username in users_data:
        return users_data[username].get('goals', [])
    return []

def calculate_goal_metrics(username):
    """Calculate metrics related to user's goals"""
    goals = get_user_goals(username)
    total_goals = len(goals)
    completed_goals = sum(1 for goal in goals if goal['completed'])
    active_goals = sum(1 for goal in goals if not goal['completed'])
    avg_progress = sum(goal['progress'] for goal in goals) / total_goals if total_goals > 0 else 0
    
    return {
        'total': total_goals,
        'completed': completed_goals,
        'active': active_goals,
        'avg_progress': avg_progress
    }