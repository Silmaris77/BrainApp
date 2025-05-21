import streamlit as st
import random
import altair as alt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from data.users import load_user_data, save_user_data
from data.test_questions import DEGEN_TYPES
from config.settings import DAILY_MISSIONS, XP_LEVELS, USER_AVATARS
from data.lessons import load_lessons
from utils.goals import get_user_goals, calculate_goal_metrics
from utils.daily_missions import get_daily_missions_progress
from views.degen_test import plot_radar_chart
from utils.material3_components import apply_material3_theme
from utils.layout import get_device_type, responsive_grid, responsive_container, toggle_device_view
from utils.components import (
    zen_header, mission_card, degen_card, progress_bar, stat_card, 
    xp_level_display, zen_button, notification, leaderboard_item, 
    add_animations_css, data_chart, user_stats_panel, lesson_card
)

def calculate_xp_progress(user_data):
    """Calculate XP progress and dynamically determine the user's level"""
    # Dynamically determine the user's level based on XP
    for level, xp_threshold in sorted(XP_LEVELS.items(), reverse=True):
        if user_data['xp'] >= xp_threshold:
            user_data['level'] = level
            break

    # Calculate progress to the next level
    next_level = user_data['level'] + 1
    if next_level in XP_LEVELS:
        current_level_xp = XP_LEVELS[user_data['level']]
        next_level_xp = XP_LEVELS[next_level]
        xp_needed = next_level_xp - current_level_xp
        xp_progress = user_data['xp'] - current_level_xp
        xp_percentage = min(100, int((xp_progress / xp_needed) * 100))
        return xp_percentage, xp_needed - xp_progress

    return 100, 0

def get_top_users(limit=5):
    """Get top users by XP"""
    users_data = load_user_data()
    leaderboard = []
    
    for username, data in users_data.items():
        leaderboard.append({
            'username': username,
            'level': data.get('level', 1),
            'xp': data.get('xp', 0)
        })
    
    # Sort by XP (descending)
    leaderboard.sort(key=lambda x: x['xp'], reverse=True)
    return leaderboard[:limit]

def get_user_rank(username):
    """Get user rank in the leaderboard"""
    users_data = load_user_data()
    leaderboard = []
    
    for user, data in users_data.items():
        leaderboard.append({
            'username': user,
            'xp': data.get('xp', 0)
        })
    
    # Sort by XP (descending)
    leaderboard.sort(key=lambda x: x['xp'], reverse=True)
    
    # Find user rank
    for i, user in enumerate(leaderboard):
        if user['username'] == username:
            return {'rank': i + 1, 'xp': user['xp']}
    
    return {'rank': 0, 'xp': 0}

def get_user_xp_history(username, days=30):
    """Simulate XP history data (for now)"""
    # This would normally come from a database
    # For now, we'll generate fictional data
    history = []
    today = datetime.now()
    
    # Generate data points for the last X days
    xp = load_user_data().get(username, {}).get('xp', 0)
    daily_increment = max(1, int(xp / days))
    
    for i in range(days):
        date = today - timedelta(days=days-i)
        history.append({
            'date': date.strftime('%Y-%m-%d'),
            'xp': max(0, int(xp * (i+1) / days))
        })
    
    return history

def display_lesson_cards(lessons_list, tab_name="", custom_columns=None):
    """Display lesson cards in a responsive layout
    
    Args:
        lessons_list: Dictionary of lessons to display
        tab_name: Name of the tab to use for creating unique button keys
        custom_columns: Optional pre-defined columns for responsive layout
    """
    if not lessons_list:
        st.info("Brak dostępnych lekcji w tej kategorii.")
        return
    
    users_data = load_user_data()
    user_data = users_data.get(st.session_state.username, {})
      # Jeśli nie dostarczono niestandardowych kolumn, użyj jednej kolumny na całą szerokość
    if custom_columns is None:
        # Zawsze używaj jednej kolumny na całą szerokość
        custom_columns = [st.container()]
    
    # Display lessons in the responsive grid
    for i, (lesson_id, lesson) in enumerate(lessons_list.items()):
        # Get lesson properties
        difficulty = lesson.get('difficulty', 'intermediate')
        is_completed = lesson_id in user_data.get('completed_lessons', [])# Przygotuj symbol trudności
        if difficulty == "beginner":
            difficulty_symbol = "🟢"
        elif difficulty == "intermediate":
            difficulty_symbol = "🟠"
        else:
            difficulty_symbol = "🔴"
          # Użyj zawsze pierwszej kolumny, bo teraz mamy tylko jedną kolumnę
        with custom_columns[0]:
            # Użyj komponentu lesson_card dla spójności z widokiem lekcji
            lesson_card(
                title=lesson.get('title', 'Lekcja'),
                description=lesson.get('description', 'Ta lekcja wprowadza podstawowe zasady...'),
                xp=lesson.get('xp_reward', 30),
                difficulty=difficulty,
                category=lesson.get('tag', ''),
                completed=is_completed,
                button_text="Powtórz lekcję" if is_completed else "Rozpocznij",
                button_key=f"{tab_name}_start_{lesson_id}_{i}",
                lesson_id=lesson_id,
                on_click=lambda lesson_id=lesson_id: (
                    setattr(st.session_state, 'current_lesson', lesson_id),
                    setattr(st.session_state, 'page', 'lesson'),
                    st.rerun()
                )
        )

def get_recommended_lessons(username):
    """Get recommended lessons based on user type"""
    lessons = load_lessons()
    users_data = load_user_data()
    user_data = users_data.get(username, {})
    degen_type = user_data.get('degen_type', None)
    
    # If user has a degen type, filter lessons to match
    if degen_type:
        return {k: v for k, v in lessons.items() if v.get('recommended_for', None) == degen_type}
    
    # Otherwise, return a small selection of beginner lessons
    return {k: v for k, v in lessons.items() if v.get('difficulty', 'medium') == 'beginner'}

def get_popular_lessons():
    """Get most popular lessons based on completion count"""
    # Dla symulanty, zwracamy standardowe lekcje z modyfikatorem "popular"
    # aby zapewnić unikalność kluczy lekcji między różnymi kategoriami
    lessons = load_lessons()
    return lessons

def get_newest_lessons():
    """Get newest lessons"""
    # Dla symulanty, zwracamy standardowe lekcje z modyfikatorem "newest"
    # aby zapewnić unikalność kluczy lekcji między różnymi kategoriami
    lessons = load_lessons()
    return lessons

def get_daily_missions(username):
    """Get daily missions for user"""
    # For now, use the missions from settings
    # We're only showing the first 3 missions to the user
    return DAILY_MISSIONS[:3]

def show_dashboard():
    # Zastosuj style Material 3
    apply_material3_theme()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    # Używamy naszego komponentu nagłówka
    zen_header("Dashboard Degena")
    
    # Dodajemy animacje CSS
    add_animations_css()

    users_data = load_user_data()
    user_data = users_data[st.session_state.username]    # WIERSZ 1: Profil użytkownika i profil inwestycyjny w dwóch kolumnach
    st.markdown("<div class='st-bx fadeIn delay-1'>", unsafe_allow_html=True)
    
    # Responsywny układ kolumn, dostosowany do urządzenia
    if device_type == 'mobile':
        profile_cols = st.columns(1)  # Na telefonie jedna kolumna
        profile_col = profile_cols[0]
        investor_profile_col = profile_cols[0]
    else:
        profile_col, investor_profile_col = st.columns(2)  # Na większych ekranach dwie kolumny
    
    # 1a. PROFIL UŻYTKOWNIKA (kolumna 1)
    with profile_col:
        st.subheader("Profil użytkownika")
        
        # Avatar i typ degena
        user_avatar = USER_AVATARS.get(user_data.get('avatar', 'default'), '👤')
        degen_type = user_data.get('degen_type', 'Nie określono')
        
        # Pasek postępu XP do następnego poziomu
        xp = user_data.get('xp', 0)
        xp_progress, xp_needed = calculate_xp_progress(user_data)
        next_level = user_data.get('level', 1) + 1
        next_level_xp = XP_LEVELS.get(next_level, xp + xp_needed)
        
        # Używamy komponentu user_stats_panel
        user_stats_panel(
            username=st.session_state.username,
            avatar=user_avatar,
            degen_type=degen_type,
            level=user_data.get('level', 1),
            xp=xp,
            completed_lessons=len(user_data.get('completed_lessons', [])),
            next_level_xp=next_level_xp
        )
    
    # 1b. PROFIL INWESTYCYJNY (kolumna 2)
    with investor_profile_col:
        st.subheader("Twój profil inwestycyjny")
        
        if 'test_scores' in user_data:
            radar_fig = plot_radar_chart(user_data['test_scores'])
            st.pyplot(radar_fig)
        elif not user_data.get('test_taken', False):
            st.info("Wykonaj test Degena, aby odkryć swój profil inwestycyjny")
            if zen_button("Wykonaj test Degena"):
                st.session_state.page = 'degen_test'
                st.rerun()
        else:
            st.info("Twój profil inwestycyjny jest jeszcze niekompletny")
    
    st.markdown("</div>", unsafe_allow_html=True)
      # WIERSZ 2: Dostępne lekcje w pełnej szerokości
    st.markdown("<div class='st-bx fadeIn delay-2'>", unsafe_allow_html=True)
    st.subheader("Dostępne lekcje")
      # Zamiast zakładek, wyświetl wszystkie lekcje bez podziału na kategorie
    lessons = load_lessons()
    
    # Zawsze używamy jednej kolumny na całą szerokość
    display_lesson_cards(lessons, "all_lessons")

    st.markdown("</div>", unsafe_allow_html=True)
      # WIERSZ 3: Misje dnia (bez rankingu XP)
    st.markdown("<div class='st-bx fadeIn delay-3'>", unsafe_allow_html=True)
    
    # 3. MISJE DNIA (pełna szerokość)
    st.subheader("Misje dnia")
    
    # Get daily missions and progress
    daily_missions = get_daily_missions(st.session_state.username)
    missions_progress = get_daily_missions_progress(st.session_state.username)
    
    # Overall progress indicator
    progress_percentage = missions_progress['progress']
    
    # Add streak indicator
    streak = missions_progress['streak']
    streak_html = ""
    if streak > 0:
        streak_html = f"""
        <div class="streak-container">
            <div class="streak-badge">🔥 {streak} dni</div>
            <div class="streak-label">Twoja seria</div>
        </div>
        """
    
    # Show overall progress
    st.markdown(f"Ukończono: {missions_progress['completed']}/{missions_progress['total']} ({int(progress_percentage)}%)")
    progress_bar(missions_progress['completed'] / missions_progress['total'])
    
    if daily_missions:
        # Użyj responsywnej siatki dla misji
        mission_cols = responsive_grid(columns_desktop=3, columns_tablet=2, columns_mobile=1)
        
        for idx, mission in enumerate(daily_missions):
            # Check if mission is completed
            is_completed = mission['title'] in missions_progress['completed_ids']
              # Umieść misję w odpowiedniej kolumnie responsywnej siatki
            col_index = idx % len(mission_cols)
            with mission_cols[col_index]:
                # Używamy komponentu mission_card
                mission_card(
                    title=mission['title'], 
                    description=mission['description'], 
                    badge_emoji=mission['badge'], 
                    xp=mission['xp'],
                    progress=100 if is_completed else 0,
                    completed=is_completed
                )
                
                # Complete button (only if not completed) - moved inside column context
                if not is_completed:
                    if zen_button("Ukończ misję", key=f"complete_{mission['title'].replace(' ', '_')}"):
                        from utils.daily_missions import complete_daily_mission
                        complete_success = complete_daily_mission(st.session_state.username, mission['title'])
                        
                        if complete_success:
                            # Create a success message
                            notification(f"Misja '{mission['title']}' została ukończona! +{mission['xp']} XP", type="success")
                            st.rerun()
            
        if zen_button("Odśwież misje", key="refresh_missions"):
            st.rerun()
    else:
        st.info("Nie masz dostępnych misji na dziś.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # WIERSZ 4: Wykres postępu i Ranking XP w dwóch kolumnach
    st.markdown("<div class='st-bx fadeIn delay-4'>", unsafe_allow_html=True)
    progress_col, leaderboard_col = st.columns(2)
    
    # 4a. WYKRES POSTĘPU
    with progress_col:
        st.subheader("Twój postęp")
        
        # Wykres trendu XP przy użyciu komponentu data_chart
        history = get_user_xp_history(st.session_state.username)
        if history:
            chart_data = pd.DataFrame(history)
            data_chart(
                data=chart_data,
                chart_type="area",
                title="Rozwój XP w czasie",
                x_label="Data",
                y_label="Punkty XP",
                height=300
            )
        else:
            st.info("Brak danych o historii XP. Zacznij swój pierwszy kurs!")
    
    # 4b. RANKING XP (przeniesiony z wiersza 3)
    with leaderboard_col:
        st.subheader("Ranking XP")
        
        # Pobierz najlepszych graczy
        top_users = get_top_users(5)  # Top 5 użytkowników
        
        for i, user in enumerate(top_users):
            leaderboard_item(
                rank=i+1,
                username=user['username'],
                points=user['xp'],
                is_current_user=user['username'] == st.session_state.username
            )
        
        # Pozycja bieżącego użytkownika
        current_user_rank = get_user_rank(st.session_state.username)
        
        # Wyświetl pozycję użytkownika tylko jeśli nie jest w top 5
        if current_user_rank['rank'] > 5:
            st.markdown("---")
            leaderboard_item(
                rank=current_user_rank['rank'],
                username=st.session_state.username,
                points=current_user_rank['xp'],
                is_current_user=True
            )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Dodaj sekcję wyzwań tygodniowych w dashboardzie
    st.markdown("<div class='st-bx fadeIn delay-5'>", unsafe_allow_html=True)
    st.subheader("Wyzwania tygodniowe 🏆")

    weekly_challenges = [
        {
            'title': 'Maratończyk wiedzy',
            'description': 'Ukończ 5 lekcji w tym tygodniu',
            'current': len(user_data.get('this_week_lessons', [])),
            'target': 5,
            'reward': '250 XP',
            'expires': '3 dni'
        },
        {
            'title': 'Geniusz inwestycyjny',
            'description': 'Odpowiedz poprawnie na 15 pytań quizowych',
            'current': user_data.get('weekly_correct_answers', 0),
            'target': 15,
            'reward': 'Odblokowanie specjalnej lekcji',
            'expires': '3 dni'
        }
    ]

    for challenge in weekly_challenges:
        progress = min(100, int((challenge['current'] / challenge['target']) * 100))
        completed = progress == 100
        
        mission_card(
            title=challenge['title'], 
            description=f"{challenge['description']} (Wygasa za: {challenge['expires']})", 
            badge_emoji='🏆', 
            xp=challenge['reward'],
            progress=progress,
            completed=completed
        )

    st.markdown("</div>", unsafe_allow_html=True)
    
    # Sekcja promująca rozwój umiejętności
    st.markdown("""
    <div class="feature-card">
        <h3>🌳 Rozwijaj swoje umiejętności</h3>
        <p>Ulepszaj swoje umiejętności inwestycyjne i odblokuj nowe możliwości.</p>
    </div>
    """, unsafe_allow_html=True)

    if zen_button("Przejdź do drzewa umiejętności", key="goto_skills"):
        st.session_state.page = "skills"
        st.rerun()

    # Admin button for admin users
    admin_users = ["admin", "zenmaster"]  # Lista administratorów
    if st.session_state.get('username') in admin_users:
        st.markdown("---")
        if zen_button("🛡️ Panel administratora", key="admin_panel"):
            st.session_state.page = 'admin'
            st.rerun()
