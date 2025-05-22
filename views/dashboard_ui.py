import streamlit as st
import random
import altair as alt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from data.users import load_user_data, save_user_data
from data.test_questions import DEGEN_TYPES
from data.neuroleader_types import NEUROLEADER_TYPES
from config.settings import DAILY_MISSIONS, XP_LEVELS, USER_AVATARS
from data.lessons import load_lessons
from utils.goals import get_user_goals, calculate_goal_metrics
from utils.daily_missions import get_daily_missions_progress
from views.degen_test import plot_radar_chart as plot_degen_radar_chart
from views.neuroleader_test import plot_radar_chart as plot_neuroleader_radar_chart

# Import nowego systemu UI
from utils.ui import initialize_ui
from utils.ui.components.interactive import zen_button, notification
from utils.ui.components.text import content_section, zen_header
from utils.ui.layouts.grid import responsive_grid, render_dashboard_header
from utils.ui.components.cards import stat_card

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

def display_lesson_cards(lessons_list, tab_name=""):
    """Display lesson cards in a responsive layout
    
    Args:
        lessons_list: Dictionary of lessons to display
        tab_name: Name of the tab to use for creating unique button keys
    """
    if not lessons_list:
        st.info("Brak dostępnych lekcji w tej kategorii.")
        return
    
    users_data = load_user_data()
    user_data = users_data.get(st.session_state.username, {})
    
    # Create a responsive grid for the lessons
    cols = responsive_grid(columns_desktop=2, columns_tablet=2, columns_mobile=1)
    
    # Display lessons in the grid
    for i, (lesson_id, lesson) in enumerate(lessons_list.items()):
        # Get lesson properties
        difficulty = lesson.get('difficulty', 'intermediate')
        is_completed = lesson_id in user_data.get('completed_lessons', [])
        
        # Prepare difficulty symbol
        if difficulty == "beginner":
            difficulty_symbol = "🟢"
            difficulty_text = "Początkujący"
        elif difficulty == "intermediate":
            difficulty_symbol = "🟠"
            difficulty_text = "Średniozaawansowany"
        else:
            difficulty_symbol = "🔴"
            difficulty_text = "Zaawansowany"
        
        # Use responsive grid
        with cols[i % len(cols)]:
            # Lekcja jako karta
            st.markdown(f"""
            <div style="padding: 20px; background-color: rgba(255, 255, 255, 0.05); 
                    border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #3498db;">
                <h3>{lesson.get('title', 'Lekcja')} {difficulty_symbol}</h3>
                <p>{lesson.get('description', 'Ta lekcja wprowadza podstawowe zasady...')}</p>
                <p><strong>Kategoria:</strong> {lesson.get('tag', 'Ogólna')}</p>
                <p><strong>Poziom:</strong> {difficulty_text}</p>
                <p><strong>Nagroda:</strong> {lesson.get('xp_reward', 30)} XP</p>
                <p><strong>Status:</strong> {'✅ Ukończono' if is_completed else '⏳ Nieukończona'}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Przycisk rozpoczęcia lekcji używający zen_button
            if zen_button(("Powtórz lekcję" if is_completed else "Rozpocznij"), 
                         key=f"{tab_name}_start_{lesson_id}_{i}"):
                st.session_state.current_lesson = lesson_id
                st.session_state.page = 'lesson'
                st.rerun()

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
    """Get newest lessons based on date added"""
    # Dla symulanty, zwracamy standardowe lekcje z modyfikatorem "newest"
    # aby zapewnić unikalność kluczy lekcji między różnymi kategoriami
    lessons = load_lessons()
    return lessons

def show_dashboard():
    # Inicjalizacja UI
    initialize_ui()
    
    # Pobierz dane użytkownika - upewnij się, że username jest stringiem
    username = st.session_state.get('username')
    if isinstance(username, list) and len(username) > 0:
        username = username[0]
    elif not isinstance(username, str) and username is not None:
        username = str(username)
    
    users_data = load_user_data()
    user_data = users_data.get(username, {}) if username else {}
    
    # Nagłówek dashboardu
    render_dashboard_header("Dashboard Neuroliderów", f"Witaj, {st.session_state.username}! 👋")

    # Dane dla sekcji statystyk
    xp_percentage, xp_to_next_level = calculate_xp_progress(user_data)
    user_rank = get_user_rank(st.session_state.username)
    daily_missions_progress = get_daily_missions_progress(st.session_state.username)
    user_goals = get_user_goals(st.session_state.username)
    goal_metrics = calculate_goal_metrics(user_goals)
    stats = user_data.get('statistics', {
        'lessons_completed': len(user_data.get('completed_lessons', [])),
        'missions_completed': daily_missions_progress['completed'],
        'current_streak': user_data.get('current_streak', 0),
        'goals_achieved': goal_metrics['completed']
    })
    
    # Sekcja statystyk użytkownika
    st.header("Twoje statystyki")
      # Użyj responsive_grid dla kart statystyk
    stats_cols = responsive_grid(columns_desktop=4, columns_tablet=2, columns_mobile=2)
    
    with stats_cols[0]:
        st.markdown(f"""
        <div style="padding: 15px; background-color: rgba(255, 255, 255, 0.05); border-radius: 10px; text-align: center;">
            <div style="font-size: 16px; color: #aaa;">Poziom</div>
            <div style="font-size: 28px; margin: 10px 0;">⭐ {user_data.get('level', 1)}</div>
            <div style="font-size: 14px;">{xp_percentage}% do poziomu {user_data.get('level', 1) + 1}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_cols[1]:
        st.markdown(f"""
        <div style="padding: 15px; background-color: rgba(255, 255, 255, 0.05); border-radius: 10px; text-align: center;">
            <div style="font-size: 16px; color: #aaa;">Ukończone lekcje</div>
            <div style="font-size: 28px; margin: 10px 0;">📚 {stats.get('lessons_completed', 0)}</div>
            <div style="font-size: 14px;">Łącznie</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_cols[2]:
        st.markdown(f"""
        <div style="padding: 15px; background-color: rgba(255, 255, 255, 0.05); border-radius: 10px; text-align: center;">
            <div style="font-size: 16px; color: #aaa;">Pozycja w rankingu</div>
            <div style="font-size: 28px; margin: 10px 0;">🏆 {user_rank.get('rank', 0)}</div>
            <div style="font-size: 14px;">z {len(users_data)} użytkowników</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_cols[3]:
        st.markdown(f"""
        <div style="padding: 15px; background-color: rgba(255, 255, 255, 0.05); border-radius: 10px; text-align: center;">
            <div style="font-size: 16px; color: #aaa;">Seria logowań</div>
            <div style="font-size: 28px, margin: 10px 0;">🔥 {stats.get('current_streak', 0)}</div>
            <div style="font-size: 14px;">dni</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Karty profilu
    st.header("Twój profil")
    
    profile_cols = responsive_grid(columns_desktop=2, columns_tablet=2, columns_mobile=1)
    
    # Lewy panel - Profil/XP
    with profile_cols[0]:
        content_section(
            title="Postęp w doświadczeniu",
            content=f"""
            <div style='margin-bottom: 10px'>
                <span style='font-size: 24px'>⭐ Poziom {user_data.get('level', 1)}</span>
                <span style='float: right'>XP: {user_data.get('xp', 0)}</span>
            </div>
            <div style='height: 10px; background-color: rgba(255,255,255,0.1); border-radius: 5px;'>
                <div style='height: 10px; width: {xp_percentage}%; background-color: #4CAF50; border-radius: 5px;'></div>
            </div>
            <div style='text-align: right; margin-top: 5px'>{xp_to_next_level} XP do poziomu {user_data.get('level', 1) + 1}</div>
            """
        )        # Wyświetl wykresy Degen i Neurolider
        content_section(
            title="Twój profil Degena",
            content=""
        )
        
        if 'degen_scores' in user_data and user_data['degen_scores']:
            # Użyj plot_degen_radar_chart do wyświetlenia wykresu
            fig = plot_degen_radar_chart(user_data['degen_scores'])
            st.pyplot(fig)
            
        content_section(
            title="Twój profil Neuroleader",
            content=""
        )
        
        if 'neuroleader_scores' in user_data and user_data['neuroleader_scores']:
            # Użyj plot_neuroleader_radar_chart do wyświetlenia wykresu
            fig = plot_neuroleader_radar_chart(user_data['neuroleader_scores'])
            st.pyplot(fig)
      # Prawy panel - Misje dzienne i cele
    with profile_cols[1]:
        content_section(
            title="Misje dzienne",
            content=""
        )
        
        # Wyświetl misje dzienne
        for mission_id, mission_data in enumerate(DAILY_MISSIONS):
            mission_key = mission_data.get('id', f'mission_{mission_id}')
            mission_progress = daily_missions_progress.get(mission_key, 
                                {'complete': False, 
                                 'progress': 0, 
                                 'target': mission_data.get('target', 1)})
            progress_pct = int((mission_progress['progress'] / mission_progress['target']) * 100)
            
            st.markdown(f"""
            <div style='margin-bottom: 15px;'>
                <div>
                    <span style='font-weight: bold;'>{mission_data.get('description', 'Misja dzienna')}</span>
                    <span style='float: right;'>{mission_progress['progress']}/{mission_progress['target']}</span>
                </div>
                <div style='height: 10px; background-color: rgba(255,255,255,0.1); border-radius: 5px; margin-top: 5px;'>
                    <div style='height: 10px; width: {progress_pct}%; 
                         background-color: {"#4CAF50" if mission_progress["complete"] else "#2196F3"}; 
                         border-radius: 5px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Wyświetl cele użytkownika
        content_section(
            title="Twoje cele",
            content=""
        )
        
        if not user_goals:
            st.info("Nie ustawiłeś jeszcze żadnych celów.")
        else:
            for goal in user_goals:
                # Używamy metody get() dla wszystkich kluczy, aby uniknąć KeyError
                current = goal.get('current', 0)
                target = goal.get('target', 1)
                title = goal.get('title', 'Cel bez nazwy')
                complete = goal.get('complete', False)
                
                progress_pct = int((current / target) * 100) if target > 0 else 0
                
                st.markdown(f"""
                <div style='margin-bottom: 15px;'>
                    <div>
                        <span style='font-weight: bold;'>{title}</span>
                        <span style='float: right;'>{current}/{target}</span>
                    </div>
                    <div style='height: 10px; background-color: rgba(255,255,255,0.1); border-radius: 5px; margin-top: 5px;'>
                        <div style='height: 10px; width: {progress_pct}%; 
                             background-color: {"#4CAF50" if complete else "#2196F3"}; 
                             border-radius: 5px;'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Lekcje i rankingi
    
    # Sekcja z zakładkami
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Rekomendowane", "🔥 Popularne", "🆕 Nowe lekcje", "🏆 Ranking"])
    
    with tab1:
        st.markdown("### Rekomendowane lekcje")
        st.markdown("Te lekcje zostały specjalnie wybrane na podstawie Twojego profilu Degena.")
        
        recommended_lessons = get_recommended_lessons(st.session_state.username)
        display_lesson_cards(recommended_lessons, "recommended")
    
    with tab2:
        st.markdown("### Najpopularniejsze lekcje")
        st.markdown("Lekcje, które są najczęściej wybierane przez innych Neuroliderów.")
        
        popular_lessons = get_popular_lessons()
        display_lesson_cards(popular_lessons, "popular")
    
    with tab3:
        st.markdown("### Najnowsze lekcje")
        st.markdown("Najnowsze lekcje dodane do platformy Neuroliderów.")
        
        newest_lessons = get_newest_lessons()
        display_lesson_cards(newest_lessons, "newest")
    
    with tab4:
        st.markdown("### Ranking Neuroliderów")
        st.markdown("Sprawdź jak wypadasz na tle innych uczestników programu.")
        
        # Top users leaderboard
        leaderboard = get_top_users(10)
        for i, user in enumerate(leaderboard):
            st.markdown(f"""
            <div style='padding: 10px; background-color: {"rgba(255,215,0,0.1)" if user["username"] == st.session_state.username else "rgba(255,255,255,0.05)"}; 
                    border-radius: 5px; margin-bottom: 10px; display: flex; align-items: center;'>
                <div style='width: 30px; font-weight: bold;'>#{i+1}</div>
                <div style='flex-grow: 1; margin-left: 10px;'>{user["username"]}</div>
                <div style='width: 80px; text-align: right;'>⭐ Lvl {user["level"]}</div>
                <div style='width: 100px; text-align: right;'>{user["xp"]} XP</div>
            </div>
            """, unsafe_allow_html=True)

# Funkcje specjalne dla interfejsu
def show_view_button(text, icon, page, key):
    if zen_button(f"{icon} {text}", key=key):
        st.session_state.page = page
        st.rerun()
