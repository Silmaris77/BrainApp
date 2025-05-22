"""
Bridge module to help transition from old UI components to new UI system.
This provides compatibility functions that let you use the new UI system
while gradually migrating from the old components.
"""

import streamlit as st
from typing import Callable, Any, Optional, Dict, List, Union

# Import from new UI system
from utils.ui.components.cards import stat_card, skill_card, mission_card, lesson_card
from utils.ui.components.interactive import zen_button, notification, progress_bar
from utils.ui.components.text import zen_header, quote_block, tip_block, content_section
from utils.ui.layouts.grid import render_dashboard_header, render_stats_section, responsive_grid

# Bridge functions for cards
def bridge_degen_card(title, description, icon=None, badge=None, badges=None, progress=None, 
                      button_text=None, button_action=None, status_text=None, color=None, 
                      background=None, status=None):
    """Bridge to migrate from old degen_card to new skill_card."""
    
    # Calculate progress percentage
    prog_value = progress if progress is not None else 0
    
    # Set status based on progress
    if status or status_text:
        status_val = status or status_text
    elif prog_value == 100:
        status_val = "max-level"
    elif prog_value > 0:
        status_val = "in-progress"
    else:
        status_val = "not-started"
    
    # Render skill card with mapped values
    skill_card(
        category=title,
        progress=prog_value,
        status=status_val,
        icon=icon or "📊",
        description=description or "",
        completed_count=int(prog_value/10) if prog_value is not None else 0,
        total_count=10
    )
    
    # Handle button separately
    if button_text:
        if zen_button(button_text):
            if button_action and callable(button_action):
                button_action()

def bridge_stat_card(label, value, icon=None, change=None, change_type=None, custom_class=None):
    """Bridge to migrate from old stat_card to new stat_card."""
    # Combine value and change if provided
    display_value = str(value)
    if change:
        change_prefix = "+" if change_type == "positive" and not str(change).startswith("+") else ""
        display_value = f"{value} {change_prefix}{change}"
    
    # Use new stat_card
    stat_card(icon=icon or "📊", value=display_value, label=label)

def bridge_mission_card(title, description, badge_emoji, xp, progress=0, completed=False):
    """Bridge to migrate from old mission_card to new mission_card."""
    # Use new mission_card
    mission_card(title, description, badge_emoji, xp, progress, completed)

def bridge_lesson_card(title, description, image=None, xp=0, duration=0, difficulty=None, 
                      completed=False, button_text="Rozpocznij", on_click=None, 
                      button_key=None, lesson_id=None, category=None):
    """Bridge to migrate from old lesson_card to new lesson_card."""
    # Use new lesson_card
    lesson_card(
        title=title,
        description=description,
        xp=xp,
        difficulty=difficulty,
        category=category,
        completed=completed,
        button_text=button_text,
        on_click=on_click,
        button_key=button_key,
        lesson_id=lesson_id
    )

# Bridge functions for text components
def bridge_content_section(title, content, collapsed=True, icon=None, border_color=None):
    """Bridge to migrate from old content_section to new content_section."""
    # Use new content_section
    content_section(title, content, collapsed, icon, border_color)

def bridge_quote_block(text, author=None):
    """Bridge to migrate from old quote_block to new quote_block."""
    # Use new quote_block
    quote_block(text, author)

def bridge_tip_block(text, type="tip", title=None, icon=None):
    """Bridge to migrate from old tip_block to new tip_block."""
    # Use new tip_block
    tip_block(text, type, title, icon)

# Bridge functions for interactive components
def bridge_zen_button(label, on_click=None, key=None, disabled=False, help=None, use_container_width=False):
    """Bridge to migrate from old zen_button to new zen_button."""
    # Use new zen_button
    return zen_button(label, on_click, key, disabled, help, use_container_width)

def bridge_notification(message, type="info"):
    """Bridge to migrate from old notification to new notification."""
    # Use new notification
    notification(message, type)

def bridge_progress_bar(progress, color="#4CAF50"):
    """Bridge to migrate from old progress_bar to new progress_bar."""
    # Use new progress_bar
    progress_bar(progress, color)

# Helper function to initialize bridge mode
def initialize_bridge(theme_name=None):
    """
    Initialize UI system in bridge mode.
    This sets up the UI system and prepares it for use with bridge components.
    
    Parameters:
    - theme_name: Optional theme name to load
    """
    from utils.ui import initialize_ui
    
    # Initialize UI system
    initialize_ui(theme_name)
    
    # Add bridge-specific logic here if needed
    st.session_state.bridge_mode = True
    
    return True
