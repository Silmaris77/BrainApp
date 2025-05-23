import streamlit as st
import pandas as pd
import random
import numpy as np
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time

# Import danych

from data.users import load_user_data, save_user_data

from config.settings import USER_AVATARS, THEMES, BADGES

# Import nowego systemu UI
from utils.ui import initialize_ui
from utils.ui.components.interactive import zen_button, notification
from utils.ui.components.text import content_section, zen_header, tip_block
from utils.ui.components.cards import stat_card, profile_card
from utils.ui.components.progress import progress_bar
from utils.ui.layouts.grid import responsive_grid, responsive_container
from utils.ui.layouts.responsive import get_device_type, get_responsive_figure_size

# Import funkcji pomocniczych
from utils.personalization import (
    update_user_avatar,
    update_user_theme,
    get_user_style,
    generate_user_css
)
from utils.goals import (
    add_user_goal,
    update_goal_progress,
    delete_goal,
    get_user_goals,
    calculate_goal_metrics
)
from utils.inventory import (
    activate_item,
    get_user_inventory,
    is_booster_active,
    format_time_remaining
)

from views.dashboard_ui import calculate_xp_progress
from views.neuroleader_test import plot_radar_chart
from data.neuroleader_types import NEUROLEADER_TYPES

def show_profile():
    """
    Wyświetla profil użytkownika używając nowego systemu UI zgodnego z CSP
    """
    # Inicjalizacja UI
    initialize_ui()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    num_columns = 1 if device_type == 'mobile' else 2
    
    zen_header("Profil użytkownika")
    
    # Wczytaj dane użytkownika
    users_data = load_user_data()
    username = st.session_state.get('username')
    
    # Sprawdź czy username jest stringiem
    if not isinstance(username, str):
        if isinstance(username, list) and len(username) > 0:
            username = username[0]
        elif username is not None:
            username = str(username)
        else:
            username = ""
            
    user_data = users_data.get(username, {})
    style = get_user_style(username)
    
    # Wyświetl personalizowane style
    st.markdown(generate_user_css(username), unsafe_allow_html=True)
    
    # Setup data for user stats panel

    level = user_data.get('level', 1)
    xp = user_data.get('xp', 0)
    completed = len(user_data.get('completed_lessons', []))
    
    # Calculate XP data
    xp_progress, xp_needed = calculate_xp_progress(user_data)
    
    # Display user stats using the new UI components
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            stat_card(level, "Poziom", "📊")
        with col2:
            stat_card(xp, "Punkty XP", "⭐")
        with col3:
            stat_card(completed, "Ukończone lekcje", "📚")
            
        progress_bar(xp_progress, f"{xp_needed} XP do poziomu {level + 1}")
    
    # Create tabs
    tab_options = ["Personalizacja", "Ekwipunek", "Odznaki", "Typ Neuroliderera"]
    
    if 'profile_tab' not in st.session_state:
        st.session_state.profile_tab = "Personalizacja"
    
    # Create tab buttons
    tab_cols = st.columns(len(tab_options))
    for i, tab in enumerate(tab_options):
        with tab_cols[i]:
            if st.button(
                tab,
                key=f"tab_{tab}",
                on_click=lambda t=tab: set_profile_tab(t)
            ):
                pass  # Obsłużone przez funkcję on_click
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Display content based on selected tab
    if st.session_state.profile_tab == "Personalizacja":
        show_personalization_tab(username, user_data, device_type, num_columns)
    elif st.session_state.profile_tab == "Ekwipunek":
        show_inventory_tab(username, device_type, num_columns)
    elif st.session_state.profile_tab == "Odznaki":
        show_badges_tab(user_data, device_type, num_columns)
    elif st.session_state.profile_tab == "Typ Neuroliderera":
        show_neuroleader_type_tab(user_data, device_type, num_columns)


def set_profile_tab(tab):
    """Ustawia aktywną zakładkę profilu"""
    st.session_state.profile_tab = tab
    
# Funkcje pomocnicze dla poszczególnych zakładek...
def show_personalization_tab(username, user_data, device_type, num_columns):
    zen_header("Personalizacja profilu")
    
    cols = st.columns(num_columns)
    
    with cols[0]:
        st.subheader("🎭 Wybierz avatar")
        current_avatar = user_data.get('avatar', 'default')
        avatar_options = list(USER_AVATARS.keys())
        selected_avatar = st.selectbox(
            "Wybierz swojego avatara:",
            options=avatar_options,
            format_func=lambda x: f"{USER_AVATARS[x]} - {x.title()}",
            index=avatar_options.index(current_avatar) if current_avatar in avatar_options else 0
        )
        
        if zen_button("Zapisz avatar", key="save_avatar_btn"):
            if update_user_avatar(username, selected_avatar):
                notification("Avatar został zaktualizowany!", type="success")
                st.rerun()
    
    with cols[1 if num_columns > 1 else 0]:
        st.subheader("🎨 Wybierz motyw")
        current_theme = user_data.get('theme', 'default')
        theme_options = list(THEMES.keys())
        selected_theme = st.selectbox(
            "Wybierz motyw:",
            options=theme_options,
            format_func=lambda x: x.replace('_', ' ').title(),
            index=theme_options.index(current_theme) if current_theme in theme_options else 0
        )
        
        if zen_button("Zapisz motyw", key="save_theme_btn"):
            if update_user_theme(username, selected_theme):
                notification("Motyw został zaktualizowany!", type="success")
                st.rerun()

def show_inventory_tab(username, device_type, num_columns):
    zen_header("Twój ekwipunek")
    
    # Get user inventory
    inventory = get_user_inventory(username)
    
    if not inventory:
        st.info("Twój ekwipunek jest pusty. Zdobądź przedmioty w sklepie!")
    else:
        # Create responsive grid
        items_per_row = num_columns
        total_items = len(inventory)
        total_rows = (total_items + items_per_row - 1) // items_per_row
        
        for row in range(total_rows):
            cols = st.columns(items_per_row)
            for col in range(items_per_row):
                idx = row * items_per_row + col
                if idx < total_items:
                    item_id = list(inventory.keys())[idx]
                    item_data = inventory[item_id]
                    
                    with cols[col]:
                        # Sprawdź, jakiego typu jest item_data i obsłuż odpowiednio
                        if isinstance(item_data, dict):
                            # Jeśli item_data to słownik, użyj metody get()
                            icon = item_data.get('icon', '🎁')
                            name = item_data.get('name', 'Przedmiot')
                            description = item_data.get('description', 'Brak opisu')
                            item_type = item_data.get('type', 'Zwykły')
                            bonus = item_data.get('bonus', '0')
                            quantity = item_data.get('quantity', 1)
                        elif isinstance(item_data, list) and len(item_data) >= 5:
                            # Jeśli item_data to lista, dostęp przez indeksy
                            icon = item_data[0] if len(item_data) > 0 else '🎁'
                            name = item_data[1] if len(item_data) > 1 else 'Przedmiot'
                            description = item_data[2] if len(item_data) > 2 else 'Brak opisu'
                            item_type = item_data[3] if len(item_data) > 3 else 'Zwykły'
                            bonus = item_data[4] if len(item_data) > 4 else '0'
                            quantity = item_data[5] if len(item_data) > 5 else 1
                        else:
                            # Domyślne wartości, jeśli format danych jest nieznany
                            icon = '🎁'
                            name = f'Przedmiot {item_id}'
                            description = 'Brak opisu'
                            item_type = 'Zwykły'
                            bonus = '0'
                            quantity = 1
                        
                        st.subheader(f"{icon} {name}")
                        st.markdown(f"{description}")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown(f"**Typ:** {item_type}")
                        with col2:
                            st.markdown(f"**Bonus:** {bonus}%")
                        with col3:
                            st.markdown(f"**Ilość:** {quantity}")
                        
                        # Check if the item is active
                        is_active, expiration_str = is_booster_active(username, item_id)
                        
                        # Te warunki powinny być wewnątrz bloku "with cols[col]:"
                        if is_active:
                            remaining_time = format_time_remaining(expiration_str)
                            st.success(f"Aktywny - Pozostały czas: {remaining_time}")
                        else:
                            if zen_button(f"Aktywuj", key=f"activate_btn_{item_id}"):
                                # Określ typ przedmiotu
                                item_type = "booster"  # lub pobierz prawidłowy typ z danych przedmiotu
                                
                                # Wywołaj funkcję z trzema parametrami
                                success, message = activate_item(username, item_type, item_id)
                                
                                if success:
                                    notification(f"Przedmiot {name} został aktywowany!", type="success")
                                else:
                                    notification(message, type="error")
                                
                                st.rerun()

def show_badges_tab(user_data, device_type, num_columns):
    zen_header("Twoje odznaki")
    
    # Get user badges
    user_badges = user_data.get('badges', [])
    
    # Zdefiniuj badges_per_row na samym początku funkcji
    badges_per_row = num_columns
    
    if not user_badges:
        st.info("Nie masz jeszcze odznak. Wykonuj zadania i zdobywaj osiągnięcia, aby odblokować odznaki!")
    else:
        st.subheader("Zdobyte odznaki")
        
        # Usuń tę linię, bo teraz badges_per_row jest zdefiniowane wcześniej
        # badges_per_row = num_columns
        
        for i in range(0, len(user_badges), badges_per_row):
            cols = st.columns(badges_per_row)
            for j in range(badges_per_row):
                if i + j < len(user_badges):
                    badge_id = user_badges[i + j]
                    if badge_id in BADGES:
                        badge_data = BADGES[badge_id]
                        with cols[j]:
                            st.markdown(f"### {badge_data.get('icon', '🏅')} {badge_data.get('name', 'Odznaka')}")
                            st.markdown(f"{badge_data.get('description', 'Brak opisu')}")
                            st.caption(f"Zdobyta: {user_data.get('badge_dates', {}).get(badge_id, 'Nieznana data')}")
    
    # Show available badges
    st.markdown("---")
    st.subheader("Dostępne odznaki")
    
    available_badges = [badge_id for badge_id in BADGES if badge_id not in user_badges]
    
    if not available_badges:
        st.success("Gratulacje! Zdobyłeś wszystkie dostępne odznaki.")
    else:
        # Teraz badges_per_row jest zawsze zdefiniowane
        for i in range(0, len(available_badges), badges_per_row):
            cols = st.columns(badges_per_row)
            for j in range(badges_per_row):
                if i + j < len(available_badges):
                    badge_id = available_badges[i + j]
                    badge_data = BADGES[badge_id]
                    with cols[j]:
                        st.markdown(f"### {badge_data.get('icon', '🏅')} {badge_data.get('name', 'Odznaka')}")
                        st.markdown(f"{badge_data.get('description', 'Brak opisu')}")
                        st.caption(f"**Wymagania:** {badge_data.get('requirement', 'Nieznane')}")

def show_neuroleader_type_tab(user_data, device_type, num_columns):
    """Wyświetla zakładkę z typem Neuroliderera"""
    zen_header("Twój typ neuroliderera")
    
    # Pobierz dane dotyczące typu neuroliderera
    neuroleader_type = user_data.get('neuroleader_type', None)
    neuroleader_scores = user_data.get('neuroleader_scores', {})
    
    if not neuroleader_type or not neuroleader_scores:
        st.warning("Nie wykonałeś jeszcze testu typu neuroliderera.")
        if zen_button("Wykonaj test", key="take_neuroleader_test_btn"):
            st.session_state.page = 'neuroleader_test'
            st.rerun()
    else:
        # Nagłówek wyników
        st.subheader(f"Twój dominujący typ: {neuroleader_type}")
        if neuroleader_type in NEUROLEADER_TYPES:
            st.markdown(f"{NEUROLEADER_TYPES[neuroleader_type].get('description', 'Brak opisu')}")
        
        # Wykres wyników
        st.subheader("Twoje wyniki na wykresie")
        fig = plot_radar_chart(neuroleader_scores, device_type)
        st.pyplot(fig)
        
        # Szczegóły typu
        cols = st.columns(num_columns)
        
        # Mocne strony
        with cols[0]:
            st.subheader("💪 Twoje mocne strony")
            if neuroleader_type in NEUROLEADER_TYPES and "strengths" in NEUROLEADER_TYPES[neuroleader_type]:
                for strength in NEUROLEADER_TYPES[neuroleader_type]["strengths"]:
                    st.markdown(f"✅ {strength}")
            else:
                st.info("Brak danych o mocnych stronach.")
        
        # Wyzwania
        with cols[1 if num_columns > 1 else 0]:
            st.subheader("🚧 Twoje wyzwania")
            if neuroleader_type in NEUROLEADER_TYPES and "challenges" in NEUROLEADER_TYPES[neuroleader_type]:
                for challenge in NEUROLEADER_TYPES[neuroleader_type]["challenges"]:
                    st.markdown(f"⚠️ {challenge}")
            else:
                st.info("Brak danych o wyzwaniach.")
        
        # Strategia
        st.subheader("🎯 Zalecana strategia")
        if neuroleader_type in NEUROLEADER_TYPES and "strategy" in NEUROLEADER_TYPES[neuroleader_type]:
            st.markdown(f"{NEUROLEADER_TYPES[neuroleader_type]['strategy']}")
        else:
            st.info("Brak zalecanej strategii.")
        
        # Szczegółowy opis
        if neuroleader_type in NEUROLEADER_TYPES and "detailed_description" in NEUROLEADER_TYPES[neuroleader_type]:
            st.subheader("📑 Szczegółowy opis typu")
            st.markdown(NEUROLEADER_TYPES[neuroleader_type]["detailed_description"])
        
        # Przycisk do ponownego wykonania testu
        if zen_button("Wykonaj test ponownie", key="retake_neuroleader_test_btn"):
            st.session_state.page = 'neuroleader_test'
            if 'test_step' in st.session_state:
                del st.session_state['test_step']
            if 'test_scores' in st.session_state:
                del st.session_state['test_scores']
            st.rerun()


