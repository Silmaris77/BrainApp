import streamlit as st
import random
import altair as alt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from data.users import load_user_data, save_user_data
from data.test_questions import DEGEN_TYPES
from data.neuroleader_types import NEUROLEADER_TYPES  # Import neuroleader types
from config.settings import DAILY_MISSIONS, XP_LEVELS, USER_AVATARS
from data.lessons import load_lessons
from utils.goals import get_user_goals, calculate_goal_metrics
from utils.daily_missions import get_daily_missions_progress
from views.degen_test import plot_radar_chart as plot_degen_radar_chart
from views.neuroleader_test import plot_radar_chart as plot_neuroleader_radar_chart  # Import neuroleader radar chart
from utils.material3_components import apply_material3_theme
from utils.layout import get_device_type, responsive_grid, responsive_container, toggle_device_view
from utils.card_layout import load_card_layout, create_card, create_grid, zen_section, data_panel  # Import new card layout utils
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

def display_lesson_cards(lessons_list, tab_name="", card_layout=False):
    """Display lesson cards in a responsive layout
    
    Args:
        lessons_list: Dictionary of lessons to display
        tab_name: Name of the tab to use for creating unique button keys
        card_layout: Whether to use the new card layout or traditional lessons
    """
    if not lessons_list:
        st.info("Brak dostępnych lekcji w tej kategorii.")
        return
    
    users_data = load_user_data()
    user_data = users_data.get(st.session_state.username, {})
    
    # Create a grid for the cards if using card layout
    device_type = get_device_type()
    columns = create_grid(1 if device_type == 'mobile' else 2) if card_layout else [st.container()]
    
    # Display lessons in the grid or as regular lesson cards
    for i, (lesson_id, lesson) in enumerate(lessons_list.items()):
        # Get lesson properties
        difficulty = lesson.get('difficulty', 'intermediate')
        is_completed = lesson_id in user_data.get('completed_lessons', [])
        
        # Prepare difficulty symbol
        if difficulty == "beginner":
            difficulty_symbol = "🟢"
        elif difficulty == "intermediate":
            difficulty_symbol = "🟠"
        else:
            difficulty_symbol = "🔴"
        
        # Determine column for grid layout
        col_idx = i % len(columns) if card_layout else 0
        
        with columns[col_idx]:
            if card_layout:
                # Use new card component
                create_card(
                    title=lesson.get('title', 'Lekcja'),
                    icon=difficulty_symbol,
                    content=f"""
                    <p>{lesson.get('description', 'Ta lekcja wprowadza podstawowe zasady...')}</p>
                    <p><strong>Kategoria:</strong> {lesson.get('tag', 'Ogólna')}</p>
                    <p><strong>Nagroda:</strong> {lesson.get('xp_reward', 30)} XP</p>
                    <p><strong>Status:</strong> {'✅ Ukończono' if is_completed else '⏳ Nieukończona'}</p>
                    """,
                    footer_content=f"""
                    <button class="zen-button">{("Powtórz lekcję" if is_completed else "Rozpocznij")}</button>
                    """,
                    key=f"card_{tab_name}_{lesson_id}_{i}",
                    on_click=lambda lesson_id=lesson_id: (
                        setattr(st.session_state, 'current_lesson', lesson_id),
                        setattr(st.session_state, 'page', 'lesson'),
                        st.rerun()
                    )
                )
            else:
                # Use traditional lesson card
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
    # Load card layout CSS only (no Material 3 theme for card layout)
    load_card_layout()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    # Używamy naszego komponentu nagłówka
    zen_header("Dashboard Neuroliderzy")
    
    # Dodajemy animacje CSS
    add_animations_css()

    users_data = load_user_data()
    user_data = users_data[st.session_state.username]
    
    # Określ liczbę kolumn w zależności od urządzenia
    num_columns = 1 if device_type == 'mobile' else 2
    
    # SEKCJA: PROFIL UŻYTKOWNIKA
    zen_section("Profil użytkownika", "Twoja droga jako neurolider", "👤")
    
    # Układ dwukolumnowy dla profilu i kart
    profile_col, stats_col = st.columns([1, 1]) if device_type != 'mobile' else [st.container(), st.container()]
    
    with profile_col:
        # Avatar i typ użytkownika
        user_avatar = USER_AVATARS.get(user_data.get('avatar', 'default'), '👤')
        degen_type = user_data.get('degen_type', 'Nie określono')
        neuroleader_type = user_data.get('neuroleader_type', 'Nie określono')
        
        # Pasek postępu XP do następnego poziomu
        xp = user_data.get('xp', 0)
        xp_progress, xp_needed = calculate_xp_progress(user_data)
        next_level = user_data.get('level', 1) + 1
        next_level_xp = XP_LEVELS.get(next_level, xp + xp_needed)
        
        # Informacje o użytkowniku w karcie
        create_card(
            title="Twoje dane",
            icon="👤",
            content=f"""
            <div style="padding: 10px 0;">
                <div style="font-size: 3rem; text-align: center; margin-bottom: 10px;">{user_avatar}</div>
                <p><strong>Poziom:</strong> {user_data.get('level', 1)}</p>
                <p><strong>Doświadczenie:</strong> {xp} XP (do następnego poziomu: {xp_needed} XP)</p>
                <p><strong>Typ inwestycyjny:</strong> {degen_type}</p>
                <p><strong>Typ neuroliderera:</strong> {neuroleader_type}</p>
            </div>
            <div class="progress-container" style="margin: 15px 0;">
                <div class="progress-bar" style="width: {xp_progress}%; height: 8px; background-color: #4CAF50; border-radius: 4px;"></div>
            </div>
            """,
            key="user_profile_card"
        )
    
    with stats_col:
        # Statystyki użytkownika w karcie
        completed_lessons = len(user_data.get('completed_lessons', []))
        total_lessons = len(load_lessons())
        completion_pct = int((completed_lessons / max(1, total_lessons)) * 100)
        
        create_card(
            title="Twój postęp",
            icon="📊",
            content=f"""
            <div style="padding: 10px 0;">
                <p><strong>Ukończone lekcje:</strong> {completed_lessons}/{total_lessons} ({completion_pct}%)</p>
                <p><strong>Wykonane testy:</strong> {2 if 'test_scores' in user_data and 'neuroleader_test_scores' in user_data else 1 if 'test_scores' in user_data or 'neuroleader_test_scores' in user_data else 0}/2</p>
                <p><strong>Zdobyte odznaki:</strong> {len(user_data.get('badges', []))}</p>
                <p><strong>Pozycja w rankingu:</strong> #{get_user_rank(st.session_state.username)['rank']}</p>
            </div>
            <div class="progress-container" style="margin: 15px 0;">
                <div class="progress-bar" style="width: {completion_pct}%; height: 8px; background-color: #4CAF50; border-radius: 4px;"></div>
            </div>
            """,
            key="user_stats_card"
        )

    # SEKCJA: PROFILE TESTÓW
    zen_section("Twoje profile testów", "Wyniki wykonanych testów", "🧪")
    
    # Create tabs for the test profiles
    tab1, tab2 = st.tabs(["Profil Inwestycyjny", "Profil Neuroliderera"])
        
    with tab1:
        if 'test_scores' in user_data:
            try:
                radar_fig = plot_degen_radar_chart(user_data['test_scores'])
                st.pyplot(radar_fig)
                
                # Add card with test details
                degen_type = user_data.get('degen_type', 'Nie określono')
                if degen_type in DEGEN_TYPES:
                    create_card(
                        title=f"Profil inwestycyjny: {degen_type}",
                        icon="📈",
                        content=f"""
                        <p>{DEGEN_TYPES[degen_type].get('description', '')}</p>
                        <h4>Mocne strony:</h4>
                        <ul>
                            {"".join([f"<li>{s}</li>" for s in DEGEN_TYPES[degen_type].get('strengths', [])])}
                        </ul>
                        <h4>Wyzwania:</h4>
                        <ul>
                            {"".join([f"<li>{c}</li>" for c in DEGEN_TYPES[degen_type].get('challenges', [])])}
                        </ul>
                        """,
                        key="degen_profile_details"
                    )
            except:
                st.error("Wystąpił problem z wizualizacją profilu inwestycyjnego.")
        elif not user_data.get('test_taken', False):
            create_card(
                title="Wykonaj test profilu inwestycyjnego",
                icon="🧪",
                content="Poznaj swój profil inwestycyjny, aby otrzymać spersonalizowane rekomendacje i dostosowane ścieżki nauki.",
                footer_content='<button class="zen-button">Wykonaj test</button>',
                key="take_degen_test",
                on_click=lambda: (
                    setattr(st.session_state, 'page', 'degen_test'),
                    st.rerun()
                )
            )
        else:
            st.info("Twój profil inwestycyjny jest jeszcze niekompletny")
    
    with tab2:
        if 'neuroleader_test_scores' in user_data:
            try:
                radar_fig = plot_neuroleader_radar_chart(user_data['neuroleader_test_scores'])
                st.pyplot(radar_fig)
                
                # Add card with test details
                neuroleader_type = user_data.get('neuroleader_type', 'Nie określono')
                if neuroleader_type in NEUROLEADER_TYPES:
                    create_card(
                        title=f"Profil neuroliderera: {neuroleader_type}",
                        icon="🧠",
                        content=f"""
                        <p>{NEUROLEADER_TYPES[neuroleader_type].get('description', '')}</p>
                        <h4>Mocne strony:</h4>
                        <ul>
                            {"".join([f"<li>{s}</li>" for s in NEUROLEADER_TYPES[neuroleader_type].get('strengths', [])])}
                        </ul>
                        <h4>Wyzwania:</h4>
                        <ul>
                            {"".join([f"<li>{c}</li>" for c in NEUROLEADER_TYPES[neuroleader_type].get('challenges', [])])}
                        </ul>
                        """,
                        key="neuroleader_profile_details"
                    )
            except:
                st.error("Wystąpił problem z wizualizacją profilu neuroliderera.")
        elif not user_data.get('neuroleader_test_taken', False):
            create_card(
                title="Wykonaj test profilu neuroliderera",
                icon="🧠",
                content="Poznaj swój styl przywództwa neurobiologicznego, aby efektywnie rozwijać swoje kompetencje liderskie.",
                footer_content='<button class="zen-button">Wykonaj test</button>',
                key="take_neuroleader_test",
                on_click=lambda: (
                    setattr(st.session_state, 'page', 'neuroleader_test'),
                    st.rerun()
                )
            )
        else:
            st.info("Twój profil neuroleaderski jest jeszcze niekompletny")
    
    # SEKCJA: DOSTĘPNE LEKCJE
    zen_section("Dostępne lekcje", "Poszerzaj swoją wiedzę i rozwijaj umiejętności", "📚")
    
    # Get all lessons
    lessons = load_lessons()
    
    # Display lesson cards in a grid layout
    display_lesson_cards(lessons, "all_lessons", card_layout=True)
    
    # SEKCJA: MISJE DNIA
    zen_section("Misje dnia", "Wykonuj codzienne zadania i zdobywaj punkty doświadczenia", "🎯")
    
    # Get daily missions and progress
    daily_missions = get_daily_missions(st.session_state.username)
    missions_progress = get_daily_missions_progress(st.session_state.username)
    
    # Overall progress indicator
    progress_percentage = missions_progress['progress']
    
    # Add streak indicator
    streak = missions_progress['streak']
    
    # Create a card for overall mission progress
    create_card(
        title=f"Postęp misji dziennych",
        icon="📊",
        content=f"""
        <div style="padding: 10px 0;">
            <p><strong>Ukończono:</strong> {missions_progress['completed']}/{missions_progress['total']} ({int(progress_percentage)}%)</p>
            {"<p><strong>Twoja seria:</strong> 🔥 " + str(streak) + " dni</p>" if streak > 0 else ""}
        </div>
        <div class="progress-container" style="margin: 15px 0;">
            <div class="progress-bar" style="width: {progress_percentage}%; height: 8px; background-color: #4CAF50; border-radius: 4px;"></div>
        </div>
        """,
        key="missions_progress_card"
    )
    
    if daily_missions:
        # Create responsive grid for missions
        mission_cols = create_grid(num_columns)
        
        # Display mission cards
        for idx, mission in enumerate(daily_missions):
            # Check if mission is completed
            is_completed = mission['title'] in missions_progress['completed_ids']
            
            # Add to appropriate column
            col_idx = idx % len(mission_cols)
            with mission_cols[col_idx]:
                create_card(
                    title=mission['title'],
                    icon=mission['badge'],
                    content=f"""
                    <p>{mission['description']}</p>
                    <p><strong>Nagroda:</strong> {mission['xp']} XP</p>
                    <div class="progress-container" style="margin: 15px 0;">
                        <div class="progress-bar" style="width: {100 if is_completed else 0}%; height: 8px; background-color: {'#4CAF50' if is_completed else '#ccc'}; border-radius: 4px;"></div>
                    </div>
                    <p><strong>Status:</strong> {"✅ Ukończone" if is_completed else "⏳ W trakcie"}</p>
                    """,
                    footer_content=f"""
                    <button class="zen-button" {'disabled="disabled" style="opacity: 0.5;"' if is_completed else ''}>{("Ukończone" if is_completed else "Ukończ misję")}</button>
                    """,
                    key=f"mission_{mission['title'].replace(' ', '_')}",
                    on_click=None if is_completed else lambda mission_title=mission['title']: (
                        complete_daily_mission(st.session_state.username, mission_title),
                        st.rerun()
                    )
                )
        
        # Add refresh button
        st.button("Odśwież misje", key="refresh_missions", on_click=st.rerun)
    else:
        st.info("Nie masz dostępnych misji na dziś.")
    
    # SEKCJA: POSTĘP I RANKING
    if device_type != 'mobile':  # Show this section only on desktop and tablet
        zen_section("Statystyki i ranking", "Śledź swój postęp i porównuj się z innymi", "📈")
        
        # Create two columns for progress chart and leaderboard
        progress_col, leaderboard_col = st.columns(2)
        
        # Progress Chart
        with progress_col:
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
        
        # Leaderboard
        with leaderboard_col:
            # Get top users
            top_users = get_top_users(5)  # Top 5 users
            
            for i, user in enumerate(top_users):
                leaderboard_item(
                    rank=i+1,
                    username=user['username'],
                    points=user['xp'],
                    is_current_user=user['username'] == st.session_state.username
                )
            
            # Get current user rank
            current_user_rank = get_user_rank(st.session_state.username)
            
            # Show current user position if not in top 5
            if current_user_rank['rank'] > 5:
                st.markdown("---")
                leaderboard_item(
                    rank=current_user_rank['rank'],
                    username=st.session_state.username,
                    points=current_user_rank['xp'],
                    is_current_user=True
                )

    # Admin access
    admin_users = ["admin", "zenmaster"]  # List of administrators
    if st.session_state.get('username') in admin_users:
        st.markdown("---")
        if zen_button("🛡️ Panel administratora", key="admin_panel"):
            st.session_state.page = 'admin'
            st.rerun()

# Helper function available in the scope
def complete_daily_mission(username, mission_title):
    """Complete a daily mission for the user"""
    from utils.daily_missions import complete_daily_mission as cdm
    success = cdm(username, mission_title)
    
    if success:
        # Find the mission to get XP reward
        for mission in DAILY_MISSIONS:
            if mission['title'] == mission_title:
                st.success(f"Misja '{mission_title}' została ukończona! +{mission['xp']} XP")
                break
    
    return success
