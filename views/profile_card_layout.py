import streamlit as st
import pandas as pd
import random
import re
import os
import numpy as np
import json
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
from data.test_questions import DEGEN_TYPES
from data.users import load_user_data, save_user_data, update_single_user_field
from PIL import Image
from utils.components import zen_header, zen_button, notification, content_section, tip_block
from utils.material3_components import apply_material3_theme
from utils.layout import get_device_type, responsive_grid, responsive_container, toggle_device_view, apply_responsive_styles, get_responsive_figure_size
from utils.card_layout import load_card_layout, create_card, create_grid, zen_section, data_panel

from datetime import datetime, timedelta
import time
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
from config.settings import USER_AVATARS, THEMES, DEGEN_TYPES, BADGES
from data.degen_details import degen_details
from views.degen_test import plot_radar_chart
from views.dashboard import calculate_xp_progress
from utils.components import zen_header, zen_button, notification, content_section, stat_card, xp_level_display, goal_card, badge_card, progress_bar, tip_block, quote_block, add_animations_css
from utils.user_components import user_stats_panel

def show_profile():
    # Zastosuj style Material 3
    
    # Zastosuj responsywne style
    apply_responsive_styles()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    # Determine the layout grid size based on device type
    num_columns = 1 if device_type == 'mobile' else 2
    
    zen_header("Profil użytkownika")
    
    # Wczytaj dane użytkownika
    users_data = load_user_data()
    user_data = users_data.get(st.session_state.username, {})
    style = get_user_style(st.session_state.username)
    
    # Wyświetl personalizowane style
    st.markdown(generate_user_css(st.session_state.username), unsafe_allow_html=True)
    
    # Add animations and effects using the component
    add_animations_css()
    
    # Setup data for user stats panel
    avatar = style['avatar']
    degen_type = user_data.get('degen_type', 'Typ nie określony')
    level = user_data.get('level', 1)
    xp = user_data.get('xp', 0)
    completed = len(user_data.get('completed_lessons', []))
    
    # Calculate XP data
    xp_progress, xp_needed = calculate_xp_progress(user_data)
    next_level_xp = xp + xp_needed  # Estimated XP for next level
    
    # Display user stats card
    create_card(
        title="Statystyki użytkownika",
        icon=USER_AVATARS.get(avatar, "👤"),
        content=f"""
        <div class="user-stats-card">
            <div class="user-stats-header">
                <h2>{st.session_state.username}</h2>
                <div class="user-type" style="color: {DEGEN_TYPES.get(degen_type, {}).get('color', '#333')};">
                    {degen_type}
                </div>
            </div>
            <div class="user-stats-grid">
                <div class="stat-item">
                    <div class="stat-value">{level}</div>
                    <div class="stat-label">Poziom</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{xp}</div>
                    <div class="stat-label">Punkty XP</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{completed}</div>
                    <div class="stat-label">Ukończone lekcje</div>
                </div>
            </div>
            <div class="xp-progress">
                <div class="xp-bar">
                    <div class="xp-fill" style="width: {xp_progress}%;"></div>
                </div>
                <div class="xp-text">
                    {xp_needed} XP do poziomu {level + 1}
                </div>
            </div>
        </div>
        <style>
            .user-stats-card {
                padding: 0.5rem 0;
            }
            .user-stats-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
            }
            .user-stats-header h2 {
                margin: 0;
                font-size: 1.5rem;
            }
            .user-type {
                font-weight: 500;
                padding: 0.3rem 0.8rem;
                border-radius: 1rem;
                background-color: rgba(0,0,0,0.05);
            }
            .user-stats-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 1rem;
                margin-bottom: 1rem;
            }
            .stat-item {
                text-align: center;
                padding: 0.8rem;
                background-color: rgba(0,0,0,0.02);
                border-radius: 0.5rem;
            }
            .stat-value {
                font-size: 1.5rem;
                font-weight: 600;
                color: var(--primary-color);
            }
            .stat-label {
                font-size: 0.85rem;
                color: #666;
                margin-top: 0.3rem;
            }
            .xp-progress {
                margin-top: 1rem;
            }
            .xp-bar {
                height: 0.5rem;
                background-color: rgba(0,0,0,0.1);
                border-radius: 0.25rem;
                overflow: hidden;
                margin-bottom: 0.5rem;
            }
            .xp-fill {
                height: 100%;
                background-color: var(--primary-color);
            }
            .xp-text {
                font-size: 0.85rem;
                color: #666;
                text-align: right;
            }
        </style>
        """,
        key="user_stats_card"
    )
    
    # Create tabs using cards
    zen_section("Profil", "Zarządzaj swoim profilem", icon="👤")
    
    # Tab selector
    tab_options = ["Personalizacja", "Ekwipunek", "Odznaki", "Typ Degena"]
    
    if 'profile_tab' not in st.session_state:
        st.session_state.profile_tab = "Personalizacja"
    
    # Create tab buttons
    tab_cols = st.columns(len(tab_options))
    for i, tab in enumerate(tab_options):
        with tab_cols[i]:
            if st.button(
                tab,
                key=f"tab_{tab}",
                type="secondary" if st.session_state.profile_tab == tab else "primary"
            ):
                st.session_state.profile_tab = tab
                st.rerun()
    
    st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)
    
    # Display content based on selected tab
    if st.session_state.profile_tab == "Personalizacja":
        # Personalization section
        zen_section("Personalizacja profilu", "Dostosuj swój profil", icon="🎨")
        
        # Create a grid of columns for personalization options
        cols = create_grid(num_columns)
        
        # Avatar Selection Card
        with cols[0]:
            create_card(
                title="Wybierz avatar",
                icon="😎",
                content="""
                <p>Kliknij, aby wybrać swój avatar:</p>
                <div class="avatar-grid" id="avatar-grid">
                </div>
                <style>
                    .avatar-grid {
                        display: grid;
                        grid-template-columns: repeat(4, 1fr);
                        gap: 0.8rem;
                        margin: 1rem 0;
                    }
                    .avatar-option {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        padding: 0.8rem;
                        border-radius: 0.5rem;
                        cursor: pointer;
                        transition: all 0.2s;
                    }
                    .avatar-option:hover {
                        background-color: rgba(0,0,0,0.05);
                        transform: translateY(-2px);
                    }
                    .avatar-emoji {
                        font-size: 2rem;
                        margin-bottom: 0.5rem;
                    }
                    .avatar-name {
                        font-size: 0.8rem;
                        text-align: center;
                    }
                    .avatar-selected {
                        background-color: rgba(var(--primary-color-rgb), 0.1);
                        border: 1px solid var(--primary-color);
                    }
                </style>
                """,
                key="avatar_card"
            )
            
            # We still need a form to submit the selection
            current_avatar = user_data.get('avatar', 'default')
            selected_avatar = st.selectbox(
                "Wybierz swojego avatara:",
                options=list(USER_AVATARS.keys()),
                format_func=lambda x: f"{USER_AVATARS[x]} - {x.title()}",
                index=list(USER_AVATARS.keys()).index(current_avatar)
            )
            
            # Add JavaScript to dynamically populate the avatar grid
            avatar_js = """
            <script>
                const avatarGrid = document.getElementById('avatar-grid');
                const avatars = {
            """
            
            for avatar_id, avatar_emoji in USER_AVATARS.items():
                avatar_js += f"    '{avatar_id}': '{avatar_emoji}',\n"
            
            avatar_js += """
                };
                
                // Current selected avatar
                const currentAvatar = '""" + current_avatar + """';
                
                // Create avatar options
                for (const [id, emoji] of Object.entries(avatars)) {
                    const isSelected = id === currentAvatar;
                    const div = document.createElement('div');
                    div.className = `avatar-option ${isSelected ? 'avatar-selected' : ''}`;
                    div.innerHTML = `
                        <div class="avatar-emoji">${emoji}</div>
                        <div class="avatar-name">${id.charAt(0).toUpperCase() + id.slice(1)}${isSelected ? ' ✓' : ''}</div>
                    `;
                    avatarGrid.appendChild(div);
                }
            </script>
            """
            
            st.markdown(avatar_js, unsafe_allow_html=True)
            
            if zen_button("Zapisz avatar", key="save_avatar"):
                if update_user_avatar(st.session_state.username, selected_avatar):
                    notification("Avatar został zaktualizowany!", type="success")
                    st.rerun()
        
        # Theme Selection Card
        with cols[1 if num_columns > 1 else 0]:
            create_card(
                title="Wybierz motyw",
                icon="🎨",
                content="""
                <div class="theme-grid" id="theme-grid">
                </div>
                <style>
                    .theme-grid {
                        display: grid;
                        grid-template-columns: repeat(1, 1fr);
                        gap: 0.8rem;
                        margin: 1rem 0;
                    }
                    .theme-option {
                        display: flex;
                        flex-direction: column;
                        padding: 0.8rem;
                        border-radius: 0.5rem;
                        cursor: pointer;
                        transition: all 0.2s;
                        border: 1px solid rgba(0,0,0,0.1);
                    }
                    .theme-option:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    }
                    .theme-name {
                        font-weight: 500;
                        margin-bottom: 0.5rem;
                    }
                    .theme-colors {
                        display: flex;
                        gap: 0.5rem;
                    }
                    .color-sample {
                        width: 25px;
                        height: 25px;
                        border-radius: 50%;
                        border: 1px solid rgba(0,0,0,0.1);
                    }
                    .theme-selected {
                        background-color: rgba(var(--primary-color-rgb), 0.1);
                        border: 1px solid var(--primary-color);
                    }
                </style>
                """,
                key="theme_card"
            )
            
            # We still need a dropdown for selection
            current_theme = user_data.get('theme', 'default')
            selected_theme = st.selectbox(
                "Wybierz motyw:",
                options=list(THEMES.keys()),
                format_func=lambda x: x.replace('_', ' ').title(),
                index=list(THEMES.keys()).index(current_theme)
            )
            
            # Add JavaScript to dynamically populate the theme grid
            theme_js = """
            <script>
                const themeGrid = document.getElementById('theme-grid');
                const themes = {
            """
            
            for theme_id, theme_colors in THEMES.items():
                theme_js += f"""    '{theme_id}': {{
                    primary: '{theme_colors['primary']}',
                    secondary: '{theme_colors['secondary']}',
                    accent: '{theme_colors['accent']}'
                }},\n"""
            
            theme_js += """
                };
                
                // Current selected theme
                const currentTheme = '""" + current_theme + """';
                
                // Create theme options
                for (const [id, colors] of Object.entries(themes)) {
                    const isSelected = id === currentTheme;
                    const div = document.createElement('div');
                    div.className = `theme-option ${isSelected ? 'theme-selected' : ''}`;
                    div.innerHTML = `
                        <div class="theme-name">${id.charAt(0).toUpperCase() + id.slice(1).replace('_', ' ')}${isSelected ? ' ✓' : ''}</div>
                        <div class="theme-colors">
                            <div class="color-sample" style="background-color: ${colors.primary}"></div>
                            <div class="color-sample" style="background-color: ${colors.secondary}"></div>
                            <div class="color-sample" style="background-color: ${colors.accent}"></div>
                        </div>
                    `;
                    themeGrid.appendChild(div);
                }
            </script>
            """
            
            st.markdown(theme_js, unsafe_allow_html=True)
            
            if zen_button("Zapisz motyw", key="save_theme"):
                if update_user_theme(st.session_state.username, selected_theme):
                    notification("Motyw został zaktualizowany!", type="success")
                    st.rerun()
    
    elif st.session_state.profile_tab == "Ekwipunek":
        # Inventory section
        zen_section("Twój ekwipunek", "Zarządzaj swoimi przedmiotami", icon="🎒")
        
        # Get user inventory
        inventory = get_user_inventory(st.session_state.username)
        
        if not inventory:
            create_card(
                title="Pusty ekwipunek",
                icon="📦",
                content="""
                <div style="text-align: center; padding: 2rem 0;">
                    <p>Twój ekwipunek jest pusty. Zdobądź przedmioty w sklepie!</p>
                </div>
                """,
                key="empty_inventory_card"
            )
        else:
            # Create inventory grid
            cols = create_grid(num_columns)
            col_index = 0
            
            for item_id, item_data in inventory.items():
                with cols[col_index % num_columns]:
                    # Check if the item is active
                    is_active = is_booster_active(st.session_state.username, item_id)
                    active_status = ""
                    
                    if is_active:
                        remaining_time = format_time_remaining(st.session_state.username, item_id)
                        active_status = f"""
                        <div class="item-active-status">
                            <span class="active-badge">Aktywny</span>
                            <span class="time-remaining">{remaining_time}</span>
                        </div>
                        """
                    
                    create_card(
                        title=item_data.get('name', 'Przedmiot'),
                        icon=item_data.get('icon', '🎁'),
                        content=f"""
                        <div class="inventory-item">
                            <div class="item-description">
                                {item_data.get('description', 'Brak opisu')}
                            </div>
                            <div class="item-stats">
                                <div class="stat">
                                    <span class="stat-label">Typ:</span>
                                    <span class="stat-value">{item_data.get('type', 'Zwykły')}</span>
                                </div>
                                <div class="stat">
                                    <span class="stat-label">Bonus:</span>
                                    <span class="stat-value">{item_data.get('bonus', '0')}%</span>
                                </div>
                                <div class="stat">
                                    <span class="stat-label">Ilość:</span>
                                    <span class="stat-value">{item_data.get('quantity', 1)}</span>
                                </div>
                            </div>
                            {active_status}
                        </div>
                        <style>
                            .inventory-item {
                                padding: 0.5rem 0;
                            }
                            .item-description {
                                margin-bottom: 1rem;
                                font-size: 0.9rem;
                            }
                            .item-stats {
                                display: grid;
                                grid-template-columns: repeat(3, 1fr);
                                gap: 0.5rem;
                                margin-bottom: 1rem;
                                background-color: rgba(0,0,0,0.02);
                                padding: 0.8rem;
                                border-radius: 0.5rem;
                            }
                            .stat {
                                display: flex;
                                flex-direction: column;
                                align-items: center;
                            }
                            .stat-label {
                                font-size: 0.8rem;
                                color: #666;
                                margin-bottom: 0.3rem;
                            }
                            .stat-value {
                                font-weight: 500;
                            }
                            .item-active-status {
                                display: flex;
                                justify-content: space-between;
                                align-items: center;
                                padding: 0.5rem;
                                background-color: rgba(var(--primary-color-rgb), 0.1);
                                border-radius: 0.5rem;
                                margin-top: 0.5rem;
                            }
                            .active-badge {
                                background-color: var(--primary-color);
                                color: white;
                                padding: 0.2rem 0.5rem;
                                border-radius: 1rem;
                                font-size: 0.8rem;
                                font-weight: 500;
                            }
                            .time-remaining {
                                font-size: 0.8rem;
                                color: #666;
                            }
                        </style>
                        """,
                        footer_content=f"""
                        <button class="zen-button {'disabled' if is_active else ''}" id="activate_{item_id}" {'disabled' if is_active else ''}>
                            {'Aktywny' if is_active else 'Aktywuj'}
                        </button>
                        <style>
                            .zen-button {
                                background-color: var(--primary-color);
                                color: white;
                                border: none;
                                padding: 0.5rem 1rem;
                                border-radius: 0.25rem;
                                cursor: pointer;
                                font-weight: 500;
                                transition: all 0.2s;
                            }
                            .zen-button:hover {
                                filter: brightness(1.1);
                            }
                            .zen-button.disabled {
                                background-color: #ccc;
                                cursor: not-allowed;
                            }
                        </style>
                        """,
                        key=f"inventory_item_{item_id}"
                    )
                    
                    # Only show the activate button if not already active
                    if not is_active:
                        if st.button(f"Aktywuj {item_data.get('name', 'przedmiot')}", key=f"activate_btn_{item_id}"):
                            activate_item(st.session_state.username, item_id)
                            notification(f"Przedmiot {item_data.get('name', '')} został aktywowany!", type="success")
                            st.rerun()
                
                col_index += 1
    
    elif st.session_state.profile_tab == "Odznaki":
        # Badges section
        zen_section("Twoje odznaki", "Sprawdź swoje osiągnięcia", icon="🏆")
        
        # Get user badges
        user_badges = user_data.get('badges', [])
        
        if not user_badges:
            create_card(
                title="Brak odznak",
                icon="🏅",
                content="""
                <div style="text-align: center; padding: 2rem 0;">
                    <p>Nie masz jeszcze odznak. Wykonuj zadania i zdobywaj osiągnięcia, aby odblokować odznaki!</p>
                </div>
                """,
                key="empty_badges_card"
            )
        else:
            # Create badges grid
            cols = create_grid(num_columns)
            col_index = 0
            
            for badge_id in user_badges:
                if badge_id in BADGES:
                    badge_data = BADGES[badge_id]
                    
                    with cols[col_index % num_columns]:
                        create_card(
                            title=badge_data.get('name', 'Odznaka'),
                            icon=badge_data.get('icon', '🏅'),
                            content=f"""
                            <div class="badge-item">
                                <div class="badge-description">
                                    {badge_data.get('description', 'Brak opisu')}
                                </div>
                                <div class="badge-date">
                                    Zdobyta: {user_data.get('badge_dates', {}).get(badge_id, 'Nieznana data')}
                                </div>
                            </div>
                            <style>
                                .badge-item {
                                    padding: 0.5rem 0;
                                    text-align: center;
                                }
                                .badge-description {
                                    margin: 1rem 0;
                                    font-size: 0.9rem;
                                }
                                .badge-date {
                                    font-size: 0.8rem;
                                    color: #666;
                                    font-style: italic;
                                }
                            </style>
                            """,
                            key=f"badge_{badge_id}"
                        )
                    
                    col_index += 1
            
            # Show available badges
            zen_section("Dostępne odznaki", "Odznaki, które możesz zdobyć", icon="🎖️")
            
            cols = create_grid(num_columns)
            col_index = 0
            
            for badge_id, badge_data in BADGES.items():
                if badge_id not in user_badges:
                    with cols[col_index % num_columns]:
                        create_card(
                            title=badge_data.get('name', 'Odznaka'),
                            icon=badge_data.get('icon', '🏅'),
                            content=f"""
                            <div class="badge-item locked">
                                <div class="badge-lock">🔒</div>
                                <div class="badge-description">
                                    {badge_data.get('description', 'Brak opisu')}
                                </div>
                                <div class="badge-requirement">
                                    Wymagania: {badge_data.get('requirement', 'Nieznane')}
                                </div>
                            </div>
                            <style>
                                .badge-item.locked {
                                    padding: 0.5rem 0;
                                    text-align: center;
                                    opacity: 0.7;
                                }
                                .badge-lock {
                                    font-size: 1.5rem;
                                    margin-bottom: 0.5rem;
                                }
                                .badge-description {
                                    margin: 1rem 0;
                                    font-size: 0.9rem;
                                }
                                .badge-requirement {
                                    font-size: 0.8rem;
                                    color: #666;
                                }
                            </style>
                            """,
                            key=f"badge_locked_{badge_id}"
                        )
                    
                    col_index += 1
    
    elif st.session_state.profile_tab == "Typ Degena":
        # Degen type section
        zen_section("Twój typ degena", "Sprawdź swój typ inwestora", icon="🧠")
        
        # Get user degen type
        degen_type = user_data.get('degen_type', None)
        degen_scores = user_data.get('degen_scores', {})
        
        if not degen_type or not degen_scores:
            create_card(
                title="Typ nie określony",
                icon="❓",
                content="""
                <div style="text-align: center; padding: 2rem 0;">
                    <p>Nie wykonałeś jeszcze testu typu degena. Wykonaj test, aby poznać swój typ!</p>
                </div>
                """,
                footer_content="""
                <a href="/?page=degen_test" class="zen-button">Wykonaj test</a>
                <style>
                    .zen-button {
                        display: inline-block;
                        background-color: var(--primary-color);
                        color: white;
                        border: none;
                        padding: 0.5rem 1rem;
                        border-radius: 0.25rem;
                        cursor: pointer;
                        font-weight: 500;
                        transition: all 0.2s;
                        text-decoration: none;
                    }
                    .zen-button:hover {
                        filter: brightness(1.1);
                    }
                </style>
                """,
                key="no_degen_type_card"
            )
        else:
            # Results header card
            create_card(
                title=f"Twój dominujący typ to: {degen_type}",
                icon="🏆",
                content=f"""
                <div style="padding: 15px 0; text-align: center;">
                    <h2 style="color: {DEGEN_TYPES[degen_type]['color']}; margin-bottom: 15px;">{degen_type}</h2>
                    <p style="font-size: 1.1rem;">{DEGEN_TYPES[degen_type]['description']}</p>
                </div>
                """,
                key="degen_type_card"
            )
            
            # Results chart card
            chart_container = create_card(
                title="Twoje wyniki na wykresie",
                icon="📊",
                content="<div id='chart-container' style='padding: 10px 0; display: flex; justify-content: center;'></div>",
                key="degen_chart_card"
            )
            
            with chart_container:
                fig = plot_radar_chart(degen_scores)
                st.pyplot(fig)
            
            # Type details cards
            cols = create_grid(num_columns)
            
            with cols[0]:
                # Strengths card
                create_card(
                    title="Twoje mocne strony",
                    icon="💪",
                    content="""
                    <ul style="padding-left: 20px;">
                        {}
                    </ul>
                    """.format("\n".join([f"<li>✅ {strength}</li>" for strength in DEGEN_TYPES[degen_type]["strengths"]])),
                    key="degen_strengths_card"
                )
            
            with cols[1 if num_columns > 1 else 0]:
                # Challenges card
                create_card(
                    title="Twoje wyzwania",
                    icon="🚧",
                    content="""
                    <ul style="padding-left: 20px;">
                        {}
                    </ul>
                    """.format("\n".join([f"<li>⚠️ {challenge}</li>" for challenge in DEGEN_TYPES[degen_type]["challenges"]])),
                    key="degen_challenges_card"
                )
            
            # Strategy card
            create_card(
                title="Zalecana strategia",
                icon="🎯",
                content=f"<p style='padding: 10px 0;'>{DEGEN_TYPES[degen_type]['strategy']}</p>",
                key="degen_strategy_card"
            )
            
            # Detailed description card
            if degen_type in degen_details:
                create_card(
                    title="Szczegółowy opis typu",
                    icon="📑",
                    content=f"""
                    <div class="degen-details">
                        {degen_details[degen_type]}
                    </div>
                    <style>
                        .degen-details {
                            padding: 0.5rem 0;
                            font-size: 0.9rem;
                        }
                        .degen-details h1, .degen-details h2, .degen-details h3 {
                            margin-top: 1rem;
                            margin-bottom: 0.5rem;
                        }
                        .degen-details p {
                            margin-bottom: 1rem;
                        }
                        .degen-details ul {
                            padding-left: 1.5rem;
                            margin-bottom: 1rem;
                        }
                    </style>
                    """,
                    key="degen_details_card"
                )
            
            # Retake test button
            if st.button("Wykonaj test ponownie", key="retake_degen_test"):
                st.session_state['page'] = 'degen_test'
                if 'test_step' in st.session_state:
                    del st.session_state['test_step']
                if 'test_scores' in st.session_state:
                    del st.session_state['test_scores']
                st.session_state['show_test_info'] = True
                st.rerun()
