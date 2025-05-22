import streamlit as st
import json
import random
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
import io
import base64
from utils.components import zen_header, notification, progress_bar
from utils.material3_components import apply_material3_theme
from utils.card_layout import create_card, create_grid, zen_section
from utils.layout import get_device_type
from data.users import load_user_data, save_user_data
from data.lessons import load_lessons, get_lesson_by_id

def show_lesson():
    """
    Wyświetla lekcję z układem kart
    """
    # Zastosuj style Material 3
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    num_columns = 1 if device_type == "mobile" else 2
    
    # Sprawdź, czy ID lekcji zostało ustawione w sesji
    if 'lesson_id' not in st.session_state:
        st.error("Nie wybrano lekcji!")
        return
    
    # Pobierz dane lekcji
    lesson_id = st.session_state.lesson_id
    lesson = get_lesson_by_id(lesson_id)
    
    if not lesson:
        st.error("Nie znaleziono lekcji!")
        return
    
    # Inicjalizuj stan lekcji
    if 'lesson_state' not in st.session_state or st.session_state.get('current_lesson_id') != lesson_id:
        st.session_state.lesson_state = "intro"  # intro, content, quiz, summary
        st.session_state.current_step = 0
        st.session_state.quiz_answers = {}
        st.session_state.quiz_completed = False
        st.session_state.current_lesson_id = lesson_id
        st.session_state.lesson_start_time = time.time()
    
    # Pobierz dane użytkownika
    users_data = load_user_data()
    user_data = users_data.get(st.session_state.username, {})
    completed_lessons = set(user_data.get("completed_lessons", []))
    
    # Nagłówek lekcji
    zen_section(lesson.get('title', 'Lekcja'), None, lesson.get('icon', '📚'))
    
    # Pasek postępu dostosowany do etapu lekcji
    if st.session_state.lesson_state == "intro":
        progress = 0
    elif st.session_state.lesson_state == "content":
        total_steps = len(lesson.get('content', []))
        progress = (st.session_state.current_step / total_steps) * 80 if total_steps > 0 else 0
    elif st.session_state.lesson_state == "quiz":
        progress = 80 + (len(st.session_state.quiz_answers) / len(lesson.get('quiz', []))) * 15 if lesson.get('quiz', []) else 95
    else:  # summary
        progress = 100
    
    # Wyświetl pasek postępu
    st.markdown(f"""
    <div style='margin-bottom: 20px;'>
        <div style='background-color: #f0f0f0; border-radius: 4px; height: 8px; width: 100%;'>
            <div style='background-color: var(--primary-color); border-radius: 4px; height: 8px; width: {progress}%;'></div>
        </div>
        <div style='display: flex; justify-content: space-between; margin-top: 5px; font-size: 0.8em; color: #666;'>
            <span>Start</span>
            <span>Treść</span>
            <span>Quiz</span>
            <span>Zakończenie</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Wyświetl odpowiednią część lekcji
    if st.session_state.lesson_state == "intro":
        show_lesson_intro(lesson)
    elif st.session_state.lesson_state == "content":
        show_lesson_content(lesson)
    elif st.session_state.lesson_state == "quiz":
        show_lesson_quiz(lesson)
    else:  # summary
        show_lesson_summary(lesson, user_data, users_data, completed_lessons)

    # Dodaj przycisk powrotu do poprzedniej strony
    st.markdown("---")
    
    if st.button("← Powrót do drzewa umiejętności"):
        # Przywróć stan strony do drzewa umiejętności
        st.session_state.page = 'skills'
        # Wyczyść stan lekcji
        if 'lesson_state' in st.session_state:
            del st.session_state.lesson_state
        if 'current_step' in st.session_state:
            del st.session_state.current_step
        if 'quiz_answers' in st.session_state:
            del st.session_state.quiz_answers
        if 'current_lesson_id' in st.session_state:
            del st.session_state.current_lesson_id
        st.rerun()

def show_lesson_intro(lesson):
    """
    Wyświetla wprowadzenie do lekcji w układzie kart
    """
    # Stwórz kartę z wprowadzeniem do lekcji
    create_card(
        title="O tej lekcji",
        icon=lesson.get('icon', '📚'),
        content=f"""
        <div style='padding: 10px 0;'>
            <p>{lesson.get('description', 'Opis lekcji')}</p>
            <div style='margin-top: 15px;'>
                <ul style='padding-left: 20px;'>
                    <li><strong>Czas trwania:</strong> {lesson.get('duration', '10 min')}</li>
                    <li><strong>Poziom trudności:</strong> {lesson.get('difficulty', 'Podstawowy')}</li>
                    <li><strong>XP do zdobycia:</strong> {lesson.get('xp_reward', 50)}</li>
                </ul>
            </div>
            <div style='margin-top: 20px;'>
                <button class='material-button' 
                    onclick="document.getElementById('btn-start-lesson-content').click()">
                    Rozpocznij lekcję
                </button>
            </div>
        </div>
        """,
        key="lesson_intro_card"
    )
    
    # Dodaj informacje o celach lekcji
    objectives = lesson.get('objectives', ['Zrozumienie kluczowych pojęć', 'Praktyczne zastosowanie wiedzy'])
    
    create_card(
        title="Cele lekcji",
        icon="🎯",
        content=f"""
        <div style='padding: 10px 0;'>
            <ul style='padding-left: 20px;'>
                {"".join([f'<li>{obj}</li>' for obj in objectives])}
            </ul>
        </div>
        """,
        key="lesson_objectives_card"
    )
    
    # Ukryty przycisk do przejścia do treści lekcji
    if st.button("Rozpocznij", key="btn-start-lesson-content", help="", label_visibility="collapsed"):
        st.session_state.lesson_state = "content"
        st.rerun()

def show_lesson_content(lesson):
    """
    Wyświetla treść lekcji w układzie kart
    """
    # Pobierz treść lekcji
    content_blocks = lesson.get('content', [])
    
    if not content_blocks:
        st.warning("Ta lekcja nie ma treści!")
        return
    
    # Sprawdź czy indeks kroku jest poprawny
    if st.session_state.current_step >= len(content_blocks):
        st.session_state.current_step = len(content_blocks) - 1
    
    # Pobierz aktualny blok treści
    current_block = content_blocks[st.session_state.current_step]
    
    # Wyświetl tytuł sekcji
    st.markdown(f"### {current_block.get('title', f'Krok {st.session_state.current_step + 1}')}")
    
    # Wyświetl treść bloku w karcie
    create_card(
        title=current_block.get('subtitle', 'Informacje'),
        icon=current_block.get('icon', '📝'),
        content=f"""
        <div style='padding: 10px 0;'>
            {current_block.get('content', 'Treść bloku')}
        </div>
        """,
        key=f"content_block_{st.session_state.current_step}_card"
    )
    
    # Dodatkowe materiały, jeśli są dostępne
    if 'resources' in current_block and current_block['resources']:
        create_card(
            title="Dodatkowe materiały",
            icon="📚",
            content=f"""
            <div style='padding: 10px 0;'>
                <ul style='padding-left: 20px;'>
                    {"".join([f'<li><a href="{res.get("url", "#")}" target="_blank">{res.get("title", "Materiał")}</a></li>' for res in current_block['resources']])}
                </ul>
            </div>
            """,
            key=f"resources_block_{st.session_state.current_step}_card"
        )
    
    # Przyciski nawigacji
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.current_step > 0:
            if st.button("← Poprzedni"):
                st.session_state.current_step -= 1
                st.rerun()
    
    with col3:
        next_text = "Dalej →" if st.session_state.current_step < len(content_blocks) - 1 else "Przejdź do quizu →"
        if st.button(next_text):
            if st.session_state.current_step < len(content_blocks) - 1:
                st.session_state.current_step += 1
            else:
                # Przejdź do quizu, jeśli jest dostępny
                if lesson.get('quiz', []):
                    st.session_state.lesson_state = "quiz"
                else:
                    # Jeśli nie ma quizu, przejdź do podsumowania
                    st.session_state.lesson_state = "summary"
            st.rerun()

def show_lesson_quiz(lesson):
    """
    Wyświetla quiz w układzie kart
    """
    # Pobierz pytania quizu
    quiz_questions = lesson.get('quiz', [])
    
    if not quiz_questions:
        st.warning("Ta lekcja nie ma quizu!")
        st.session_state.lesson_state = "summary"
        st.rerun()
        return
    
    # Nagłówek quizu
    st.markdown("### Quiz sprawdzający wiedzę")
    
    # Inicjalizuj wyniki quizu, jeśli jeszcze nie istnieją
    if 'quiz_results' not in st.session_state:
        st.session_state.quiz_results = {}
    
    # Iteracja przez pytania quizu
    for i, question in enumerate(quiz_questions):
        question_id = f"q{i}"
        
        # Wyświetl pytanie jako kartę
        create_card(
            title=f"Pytanie {i+1}",
            icon="❓",
            content=f"""
            <div style='padding: 10px 0;'>
                <p>{question.get('question', 'Treść pytania')}</p>
            </div>
            """,
            key=f"quiz_question_{question_id}_card"
        )
        
        # Wyświetl opcje odpowiedzi poza kartą
        options = question.get('options', [])
        
        # Sprawdź, czy użytkownik już odpowiedział na to pytanie
        user_answer = st.session_state.quiz_answers.get(question_id)
        correct_answer = question.get('correct_answer')
        
        # Stan po udzieleniu odpowiedzi - pokaż czy odpowiedź była poprawna
        if user_answer is not None and 'quiz_completed' in st.session_state and st.session_state.quiz_completed:
            if user_answer == correct_answer:
                st.success("✓ Poprawna odpowiedź!")
                st.session_state.quiz_results[question_id] = True
            else:
                st.error(f"✗ Niepoprawna odpowiedź. Poprawna odpowiedź: {options[correct_answer]}")
                st.session_state.quiz_results[question_id] = False
        else:
            # Wyświetl opcje odpowiedzi jako przyciski
            for j, option in enumerate(options):
                button_style = ""
                if user_answer == j:
                    button_style = "background-color: #4CAF50; color: white;"
                
                if st.button(option, key=f"option_{question_id}_{j}", disabled=user_answer is not None):
                    st.session_state.quiz_answers[question_id] = j
                    st.rerun()
        
        st.markdown("---")
    
    # Sprawdź, czy wszystkie pytania mają odpowiedzi
    all_answered = len(st.session_state.quiz_answers) == len(quiz_questions)
    
    # Przycisk zakończenia quizu
    if all_answered and not st.session_state.quiz_completed:
        if st.button("Zakończ quiz"):
            st.session_state.quiz_completed = True
            st.rerun()
    
    # Przycisk przejścia do podsumowania
    if st.session_state.quiz_completed:
        # Oblicz wynik
        correct_count = sum(1 for result in st.session_state.quiz_results.values() if result)
        total_count = len(quiz_questions)
        score_percentage = (correct_count / total_count) * 100 if total_count > 0 else 0
        
        st.markdown(f"""
        <div style='background-color: #f0f0f0; padding: 15px; border-radius: 8px; margin: 20px 0;'>
            <h3>Twój wynik: {correct_count}/{total_count} ({score_percentage:.0f}%)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Przejdź do podsumowania"):
            st.session_state.quiz_score = score_percentage
            st.session_state.lesson_state = "summary"
            st.rerun()

def show_lesson_summary(lesson, user_data, users_data, completed_lessons):
    """
    Wyświetla podsumowanie lekcji w układzie kart
    """
    # Oblicz czas spędzony na lekcji
    lesson_duration = time.time() - st.session_state.get('lesson_start_time', time.time())
    lesson_minutes = int(lesson_duration / 60)
    lesson_seconds = int(lesson_duration % 60)
    
    # Wynik quizu, jeśli był
    quiz_score = st.session_state.get('quiz_score', 100)
    
    # Oblicz zdobyte XP i monety
    base_xp = lesson.get('xp_reward', 50)
    quiz_multiplier = quiz_score / 100.0
    earned_xp = int(base_xp * quiz_multiplier)
    earned_coins = int(earned_xp / 2)  # Monety to połowa XP
    
    # Sprawdź, czy lekcja była już ukończona
    lesson_id = st.session_state.current_lesson_id
    first_completion = lesson_id not in completed_lessons
    
    # Przyznaj nagrody tylko przy pierwszym ukończeniu
    if first_completion:
        # Aktualizuj dane użytkownika
        user_data['xp'] = user_data.get('xp', 0) + earned_xp
        user_data['degen_coins'] = user_data.get('degen_coins', 0) + earned_coins
        
        # Dodaj lekcję do ukończonych
        if 'completed_lessons' not in user_data:
            user_data['completed_lessons'] = []
        user_data['completed_lessons'].append(lesson_id)
        
        # Zapisz dane
        save_user_data(users_data)
    
    # Wyświetl gratulacje i podsumowanie w karcie
    create_card(
        title="Gratulacje!",
        icon="🎉",
        content=f"""
        <div style='padding: 15px 0; text-align: center;'>
            <h2>Ukończyłeś lekcję!</h2>
            <p>Czas trwania: {lesson_minutes} min {lesson_seconds} sek</p>
            <div style='margin: 20px 0;'>
                {"<p style='color: #4CAF50; font-weight: bold;'>Pierwsze ukończenie!</p>" if first_completion else "<p>Już wcześniej ukończyłeś tę lekcję.</p>"}
                <p>{"Zdobyte nagrody:" if first_completion else "Nagrody za pierwsze ukończenie:"}</p>
                <div style='display: flex; justify-content: center; gap: 30px; margin-top: 15px;'>
                    <div style='text-align: center;'>
                        <div style='font-size: 2em;'>⭐</div>
                        <div><strong>{earned_xp}</strong> XP</div>
                    </div>
                    <div style='text-align: center;'>
                        <div style='font-size: 2em;'>💰</div>
                        <div><strong>{earned_coins}</strong> DegenCoins</div>
                    </div>
                </div>
            </div>
            <div style='margin-top: 20px;'>
                <button class='material-button' 
                    onclick="document.getElementById('btn-go-back').click()">
                    Powrót do drzewa umiejętności
                </button>
            </div>
        </div>
        """,
        key="lesson_summary_card"
    )
    
    # Wyświetl podsumowanie wiedzy w karcie
    key_points = lesson.get('key_points', ['Zrozumienie podstawowych pojęć', 'Praktyczne zastosowanie wiedzy'])
    
    create_card(
        title="Kluczowe informacje",
        icon="📝",
        content=f"""
        <div style='padding: 10px 0;'>
            <p>Podsumowanie najważniejszych elementów lekcji:</p>
            <ul style='padding-left: 20px; margin-top: 10px;'>
                {"".join([f'<li>{point}</li>' for point in key_points])}
            </ul>
        </div>
        """,
        key="lesson_key_points_card"
    )
    
    # Ukryty przycisk do powrotu
    if st.button("Powrót", key="btn-go-back", help="", label_visibility="collapsed"):
        st.session_state.page = 'skills'
        # Wyczyść stan lekcji
        if 'lesson_state' in st.session_state:
            del st.session_state.lesson_state
        if 'current_step' in st.session_state:
            del st.session_state.current_step
        if 'quiz_answers' in st.session_state:
            del st.session_state.quiz_answers
        if 'current_lesson_id' in st.session_state:
            del st.session_state.current_lesson_id
        st.rerun()
    
    # Dodaj styl dla przycisków
    st.markdown("""
    <style>
    .material-button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.3s;
    }
    
    .material-button:hover {
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)
