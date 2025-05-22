import streamlit as st
from data.lessons import load_lessons as load_lessons_data
from utils.ui import initialize_ui
from utils.ui.components.interactive import zen_button, notification
from utils.ui.components.text import content_section, zen_header
from utils.ui.layouts.grid import responsive_grid, render_dashboard_header

def show_lesson_content(lesson_id):
    """
    Wyświetla zawartość lekcji używając nowego systemu UI zgodnego z CSP
    """
    # Inicjalizacja UI
    initialize_ui()
    
    # Pobierz dane lekcji
    lessons = load_lessons_data()
    lesson = lessons.get(lesson_id, None)
    
    if not lesson:
        notification(f"Nie znaleziono lekcji o ID: {lesson_id}", "error")
        return
    
    # Nagłówek lekcji
    render_dashboard_header(f"Lekcja: {lesson.get('title', 'Bez tytułu')}")
    
    # Wprowadzenie do lekcji
    with st.container():
        st.markdown(f"### {lesson.get('title', 'Bez tytułu')}")
        st.markdown(f"{lesson.get('description', 'Opis lekcji')}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Informacje o lekcji:**")
            st.markdown(f"- **Czas trwania:** {lesson.get('duration', '10 min')}")
            st.markdown(f"- **Poziom trudności:** {lesson.get('difficulty', 'Podstawowy')}")
            st.markdown(f"- **XP do zdobycia:** {lesson.get('xp_reward', 50)}")
        
        # Przycisk rozpoczęcia lekcji
        if zen_button("Rozpocznij lekcję", key="btn-start-lesson-content"):
            # Logika rozpoczęcia lekcji - to zastępuje ukryty przycisk, który był wcześniej aktywowany przez inline JS
            st.session_state.lesson_started = True
            st.rerun()
    
    # Cele lekcji
    objectives = lesson.get('objectives', ['Zrozumienie kluczowych pojęć', 'Praktyczne zastosowanie wiedzy'])
    
    with st.container():
        st.markdown("### Cele lekcji")
        for i, objective in enumerate(objectives, 1):
            st.markdown(f"{i}. {objective}")

def show_lesson_summary(lesson_id, earned_xp, earned_coins):
    """
    Wyświetla podsumowanie lekcji używając nowego systemu UI zgodnego z CSP
    """
    # Inicjalizacja UI
    initialize_ui()
    
    # Pobierz dane lekcji
    lessons = load_lessons_data()
    lesson = lessons.get(lesson_id, None)
    
    if not lesson:
        notification(f"Nie znaleziono lekcji o ID: {lesson_id}", "error")
        return
    
    # Nagłówek podsumowania
    render_dashboard_header(f"Lekcja ukończona: {lesson.get('title', 'Bez tytułu')}")
    
    # Podsumowanie lekcji
    with st.container():
        st.markdown("### Gratulacje! Ukończyłeś lekcję.")
        st.markdown(f"Tytuł: **{lesson.get('title', 'Bez tytułu')}**")
        
        # Nagrody w responsywnej siatce
        st.markdown("### Zdobyte nagrody:")
        
        reward_cols = responsive_grid(columns_desktop=2, columns_tablet=2, columns_mobile=1)
        
        with reward_cols[0]:
            st.markdown(f"""
            <div style='padding: 20px; background-color: rgba(75, 192, 192, 0.1); border-radius: 10px; text-align: center;'>
                <div style='font-size: 2em;'>⭐</div>
                <div><strong>{earned_xp}</strong> XP</div>
            </div>
            """, unsafe_allow_html=True)
            
        with reward_cols[1]:
            st.markdown(f"""
            <div style='padding: 20px; background-color: rgba(255, 206, 86, 0.1); border-radius: 10px; text-align: center;'>
                <div style='font-size: 2em;'>💰</div>
                <div><strong>{earned_coins}</strong> DegenCoins</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Przycisk powrotu do drzewa umiejętności
        if zen_button("Powrót do drzewa umiejętności", key="btn-go-back"):
            # Logika powrotu - to zastępuje ukryty przycisk, który był wcześniej aktywowany przez inline JS
            st.session_state.return_to_skills = True
            st.rerun()
