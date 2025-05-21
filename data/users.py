import json
import os
import uuid
from datetime import datetime

def save_user_data(users_data):
    """Save user data to JSON file"""
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users_data.json')
    with open(file_path, 'w') as f:
        json.dump(users_data, f)

def load_user_data():
    """Load user data from JSON file"""
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users_data.json')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return {}

def register_user(username, password, password_confirm):
    """Register a new user"""
    users_data = load_user_data()
    if username in users_data:
        return "Username already taken!"
    elif password != password_confirm:
        return "Passwords do not match!"
    elif not username or not password:
        return "Username and password are required!"
    else:
        user_id = str(uuid.uuid4())
        users_data[username] = {
            "user_id": user_id,
            "password": password,
            "degen_type": None,
            "xp": 0,
            "level": 1,
            "joined_date": datetime.now().strftime("%Y-%m-%d"),
            "completed_lessons": [],
            "badges": [],
            "test_taken": False
        }
        save_user_data(users_data)
        return "Registration successful!"

def login_user(username, password):
    """Login a user"""
    users_data = load_user_data()
    if username in users_data and users_data[username]["password"] == password:
        return users_data[username]
    return None

def update_user_xp(username, xp_amount):
    """Update user's XP and level"""
    users_data = load_user_data()
    if username in users_data:
        users_data[username]["xp"] += xp_amount
        save_user_data(users_data)
        return True
    return False

def update_single_user_field(username, field_name, field_value):
    """Update a single field in a user's data"""
    users_data = load_user_data()
    if username in users_data:
        users_data[username][field_name] = field_value
        save_user_data(users_data)
        return True
    return False