from data.users import load_user_data, save_user_data
from config.settings import USER_AVATARS, THEMES

def update_user_avatar(username, avatar_id):
    """Update user's avatar"""
    if avatar_id not in USER_AVATARS:
        return False
    
    users_data = load_user_data()
    if username in users_data:
        users_data[username]['avatar'] = avatar_id
        save_user_data(users_data)
        return True
    return False

def update_user_theme(username, theme_id):
    """Update user's theme"""
    if theme_id not in THEMES:
        return False
    
    users_data = load_user_data()
    if username in users_data:
        users_data[username]['theme'] = theme_id
        save_user_data(users_data)
        return True
    return False

def get_user_style(username):
    """Get user's current style settings"""
    users_data = load_user_data()
    if username in users_data:
        user_data = users_data[username]
        theme_id = user_data.get('theme', 'default')
        avatar_id = user_data.get('avatar', 'default')
        
        return {
            'theme': THEMES[theme_id],
            'avatar': USER_AVATARS[avatar_id]
        }
    return {
        'theme': THEMES['default'],
        'avatar': USER_AVATARS['default']
    }

def generate_user_css(username):
    """Generate custom CSS based on user's theme"""
    style = get_user_style(username)
    theme = style['theme']
    theme_id = 'default'  # Default theme ID
      # Find the theme_id based on the theme values
    for tid, t in THEMES.items():
        if t == theme:
            theme_id = tid
            break
    
    return f"""
    <style>
        :root {{
            --primary-color: {theme['primary']};
            --secondary-color: {theme['secondary']};
            --accent-color: {theme['accent']};
            --background-color: {theme['background']};
            --card-color: {theme['card']};
        }}
        
        .progress-bar {{
            background: var(--primary-color);
            transition: width 0.3s ease-in-out;
        }}
        
        .btn-zen {{
            background: var(--primary-color);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .btn-zen:hover {{
            background: var(--secondary-color);
            transform: translateY(-2px);
        }}
        
        .degen-card {{
            background: var(--card-color);
            border: 1px solid rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        
        .degen-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        }}
        
        .notification {{
            background: var(--primary-color);
        }}
        
        .achievement.notification {{
            background: var(--accent-color);
        }}
        
        .badge {{
            background: var(--secondary-color);
        }}
        
        .confetti {{
            background: var(--accent-color);
        }}
        
        /* Dark theme adjustments */
        {'''
        @media (prefers-color-scheme: dark) {
            .degen-card {
                background: var(--card-color);
                border-color: rgba(255,255,255,0.1);
            }
            body {
                background: var(--background-color);
                color: white;
            }
        }
        ''' if 'dark' in theme_id else ''}
    </style>
    """