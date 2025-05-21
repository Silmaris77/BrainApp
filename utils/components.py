import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import random

# Komponenty kart

def degen_card(title, description, icon=None, badge=None, badges=None, progress=None, button_text=None, button_action=None, status_text=None, color=None, background=None, status=None):
    """
    Wyświetla kartę z tytułem, opisem i opcjonalnie ikoną, odznaką i paskiem postępu.
    
    Parametry:
    - title: Tytuł karty
    - description: Opis zawartości
    - icon: Emoji lub ikona (opcjonalne)
    - badge: Treść odznaki (opcjonalne)
    - badges: Lista odznak (opcjonalne) - alternatywa dla pojedynczej odznaki
      Może być listą stringów lub listą słowników {'text': '...', 'type': '...'}
    - progress: Wartość procentowa postępu (opcjonalne)
    - button_text: Tekst przycisku (opcjonalne)
    - button_action: Funkcja wywoływana po kliknięciu przycisku (opcjonalne)
    - status_text: Tekst statusu (opcjonalne)
    - color: Kolor obramowania/akcentu (opcjonalne)
    - background: Kolor tła (opcjonalne)
    - status: Alias dla status_text (dla zgodności wstecznej)
    """
    # Utwórz unikalny klucz dla przycisku
    button_key = f"degen_card_{hash(title)}_{hash(description) if description else ''}_{random.randint(1000, 9999)}"
    
    # Obsłuż alias status -> status_text dla zgodności wstecznej
    if status is not None and status_text is None:
        status_text = status
    
    # Ustawienia stylu
    color_style = f"border-color: {color};" if color else ""
    bg_style = f"background-color: {background};" if background else ""
    
    # HTML struktury karty
    html = f"""
    <div class="degen-card" style="{color_style} {bg_style}">
        <div class="degen-card-header">
    """
    
    # Dodaj ikonę jeśli istnieje
    if icon:
        html += f'<div class="degen-card-icon">{icon}</div>'
    
    html += f'<div class="degen-card-title">{title}</div>'
    
    # Dodaj odznakę jeśli istnieje
    if badge:
        html += f'<div class="degen-card-badge">{badge}</div>'
    elif badges:
        # Obsługa wielu odznak
        badges_html = ""
        for b in badges:
            if isinstance(b, dict) and 'text' in b:
                badge_text = b['text']
                badge_type = b.get('type', '')
                badges_html += f'<span class="degen-card-badge-item badge-{badge_type}">{badge_text}</span> '
            else:
                badges_html += f'<span class="degen-card-badge-item">{b}</span> '
                
        html += f'<div class="degen-card-badges">{badges_html}</div>'
    
    html += """
        </div>
        <div class="degen-card-content">
    """
    
    # Dodaj opis jeśli istnieje
    if description:
        html += f'<div class="degen-card-description">{description}</div>'
    
    # Dodaj status jeśli istnieje
    if status_text:
        html += f'<div class="degen-card-status">{status_text}</div>'
    
    # Dodaj pasek postępu jeśli istnieje
    if progress is not None:
        html += f"""
        <div class="degen-card-progress-container">
            <div class="degen-card-progress-bar" style="width: {progress}%;"></div>
        </div>
        <div class="degen-card-progress-text">{progress}% ukończone</div>
        """
    
    html += """
        </div>
    </div>
    """
    
    # Wyświetl kartę
    st.markdown(html, unsafe_allow_html=True)
    
    # Dodaj przycisk jeśli istnieje
    if button_text:
        if zen_button(button_text, key=button_key):
            if button_action:
                button_action()

def mission_card(title, description, badge_emoji, xp, progress=0, completed=False):
    """
    Tworzy kartę misji z paskiem postępu.
    
    Parametry:
    - title: Tytuł misji
    - description: Opis misji
    - badge_emoji: Emoji odznaki
    - xp: Ilość punktów XP za ukończenie
    - progress: Postęp w procentach (0-100)
    - completed: Czy misja została ukończona
    """
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

def goal_card(title, description, end_date, progress=0, completed=False):
    """
    Tworzy kartę celu z paskiem postępu.
    
    Parametry:
    - title: Tytuł celu
    - description: Opis celu
    - end_date: Data ukończenia celu (str)
    - progress: Postęp w procentach (0-100)
    - completed: Czy cel został ukończony
    """
    completed_class = "completed" if completed else ""
    progress_color = "#27ae60" if completed else "#2980B9"
    
    goal_html = f"""
    <div class="goal-card {completed_class}">
        <div class="goal-header">
            <h4>{title}</h4>
            <div class="goal-date">{end_date}</div>
        </div>
        <p>{description}</p>
        <div class="goal-progress-container">
            <div class="goal-progress-bar" style="width: {progress}%; background-color: {progress_color}"></div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 10px;">
            <span>{progress}% ukończone</span>
            <span>{end_date}</span>
        </div>
    </div>
    """
    
    st.markdown(goal_html, unsafe_allow_html=True)

def badge_card(icon, title, description, earned=False):
    """
    Tworzy kartę odznaki.
    
    Parametry:
    - icon: Emoji odznaki
    - title: Nazwa odznaki
    - description: Opis odznaki
    - earned: Czy odznaka została zdobyta
    """
    earned_class = "earned" if earned else "not-earned"
    opacity = "1.0" if earned else "0.5"
    
    badge_html = f"""
    <div class="badge-card {earned_class}" style="opacity: {opacity}">
        <div class="badge-icon">{icon}</div>
        <h4>{title}</h4>
        <p>{description}</p>
    </div>
    """
    
    st.markdown(badge_html, unsafe_allow_html=True)

# Komponenty przycisków i akcji

def zen_button(label, on_click=None, key=None, disabled=False, help=None, use_container_width=False):
    """
    Tworzy stylizowany przycisk Zen.
    
    Parametry:
    - label: Etykieta przycisku
    - on_click: Funkcja do wykonania po kliknięciu
    - key: Unikalny klucz przycisku
    - disabled: Czy przycisk jest wyłączony
    - help: Tekst pomocy pokazywany po najechaniu
    - use_container_width: Czy przycisk ma używać pełnej szerokości kontenera
    
    Zwraca:
    - Bool: True jeśli przycisk został kliknięty
    """
    return st.button(
        label, 
        on_click=on_click, 
        key=key, 
        disabled=disabled, 
        help=help, 
        use_container_width=use_container_width
    )

def notification(message, type="info"):
    """
    Wyświetla powiadomienie.
    
    Parametry:
    - message: Treść powiadomienia
    - type: Typ powiadomienia (info, success, warning, error)
    """
    if type == "info":
        st.info(message)
    elif type == "success":
        st.success(message)
    elif type == "warning":
        st.warning(message)
    elif type == "error":
        st.error(message)

# Komponenty nawigacyjne

def zen_header(title, subtitle=None):
    """
    Tworzy nagłówek dla strony.
    
    Parametry:
    - title: Tytuł strony
    - subtitle: Podtytuł (opcjonalny)
    """
    st.markdown(f"<h1 class='zen-header'>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p class='zen-subtitle'>{subtitle}</p>", unsafe_allow_html=True)

def navigation_menu():
    """Wyświetla menu nawigacyjne aplikacji"""
    
    menu_options = [
        {"id": "dashboard", "name": "Dashboard", "icon": "🏠"},
        {"id": "degen_test", "name": "Test degena", "icon": "🧪"},
        {"id": "lesson", "name": "Lekcje", "icon": "📚"},
        {"id": "skills", "name": "Umiejętności", "icon": "🌳"},
        {"id": "shop", "name": "Sklep", "icon": "🛒"},
        {"id": "degen_explorer", "name": "Eksplorator", "icon": "🔍"},
        {"id": "profile", "name": "Profil", "icon": "👤"}
    ]
    
    for option in menu_options:
        # Dodaj stylizację dla aktywnego przycisku bez parametru active
        button_label = f"{option['icon']} {option['name']}"
        
        # Użyj zen_button bez parametru active
        if zen_button(
            button_label, 
            key=f"nav_{option['id']}"
        ):
            st.session_state.page = option['id']
            st.rerun()
        
        # Opcjonalnie, możesz dodać stylizację dla aktywnego przycisku używając CSS
        if st.session_state.page == option['id']:
            st.markdown(f"""
            <style>
            div[data-testid="stButton"] button[kind="secondary"][data-testid="baseButton-secondary"][aria-label="{button_label}"] {{
                background-color: rgba(255, 255, 255, 0.1);
                border-left: 3px solid #4CAF50;
            }}
            </style>
            """, unsafe_allow_html=True)

# Komponenty statystyk i danych

def stat_card(label, value, icon=None, change=None, change_type=None, custom_class=None):
    """
    Tworzy kartę statystyki.
    
    Parametry:
    - label: Etykieta statystyki
    - value: Wartość statystyki
    - icon: Emoji ikony
    - change: Zmiana wartości (z podanym znakiem)
    - change_type: Typ zmiany (positive, negative, neutral)
    - custom_class: Niestandardowa klasa CSS dla karty
    """
    change_html = ""
    if change:
        change_color = "#27ae60" if change_type == "positive" else (
            "#e74c3c" if change_type == "negative" else "#7f8c8d")
        change_html = f'<span style="color: {change_color}; font-size: 12px;">({change})</span>'
    
    # Używamy nowej struktury HTML, jeśli przekazano custom_class
    if custom_class:
        stat_html = f"""
        <div class="{custom_class}">
            <div class="stat-icon">{icon}</div>
            <div class="stat-value">{value} {change_html}</div>
            <div class="stat-label">{label}</div>
        </div>
        """
    else:
        # Oryginalna wersja dla wstecznej kompatybilności
        icon_html = f'<span style="font-size: 24px; margin-right: 10px;">{icon}</span>' if icon else ""
        
        stat_html = f"""
        <div style="background-color: white; border-radius: 10px; padding: 15px; box-shadow: 0 3px 10px rgba(0,0,0,0.08);">
            <div style="display: flex; align-items: center;">
                {icon_html}
                <div>
                    <div style="color: #7f8c8d; font-size: 14px;">{label}</div>
                    <div style="font-size: 24px; font-weight: bold; color: #2c3e50;">{value} {change_html}</div>
                </div>
            </div>
        </div>
        """
    
    st.markdown(stat_html, unsafe_allow_html=True)

def progress_bar(progress, color="#4CAF50"):
    """
    Wyświetla pasek postępu z niestandardowym stylem.
    
    Args:
        progress (float): Wartość postępu od 0.0 do 1.0
        color (str): Kolor paska postępu w formacie HEX
    """
    # Upewnij się, że progress jest w zakresie [0.0, 1.0]
    progress = min(max(progress, 0.0), 1.0)
    
    # Zastosuj niestandardowy styl
    bar_style = f"""
    <style>
    .stProgress > div > div > div > div {{
        background-color: {color};
    }}
    </style>
    """
    st.markdown(bar_style, unsafe_allow_html=True)
    
    # Wyświetl pasek postępu
    st.progress(progress)

def xp_level_display(xp, level, next_level_xp):
    """
    Wyświetla poziom XP użytkownika z paskiem postępu.
    
    Parametry:
    - xp: Obecna liczba punktów XP
    - level: Obecny poziom
    - next_level_xp: XP wymagane do następnego poziomu
    """
    previous_level_xp = 0  # Można dostosować na podstawie konfiguracji poziomów
    xp_progress = xp - previous_level_xp
    xp_needed = next_level_xp - previous_level_xp
    progress_percent = min(100, int((xp_progress / xp_needed) * 100)) if xp_needed > 0 else 0
    
    level_html = f"""
    <div class="m3-level-progress">
        <div class="level-info">
            <div class="current-level">
                <div class="level-number">{level}</div>
                <div class="level-label">Poziom</div>
            </div>
            <div class="progress-container">
                <div class="xp-info">
                    <span>XP: {xp} / {next_level_xp}</span>
                    <span>{xp_needed - xp_progress} XP do poziomu {level + 1}</span>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-bar" style="width: {progress_percent}%"></div>
                </div>
                <div class="level-markers">
                    <div class="level-start">{level}</div>
                    <div class="level-end">{level + 1}</div>
                </div>
            </div>
        </div>
    </div>
    """
    
    # Dodajemy style CSS dla nowego wyglądu poziomu
    st.markdown("""
    <style>
    .m3-level-progress {
        margin: 15px 0;
    }
    
    .level-info {
        display: flex;
        align-items: center;
    }
    
    .current-level {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-right: 15px;
        min-width: 60px;
    }
    
    .level-number {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(102, 126, 234, 0.4);
        margin-bottom: 5px;
    }
    
    .level-label {
        font-size: 0.75rem;
        color: #666;
    }
    
    .progress-container {
        flex-grow: 1;
    }
    
    .xp-info {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        font-size: 0.85rem;
        color: #555;
    }
    
    .progress-bar-container {
        height: 10px;
        background: #e0e0e0;
        border-radius: 5px;
        overflow: hidden;
        margin-bottom: 5px;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(to right, #667eea, #764ba2);
        border-radius: 5px;
        transition: width 0.5s ease;
    }
    
    .level-markers {
        display: flex;
        justify-content: space-between;
        font-size: 0.75rem;
        color: #777;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(level_html, unsafe_allow_html=True)

# Komponenty treści edukacyjnych

def content_section(title, content, collapsed=True, icon=None, border_color=None):
    """
    Wyświetla sekcję z treścią, która może być rozwijana/zwijana
    
    Parametry:
    title (str): Tytuł sekcji
    content (str): Treść HTML do wyświetlenia w sekcji
    collapsed (bool): Czy sekcja ma być domyślnie zwinięta
    icon (str): Opcjonalna ikona do wyświetlenia obok tytułu
    border_color (str): Opcjonalny kolor obramowania sekcji (np. "#3498db")
    """
    # Generuj unikalny ID dla tej sekcji
    section_id = f"section_{title.replace(' ', '_').lower()}"
    
    # Ikonka, jeśli została podana
    icon_html = f"{icon} " if icon else ""
    
    # Strzałka rozwijania/zwijania
    arrow = "▼" if not collapsed else "▶"
    
    # Style obramowania, jeśli podano kolor
    border_style = f"border-left: 4px solid {border_color}; padding-left: 12px;" if border_color else ""
    
    # Wyświetl nagłówek jako przycisk rozwijania/zwijania
    header_html = f"""
    <div class="collapsible-header" onclick="toggleSection('{section_id}')" style="{border_style}">
        <span class="toggle-arrow" id="arrow_{section_id}">{arrow}</span>
        <h3>{icon_html}{title}</h3>
    </div>
    """
    
    # Kontener na treść
    content_style = "display:none;" if collapsed else "display:block;"
    content_style += border_style  # Dodaj obramowanie również do treści
    content_html = f"""
    <div class="section-content" id="{section_id}" style="{content_style}">
        {content}
    </div>
    """
    
    # Skrypt JS do obsługi rozwijania/zwijania
    script = """
    <script>
    function toggleSection(sectionId) {
        var content = document.getElementById(sectionId);
        var arrow = document.getElementById('arrow_' + sectionId);
        if (content.style.display === 'none' || content.style.display === '') {
            content.style.display = 'block';
            arrow.textContent = '▼';
        } else {
            content.style.display = 'none';
            arrow.textContent = '▶';
        }
    }
    </script>
    """
    
    # Łączymy wszystkie elementy
    st.markdown(header_html + content_html + script, unsafe_allow_html=True)

def quote_block(text, author=None):
    """
    Tworzy blok cytatu.
    
    Parametry:
    - text: Tekst cytatu
    - author: Autor cytatu (opcjonalnie)
    """
    author_html = f'<div style="text-align: right; font-style: italic;">— {author}</div>' if author else ""
    
    quote_html = f"""
    <div style="background-color: #f8f9fa; border-left: 4px solid #2980B9; padding: 15px; margin: 15px 0; border-radius: 0 5px 5px 0;">
        <div style="font-style: italic; font-size: 16px;">{text}</div>
        {author_html}
    </div>
    """
    
    st.markdown(quote_html, unsafe_allow_html=True)

def tip_block(text, type="tip", title=None, icon=None):
    """
    Tworzy blok ze wskazówką, ostrzeżeniem lub informacją.
    
    Parametry:
    - text: Tekst wskazówki
    - type: Typ bloku (tip, warning, info)
    - title: Opcjonalny tytuł bloku
    - icon: Niestandardowa ikona (zastępuje domyślną ikonę)
    """
    default_icon = "💡" if type == "tip" else ("⚠️" if type == "warning" else "ℹ️")
    background = "#e3f4eb" if type == "tip" else ("#fef7e6" if type == "warning" else "#e6f3fc")
    border = "#27ae60" if type == "tip" else ("#f39c12" if type == "warning" else "#3498db")
    
    # Użyj niestandardowej ikony, jeśli podana, w przeciwnym razie użyj domyślnej
    display_icon = icon if icon else default_icon
    
    # Dodaj tytuł, jeśli jest podany
    title_html = f'<div style="font-weight: bold; margin-bottom: 8px;">{title}</div>' if title else ""
    
    tip_html = f"""
    <div style="background-color: {background}; border-left: 4px solid {border}; padding: 15px; margin: 15px 0; border-radius: 0 5px 5px 0;">
        <div style="display: flex; align-items: flex-start;">
            <span style="font-size: 24px; margin-right: 10px;">{display_icon}</span>
            <div>
                {title_html}
                <div>{text}</div>
            </div>
        </div>
    </div>
    """
    
    st.markdown(tip_html, unsafe_allow_html=True)

def leaderboard_item(rank, username, points, is_current_user=False):
    """
    Tworzy element rankingu XP.
    
    Parametry:
    - rank: Pozycja w rankingu
    - username: Nazwa użytkownika
    - points: Liczba punktów XP
    - is_current_user: Czy element dotyczy bieżącego użytkownika
    """
    medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}."
    bg_color = "#f0f7fb" if is_current_user else "#ffffff"
    border = "2px solid #2980B9" if is_current_user else "1px solid #f0f0f0"
    
    leaderboard_html = f"""    <div style="display: flex; align-items: center; margin-bottom: 8px; padding: 10px; 
               border-radius: 8px; background-color: {bg_color}; border: {border};">
        <div style="width: 30px; text-align: center; font-size: 16px;">{medal}</div>
        <div style="flex-grow: 1; padding-left: 10px; font-weight: {500 if is_current_user else 400};">
            {username}{" (Ty)" if is_current_user else ""}
        </div>
        <div style="font-weight: bold; color: #2980B9;">{points} XP</div>
    </div>
    """
    
    st.markdown(leaderboard_html, unsafe_allow_html=True)

def embed_content(url, width="100%", height="600px", title=None):
    """
    Tworzy osadzony element (iframe) dla interaktywnych treści.
    
    Parametry:
    - url: URL do osadzenia 
    - width: Szerokość elementu (domyślnie: '100%')
    - height: Wysokość elementu (domyślnie: '600px')
    - title: Opcjonalny tytuł nad osadzonym elementem
    """
    if title:
        st.subheader(title)
        
    embed_html = f"""
    <div style="margin: 15px 0;">
        <iframe src="{url}"
                width="{width}" height="{height}" 
                style="border:none; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" 
                allowfullscreen>
        </iframe>
    </div>
    """
    
    st.markdown(embed_html, unsafe_allow_html=True)

def add_animations_css():
    """Dodaje animacje CSS bez używania jQuery"""
    st.markdown("""
    <style>
    /* Animacje używające czystego CSS zamiast jQuery */
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    
    .fadeIn {
        animation: fadeIn 0.5s ease-in;
    }
    </style>
    """, unsafe_allow_html=True)

def data_chart(data, chart_type="bar", title=None, x_label=None, y_label=None, height=400):
    """
    Tworzy wykres na podstawie danych.
    
    Parametry:
    - data: Dane do wykresu (lista słowników lub pandas DataFrame)
    - chart_type: Typ wykresu ("bar", "line", "area", "pie")
    - title: Tytuł wykresu
    - x_label: Etykieta osi X
    - y_label: Etykieta osi Y
    - height: Wysokość wykresu w pikselach
    """
    if title:
        st.subheader(title)
    
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)
    
    if chart_type == "bar":
        chart = alt.Chart(data).mark_bar().encode(
            x=alt.X(data.columns[0], title=x_label or data.columns[0]),
            y=alt.Y(data.columns[1], title=y_label or data.columns[1])
        ).properties(height=height)
        st.altair_chart(chart, use_container_width=True)
    
    elif chart_type == "line":
        chart = alt.Chart(data).mark_line().encode(
            x=alt.X(data.columns[0], title=x_label or data.columns[0]),
            y=alt.Y(data.columns[1], title=y_label or data.columns[1])
        ).properties(height=height)
        st.altair_chart(chart, use_container_width=True)
    
    elif chart_type == "area":
        chart = alt.Chart(data).mark_area().encode(
            x=alt.X(data.columns[0], title=x_label or data.columns[0]),
            y=alt.Y(data.columns[1], title=y_label or data.columns[1])
        ).properties(height=height)
        st.altair_chart(chart, use_container_width=True)
    elif chart_type == "pie":
        # For pie charts, we use matplotlib
        fig, ax = plt.subplots()
        ax.pie(data[data.columns[1]], labels=list(data[data.columns[0]]), autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        if title:
            ax.set_title(title)
        st.pyplot(fig)

def user_stats_panel(username, avatar, degen_type, level, xp, completed_lessons=None, next_level_xp=None):
    """
    Tworzy panel z podstawowymi statystykami użytkownika.
    
    Parametry:
    - username: Nazwa użytkownika
    - avatar: Emoji awatara użytkownika
    - degen_type: Typ Degena użytkownika
    - level: Aktualny poziom użytkownika
    - xp: Aktualna ilość punktów XP
    - completed_lessons: Lista ukończonych lekcji (opcjonalna)
    - next_level_xp: Wymagane XP do następnego poziomu (opcjonalne)
    """
    
    # Avatar i informacje podstawowe
    st.markdown(f"""
    <div class="user-panel">
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 5rem; margin-bottom: 10px;">{avatar}</div>
            <div style="font-weight: bold; font-size: 1.2rem;">{username}</div>
            <div style="color: #888;">{degen_type}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Statystyki w trzech kolumnach
    stats_cols = st.columns(3)
    
    with stats_cols[0]:
        stat_card("Poziom", level, icon="🏆")
    
    with stats_cols[1]:
        stat_card("XP", xp, icon="💎")
    
    with stats_cols[2]:
        if completed_lessons is not None:
            completed_count = len(completed_lessons) if isinstance(completed_lessons, list) else completed_lessons
            stat_card("Ukończone lekcje", completed_count, icon="📚")
    
    # Pasek postępu XP do następnego poziomu
    if next_level_xp is not None:
        xp_level_display(xp=xp, level=level, next_level_xp=next_level_xp)

def lesson_card(title, description, image=None, xp=0, duration=0, difficulty=None, 
               completed=False, button_text="Rozpocznij", on_click=None, 
               button_key=None, lesson_id=None, category=None):
    """
    Renders a standardized lesson card for both dashboard and lessons view
    with Material 3 design principles
    """
    # Prepare difficulty info
    if difficulty is None:
        difficulty = "beginner"
    
    # Material 3 Colors
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
    
    # Generate the HTML for the card with Material 3 design
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
    
    # Define Material 3 CSS styles
    styles = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    
    .m3-lesson-card {
        background-color: white;
        color: #333;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
        transition: all 0.3s;
        position: relative;
        overflow: hidden;
        font-family: 'Roboto', sans-serif;
    }
    
    .m3-lesson-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #2196F3, #673AB7);
        opacity: 0.8;
    }
    
    .m3-lesson-card:hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.16);
        transform: translateY(-2px);
    }
    
    .m3-lesson-card-completed::before {
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
    }
    
    .m3-card-content {
        position: relative;
    }
    
    .m3-lesson-card h3 {
        font-size: 1.5rem;
        font-weight: 500;
        margin-bottom: 16px;
        color: #1A237E;
    }
    
    .m3-lesson-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin: 16px 0;
    }
    
    .m3-badge {
        padding: 6px 12px;
        border-radius: 24px;
        font-size: 14px;
        font-weight: 500;
        color: white;
        display: inline-flex;
        align-items: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    }
    .time-badge {
        background-color: #2196F3;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 14px;
    }
    .category-badge {
        background-color: #9575CD;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 14px;
        display: inline-block;
        margin-top: 5px;
    }
    .completion-status {
        color: #757575;
        margin-top: 10px;
    }
    .completion-status.completed {
        color: #4CAF50;
    }
    </style>
    """
    
    # Render the card with styles
    st.markdown(card_html + styles, unsafe_allow_html=True)
    
    # Add the button with custom behavior
    if button_key is None and lesson_id is not None:
        button_key = f"lesson_btn_{lesson_id}"
    
    if zen_button(button_text, key=button_key, use_container_width=True):
        if on_click and callable(on_click):
            # If there's a callback function, call it with lesson_id
            if lesson_id:
                on_click(lesson_id)
            else:
                on_click()
        else:
            # Default behavior - set current lesson and redirect
            st.session_state.current_lesson = lesson_id
            st.session_state.lesson_step = 'intro'
            if 'quiz_score' in st.session_state:
                st.session_state.quiz_score = 0
            st.rerun()

def skill_node(name, icon, level, max_level, description="", unlocked=True, cost=0, on_click=None, node_id=None):
    """
    Wyświetla węzeł umiejętności w drzewie umiejętności.
    
    Parametry:
    - name: Nazwa umiejętności
    - icon: Emoji lub ikona umiejętności
    - level: Aktualny poziom umiejętności
    - max_level: Maksymalny poziom umiejętności
    - description: Opis umiejętności (opcjonalny)
    - unlocked: Czy umiejętność jest odblokowana (domyślnie True)
    - cost: Koszt ulepszenia w XP (opcjonalny)
    - on_click: Funkcja wywoływana po kliknięciu w węzeł (opcjonalny)
    - node_id: Identyfikator węzła (opcjonalny)
    """
    node_key = f"skill_node_{hash(name)}_{random.randint(1000, 9999)}" if node_id is None else f"skill_node_{node_id}"
    
    # Klasa CSS zależna od stanu odblokowania
    lock_class = "unlocked" if unlocked else "locked"
    
    # Pasek postępu
    progress_percent = (level / max_level) * 100 if max_level > 0 else 0
    
    html = f"""
    <div class="skill-node {lock_class}" id="{node_key}">
        <div class="skill-icon">{icon}</div>
        <h4>{name}</h4>
        <div class="skill-level">Poziom: {level}/{max_level}</div>
        <div class="skill-progress-container">
            <div class="skill-progress-bar" style="width: {progress_percent}%;"></div>
        </div>
        <p>{description}</p>
    """
    
    if not unlocked:
        html += f'<div class="skill-cost">Koszt odblokowania: {cost} XP</div>'
    elif level < max_level:
        html += f'<div class="skill-cost">Koszt ulepszenia: {cost} XP</div>'
    
    html += "</div>"
    
    # Wyświetl węzeł
    st.markdown(html, unsafe_allow_html=True)
    
    # Zwróć klucz węzła, który może być używany do śledzenia kliknięć
    return node_key
