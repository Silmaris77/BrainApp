import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta

# Import z nowego systemu UI
from utils.ui import initialize_ui, theme_selector
from utils.ui.components.cards import stat_card, skill_card
from utils.ui.components.text import zen_header, tip_block
from utils.ui.layouts.grid import render_dashboard_header, render_stats_section, responsive_grid

# Import z pozostałych modułów aplikacji
from data.users import load_user_data, save_user_data
from data.neuroleader_types import NEUROLEADER_TYPES

def show_neuroleader_dashboard():
    """Przykład dashboardu korzystającego z nowego systemu UI."""
    # Inicjalizacja UI
    initialize_ui()
    
    # Pobranie danych użytkownika
    user_data = load_user_data().get(st.session_state.username, {})
    
    # Nagłówek strony
    render_dashboard_header(
        "Dashboard Neuroliderera", 
        f"Witaj, {st.session_state.username}! Oto twój dashboard."
    )
    
    # Ustawienia motywu
    with st.sidebar:
        st.header("Ustawienia")
        theme_selector()
    
    # Sekcja statystyk
    user_stats = [
        ("🧠", user_data.get("level", 1), "Poziom Neuroliderera"),
        ("⭐", user_data.get("xp", 0), "Punkty XP"),
        ("📚", len(user_data.get("completed_lessons", [])), "Ukończone lekcje")
    ]
    render_stats_section(user_stats)
    
    # Wskazówka dla użytkownika
    tip_block(
        "Zdobywaj punkty XP, kończąc lekcje i misje. Im wyższy poziom, tym więcej funkcji odblokujesz!",
        type="tip",
        title="Jak zdobywać poziomy?",
        icon="💡"
    )
    
    # Umiejętności użytkownika
    st.header("Twoje umiejętności")
    
    # Pobierz dane umiejętności
    user_skills = user_data.get("skills", {})
    
    # Wyświetl umiejętności w responsywnej siatce
    columns = responsive_grid(columns_desktop=3, columns_tablet=2, columns_mobile=1)
    
    # Przykładowe umiejętności
    skills_data = [
        {
            "name": "Neurobiologia przywództwa",
            "id": "neuro_leadership_intro",
            "progress": user_skills.get("neuro_leadership_intro", {}).get("level", 0) * 10,
            "icon": "🧠",
            "description": "Podstawy neuroprzywództwa i struktura mózgu lidera",
            "completed": user_skills.get("neuro_leadership_intro", {}).get("level", 0),
            "total": 10
        },
        {
            "name": "Procesy decyzyjne",
            "id": "decision_models",
            "progress": user_skills.get("decision_models", {}).get("level", 0) * 10,
            "icon": "⚖️",
            "description": "Modele podejmowania decyzji i analiza ryzyka",
            "completed": user_skills.get("decision_models", {}).get("level", 0),
            "total": 10
        },
        {
            "name": "Emocje w przywództwie",
            "id": "emotions_leadership",
            "progress": user_skills.get("emotions_leadership", {}).get("level", 0) * 10,
            "icon": "❤️",
            "description": "Inteligencja emocjonalna i zarządzanie emocjami",
            "completed": user_skills.get("emotions_leadership", {}).get("level", 0),
            "total": 10
        }
    ]
    
    # Wyświetl karty umiejętności
    for i, skill in enumerate(skills_data):
        with columns[i % len(columns)]:
            # Określenie statusu
            if skill["progress"] == 100:
                status = "max-level"
            elif skill["progress"] > 0:
                status = "in-progress"
            else:
                status = "not-started"
            
            # Karta umiejętności
            skill_card(
                category=skill["name"],
                progress=skill["progress"],
                status=status,
                icon=skill["icon"],
                description=skill["description"],
                completed_count=skill["completed"],
                total_count=skill["total"],
                index=i
            )
    
    # Wykres postępu
    st.header("Postęp w czasie")
    
    # Symulowane dane dla wykresu (normalnie pobrane z bazy danych)
    dates = [datetime.now() - timedelta(days=x) for x in range(14, -1, -1)]
    dates_str = [d.strftime("%d.%m") for d in dates]
    
    # Symulowane wartości XP
    xp_values = np.cumsum(np.random.randint(10, 50, size=15))
    
    # Tworzenie DataFrame
    chart_data = pd.DataFrame({
        'data': dates_str,
        'XP': xp_values
    })
    
    # Wyświetl wykres
    st.area_chart(chart_data.set_index('data'))
    
    # Przykład zastosowania sekcji zawartości
    content_section(
        "Zaplanowane aktywności",
        """
        <ul>
            <li><strong>Nowy moduł:</strong> Neuroplastyczność w przywództwie - dostępny od 15 czerwca</li>
            <li><strong>Wyzwanie:</strong> 30-dniowy challenge neurolidera - rozpoczyna się 1 lipca</li>
            <li><strong>Webinar:</strong> Neuroscience w praktyce biznesowej - 20 czerwca, 18:00</li>
        </ul>
        """,
        collapsed=True,
        icon="📅"
    )

if __name__ == "__main__":
    show_neuroleader_dashboard()
