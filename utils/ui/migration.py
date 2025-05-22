"""
Moduł migracyjny do płynnego przejścia z starego systemu komponentów na nowy
"""

# Importy z nowego systemu
from utils.ui import (
    stat_card as new_stat_card,
    skill_card as new_skill_card,
    mission_card as new_mission_card,
    lesson_card as new_lesson_card,
    zen_button as new_zen_button,
    notification as new_notification,
    progress_bar as new_progress_bar,
    zen_header as new_zen_header,
    quote_block as new_quote_block,
    tip_block as new_tip_block,
    content_section as new_content_section
)

# Importy ze starego systemu dla zgodności
from utils.components import (
    degen_card,
    goal_card,
    badge_card,
    skill_node,
    lesson_button,
    add_animations_css,
    leaderboard_item,
    embed_content,
    data_chart,
    xp_level_display
)

def initialize_ui():
    """
    Inicjalizuje nowy system UI, zachowując zgodność z starym systemem.
    """
    from utils.ui import initialize_ui as new_initialize_ui
    return new_initialize_ui()

# Mapowanie starych funkcji do nowych
def stat_card(label, value, icon=None, change=None, change_type=None, custom_class=None):
    """Kompatybilność wsteczna dla stat_card"""
    return new_stat_card(icon, value, label)

def zen_button(label, on_click=None, key=None, disabled=False, help=None, use_container_width=False):
    """Kompatybilność wsteczna dla zen_button"""
    return new_zen_button(label, on_click, key, disabled, help, use_container_width)

def notification(message, type="info"):
    """Kompatybilność wsteczna dla notification"""
    return new_notification(message, type)

def progress_bar(progress, color="#4CAF50"):
    """Kompatybilność wsteczna dla progress_bar"""
    return new_progress_bar(progress, color)

def zen_header(title, subtitle=None):
    """Kompatybilność wsteczna dla zen_header"""
    return new_zen_header(title, subtitle)

def quote_block(text, author=None):
    """Kompatybilność wsteczna dla quote_block"""
    return new_quote_block(text, author)

def tip_block(text, type="tip", title=None, icon=None):
    """Kompatybilność wsteczna dla tip_block"""
    return new_tip_block(text, type, title, icon)

def content_section(title, content, collapsed=True, icon=None, border_color=None):
    """Kompatybilność wsteczna dla content_section"""
    return new_content_section(title, content, collapsed, icon, border_color)

def skill_card_wrapper(category, progress, status, icon, description, completed_count, total_count, index=0):
    """Adapter do przekształcania wywołań ze starego systemu na nowy"""
    return new_skill_card(category, progress, status, icon, description, completed_count, total_count, index)

def mission_card_wrapper(title, description, badge_emoji, xp, progress=0, completed=False):
    """Adapter do przekształcania wywołań ze starego systemu na nowy"""
    return new_mission_card(title, description, badge_emoji, xp, progress, completed)

def lesson_card_wrapper(title, description, image=None, xp=0, duration=0, difficulty=None, 
                       completed=False, button_text="Rozpocznij", on_click=None, 
                       button_key=None, lesson_id=None, category=None):
    """Adapter do przekształcania wywołań ze starego systemu na nowy"""
    return new_lesson_card(title, description, xp, difficulty, category, 
                           completed, button_text, on_click, button_key, lesson_id)
