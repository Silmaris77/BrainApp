import streamlit as st
import uuid
from datetime import datetime

def show_notification(message, type="success", duration=3):
    """Show a notification message to the user"""
    notification_id = str(uuid.uuid4())
    
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []
    
    notification = {
        'id': notification_id,
        'message': message,
        'type': type,
        'created_at': datetime.now().timestamp(),
        'duration': duration
    }
    
    st.session_state.notifications.append(notification)
    
    # Generuj HTML dla powiadomienia
    color = {
        'success': '#27ae60',
        'error': '#e74c3c',
        'info': '#2980b9',
        'warning': '#f1c40f'
    }.get(type, '#2980b9')
    
    st.markdown(f"""
        <div class="notification" style="background-color: {color};" id="notification-{notification_id}">
            {message}
        </div>
        <script>
            setTimeout(function() {{
                document.getElementById('notification-{notification_id}').style.opacity = '0';
                setTimeout(function() {{
                    document.getElementById('notification-{notification_id}').remove();
                }}, 300);
            }}, {duration * 1000});
        </script>
    """, unsafe_allow_html=True)

def show_achievement_notification(achievement_name, xp_gained=0):
    """Show a special notification for achieved goals or badges"""
    message = f"🎉 Osiągnięcie odblokowane: {achievement_name}"
    if xp_gained > 0:
        message += f" (+{xp_gained} XP)"
    
    st.markdown(f"""
        <div class="notification achievement" style="background-color: #8e44ad;">
            {message}
            <div class="confetti-container"></div>
        </div>
        <script>
            // Dodaj efekt confetti
            function createConfetti() {{
                const colors = ['#f1c40f', '#e74c3c', '#2ecc71', '#3498db'];
                const confettiContainer = document.querySelector('.confetti-container');
                
                for (let i = 0; i < 50; i++) {{
                    const confetti = document.createElement('div');
                    confetti.className = 'confetti';
                    confetti.style.left = Math.random() * 100 + '%';
                    confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                    confetti.style.animationDelay = Math.random() * 3 + 's';
                    confettiContainer.appendChild(confetti);
                }}
            }}
            createConfetti();
        </script>
    """, unsafe_allow_html=True)