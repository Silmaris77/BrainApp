import streamlit as st
import random

def stat_card(value, label, icon=None):
    """
    Wyświetla kartę ze statystyką.
    
    Parametry:
    - value: Wartość statystyki
    - label: Etykieta statystyki
    - icon: Ikona (opcjonalnie)
    """
    with st.container():
        st.markdown(
            f"""
            <div class="stat-card">
                {f'<div class="stat-icon">{icon}</div>' if icon else ''}
                <div class="stat-value">{value}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, 
            unsafe_allow_html=True
        )

def profile_card(title, content, color=None, icon=None, footer_content=None, key=None):
    """
    Wyświetla kartę profilu z możliwością stylizacji.
    
    Parametry:
    - title: Tytuł karty
    - content: Zawartość karty (może być HTML)
    - color: Kolor akcentu (opcjonalnie)
    - icon: Ikona (opcjonalnie)
    - footer_content: Zawartość stopki (opcjonalnie)
    - key: Unikalny klucz dla komponentu (opcjonalnie)
    """
    # Ustaw domyślny kolor, jeśli nie podano
    color = color or "var(--primary-color)"
    
    # Wygeneruj unikalny klucz, jeśli nie podano
    if key is None:
        import random
        import string
        key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    
    # Stwórz stylizowaną kartę
    st.markdown(
        f"""
        <div class="profile-card" id="profile-card-{key}">
            <div class="profile-card-header" style="border-color: {color}">
                {f'<span class="profile-card-icon">{icon}</span>' if icon else ''}
                <h3 class="profile-card-title">{title}</h3>
            </div>
            <div class="profile-card-content">
                {content}
            </div>
            {f'<div class="profile-card-footer">{footer_content}</div>' if footer_content else ''}
        </div>
        <style>
            .profile-card {{
                background-color: var(--card-background);
                border-radius: var(--card-border-radius);
                box-shadow: var(--card-shadow);
                padding: var(--card-padding);
                margin-bottom: var(--spacing-lg);
                transition: all var(--transition-speed) ease;
            }}
            .profile-card:hover {{
                box-shadow: var(--card-hover-shadow);
            }}
            .profile-card-header {{
                border-bottom: 2px solid {color};
                padding-bottom: 0.5rem;
                margin-bottom: 1rem;
                display: flex;
                align-items: center;
            }}
            .profile-card-icon {{
                font-size: 1.5rem;
                margin-right: 0.5rem;
            }}
            .profile-card-title {{
                margin: 0;
                color: {color};
            }}
            .profile-card-content {{
                margin-bottom: 0.5rem;
            }}
            .profile-card-footer {{
                margin-top: 1rem;
                padding-top: 0.5rem;
                border-top: 1px solid var(--border-color);
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

def skill_card(category, progress, status, icon, description, completed_count, total_count, index=0):
    """Renderuje kartę umiejętności."""
    status_class = status.replace(" ", "-").lower() if status else ""
    
    st.markdown(f"""
    <div class="skill-card {status_class}" style="--card-index: {index};">
        <div class="skill-card-icon">{icon}</div>
        <h4>{category}</h4>
        <div class="level-indicator">Poziom {completed_count}/{total_count}</div>
        <div class="skill-progress-bar">
            <div class="skill-progress" style="width:{progress}%;"></div>
        </div>
        <p class="skill-description">{description}</p>
        <p class="completed-lessons">Ukończone lekcje: {completed_count}/{total_count}</p>
    </div>
    """, unsafe_allow_html=True)
    
def mission_card(title, description, badge_emoji, xp, progress=0, completed=False):
    """Renderuje kartę misji z paskiem postępu."""
    completed_class = "completed" if completed else ""
    
    mission_html = f"""
    <div class="mission-card {completed_class}">
        <div class="mission-header">
            <div class="mission-badge">{badge_emoji}</div>
            <div>
                <div class="mission-title">{title}</div>
                <div class="mission-desc">{description}</div>
            </div>
        </div>
        <div class="mission-progress-container">
            <div class="mission-progress-bar" style="width: {progress}%">{progress}%</div>
        </div>
        <div style="text-align: right; margin-top: 10px;">
            <span class="mission-xp">+{xp} XP</span>
        </div>
    </div>
    """
    
    st.markdown(mission_html, unsafe_allow_html=True)

def lesson_card(title, description, xp=0, difficulty=None, category=None, 
                completed=False, button_text="Rozpocznij", on_click=None, 
                button_key=None, lesson_id=None):
    """Renderuje kartę lekcji."""
    from utils.components import zen_button  # Import lokalnie aby uniknąć cyklicznych importów
    
    # Przygotuj informacje o poziomie trudności
    if difficulty is None:
        difficulty = "beginner"
    
    # Kolory w stylu Material 3
    difficulty_colors = {
        "beginner": "#4CAF50",
        "intermediate": "#FF9800",
        "advanced": "#F44336",
        "expert": "#9C27B0"
    }
    
    difficulty_icons = {
        "beginner": "🟢",
        "intermediate": "🟠",
        "advanced": "🔴",
        "expert": "⭐"
    }
    
    difficulty_color = difficulty_colors.get(difficulty.lower(), "#4CAF50")
    difficulty_icon = difficulty_icons.get(difficulty.lower(), "🟢")
    
    # Generowanie HTML karty
    card_html = f"""
    <div class="m3-lesson-card {'m3-lesson-card-completed' if completed else ''}">
        <div class="m3-card-content">
            <h3>{title}</h3>
            <div class="m3-lesson-badges">
                <span class="m3-badge m3-badge-xp">
                    💎 {xp} XP
                </span>
                <span class="m3-badge" style="background-color: {difficulty_color};">
                    {difficulty_icon} {difficulty.capitalize()}
                </span>
                {f'<span class="m3-badge m3-badge-category">{category}</span>' if category else ''}
            </div>
            <p class="m3-description">{description[:150]}{'...' if len(description) > 150 else ''}</p>
            <p class="m3-completion-status {'m3-completed' if completed else ''}">
                {'✓ Ukończono' if completed else '○ Nieukończono'}
            </p>
        </div>
    </div>
    """
    
    # Wyświetl kartę
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Dodaj przycisk z niestandardowym zachowaniem
    if button_key is None and lesson_id is not None:
        button_key = f"lesson_btn_{lesson_id}"
    
    if zen_button(button_text, key=button_key, use_container_width=True):
        if on_click and callable(on_click):
            # Jeśli istnieje funkcja zwrotna, wywołaj ją z lesson_id
            if lesson_id:
                on_click(lesson_id)
            else:
                on_click()
        else:
            # Zachowanie domyślne - ustaw bieżącą lekcję i przekierowanie
            st.session_state.current_lesson = lesson_id
            st.session_state.lesson_step = 'intro'
            if 'quiz_score' in st.session_state:
                st.session_state.quiz_score = 0
            st.rerun()
