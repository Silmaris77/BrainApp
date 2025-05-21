import streamlit as st
from data.lessons import load_lessons
from data.users import load_user_data, save_user_data
from utils.components import zen_header, zen_button, notification, content_section, tip_block, quote_block, progress_bar, embed_content, lesson_card
from utils.material3_components import apply_material3_theme
from utils.layout import get_device_type, responsive_grid, responsive_container, toggle_device_view

def get_difficulty_stars(difficulty):
    """Konwertuje poziom trudności (liczba lub tekst) na odpowiednią liczbę gwiazdek."""
    difficulty_map = {
        "beginner": 1,
        "podstawowy": 1,
        "intermediate": 2,
        "średni": 2,
        "średniozaawansowany": 3,
        "advanced": 4,
        "zaawansowany": 4,
        "expert": 5,
        "ekspercki": 5
    }
    
    if isinstance(difficulty, str):
        difficulty_level = difficulty_map.get(difficulty.lower(), 1)
    else:
        pass
        try:
            difficulty_level = int(difficulty)
        except (ValueError, TypeError):
            difficulty_level = 1
    
    return '⭐' * difficulty_level

def show_lesson():
    """Show lesson view"""
    
    # Zastosuj style Material 3
    apply_material3_theme()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    zen_header("Kurs Zen Degen Academy")
    lessons = load_lessons()
    
    # Check if we're viewing a specific lesson or the overview
    if 'current_lesson' not in st.session_state or not st.session_state.current_lesson:
        # WIDOK PRZEGLĄDU LEKCJI
        st.subheader("Dostępne lekcje")
        
        # Pobierz dane użytkownika dla oznaczenia ukończonych lekcji
        users_data = load_user_data()
        user_data = users_data.get(st.session_state.username, {})
        completed_lessons = user_data.get('completed_lessons', [])
        
        # Grupuj lekcje według kategorii
        lessons_by_category = {}
        for lesson_id, lesson in lessons.items():
            category = lesson.get("category", "Inne")
            if category not in lessons_by_category:
                lessons_by_category[category] = []
            lessons_by_category[category].append((lesson_id, lesson))
          # Wyświetl lekcje w podziale na kategorie
        for category, category_lessons in lessons_by_category.items():
            st.markdown(f"## {category}")            # Wyświetlaj każdą kartę lekcji na całą szerokość wiersza
            for i, (lesson_id, lesson) in enumerate(category_lessons):
                # Sprawdź, czy lekcja jest ukończona
                is_completed = lesson_id in completed_lessons
                
                # Użyj komponentu lesson_card zamiast ręcznego HTML
                lesson_card(
                    title=lesson.get('title', 'Lekcja'),
                    description=lesson.get('description', 'Ta lekcja wprowadza podstawowe zasady...'),
                    xp=lesson.get('xp_reward', 30),
                    difficulty=lesson.get('difficulty', 'beginner'),
                    category=lesson.get('tag', category),
                    completed=is_completed,                    button_text="Powtórz lekcję" if is_completed else "Rozpocznij",
                    button_key=f"start_{lesson_id}",
                    lesson_id=lesson_id,
                    on_click=lambda lesson_id=lesson_id: (
                        setattr(st.session_state, 'current_lesson', lesson_id),
                        setattr(st.session_state, 'lesson_step', 'intro'),
                        setattr(st.session_state, 'quiz_score', 0) if 'quiz_score' in st.session_state else None,
                        st.rerun()
                    )
                )
    else:
        # Kod wyświetlania pojedynczej lekcji
        lesson_id = st.session_state.current_lesson
        if lesson_id not in lessons:
            st.error("Nie znaleziono wybranej lekcji.")
            return
            
        lesson = lessons[lesson_id]
        
        if 'lesson_step' not in st.session_state:
            st.session_state.lesson_step = 'intro'
        if 'quiz_score' not in st.session_state:
            st.session_state.quiz_score = 0
        
        # Inicjalizacja śledzenia postępu przy pierwszym otwarciu lekcji
        # Inicjalizacja pełnego słownika śledzenia postępu
        if 'lesson_progress' not in st.session_state:
            st.session_state.lesson_progress = {
                'intro': False,
                'opening_quiz': False,
                'content': False,
                'reflection': False,
                'application': False,
                'closing_quiz': False,
                'summary': False,
                'total_xp_earned': 0,
                'steps_completed': 0,
                'quiz_scores': {},  # Do śledzenia wyników quizów
                'answers': {}       # Do śledzenia odpowiedzi użytkownika
            }
        
        # Oblicz całkowitą liczbę dostępnych kroków w tej lekcji
        available_steps = ['intro', 'content', 'reflection', 'summary']
        if 'sections' in lesson:
            if 'opening_quiz' in lesson.get('sections', {}):
                available_steps.append('opening_quiz')
            if 'application' in lesson.get('sections', {}):
                available_steps.append('application')
            if 'closing_quiz' in lesson.get('sections', {}):
                available_steps.append('closing_quiz')
        
        # Ustal kolejność kroków
        step_order = ['intro']
        if 'opening_quiz' in available_steps:
            step_order.append('opening_quiz')
        step_order.extend(['content', 'reflection'])
        if 'application' in available_steps:
            step_order.append('application')
        if 'closing_quiz' in available_steps:
            step_order.append('closing_quiz')
        step_order.append('summary')
        
        total_steps = len(step_order)
        max_xp = lesson.get('xp_reward', 100)
        
        # Mapowanie kroków do nazw wyświetlanych
        step_names = {
            'intro': 'Wprowadzenie',
            'opening_quiz': 'Quiz startowy',
            'content': 'Materiał',
            'reflection': 'Refleksja',
            'application': 'Zadania praktyczne',
            'closing_quiz': 'Quiz końcowy',
            'summary': 'Podsumowanie'
        }
        
        # Mapowanie kroków do wartości XP
        step_xp_values = {
            'intro': int(max_xp * 0.10),          # 10% całkowitego XP
            'opening_quiz': int(max_xp * 0.15),   # 15% całkowitego XP
            'content': int(max_xp * 0.20),        # 20% całkowitego XP
            'reflection': int(max_xp * 0.15),     # 15% całkowitego XP
            'application': int(max_xp * 0.15),    # 15% całkowitego XP
            'closing_quiz': int(max_xp * 0.15),   # 15% całkowitego XP
            'summary': int(max_xp * 0.10)         # 10% całkowitego XP
        }
        
        # Znajdź indeks obecnego kroku i następnego kroku
        current_step_idx = step_order.index(st.session_state.lesson_step) if st.session_state.lesson_step in step_order else 0
        next_step_idx = min(current_step_idx + 1, len(step_order) - 1)
        next_step = step_order[next_step_idx]
        
        # Wyświetl pasek postępu na górze strony
        current_progress = st.session_state.lesson_progress.get('steps_completed', 0) / total_steps
        current_xp = st.session_state.lesson_progress.get('total_xp_earned', 0)
        
        # Style dla paska postępu i interfejsu
        st.markdown("""
        <style>
        .progress-container {
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 10px 15px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .progress-text {
            font-weight: bold;
            font-size: 16px;
        }
        .xp-counter {
            color: #4CAF50;
            font-weight: bold;
            font-size: 18px;
        }
        .stTabs [data-baseweb="tab-panel"] {
            padding: 25px 15px 15px 15px;
        }
        .next-button {
            margin-top: 20px;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"<div class='progress-text'>Postęp lekcji:</div>", unsafe_allow_html=True)
            progress_bar(current_progress)
        with col2:
            st.markdown(f"<div class='xp-counter'>{current_xp} / {max_xp} XP</div>", unsafe_allow_html=True)

        # Lesson navigation in sidebar
        with st.sidebar:
            st.markdown("<h3>Nawigacja lekcji</h3>", unsafe_allow_html=True)
            
            # Dodaj przycisk powrotu do przeglądu lekcji
            if zen_button("Wszystkie lekcje", use_container_width=True):
                st.session_state.current_lesson = None
                st.rerun()
            
            # Wyświetl pełną mapę kroków lekcji z zaznaczeniem obecnego
            st.markdown("<h4>Mapa lekcji:</h4>", unsafe_allow_html=True)
            
            # Dodaj style dla przycisków nawigacji
            st.markdown("""
            <style>
            .nav-btn-current {
                background-color: #2196F3 !important;
                color: white !important;
                font-weight: bold !important;
                pointer-events: none;
            }
            .nav-btn-completed {
                background-color: #4CAF50 !important;
                color: white !important;
            }
            .nav-btn-locked {
                background-color: #f0f2f6 !important;
                color: #666 !important;
                pointer-events: none;
            }
            </style>
            """, unsafe_allow_html=True)

            for i, step in enumerate(step_order):
                if step in available_steps:
                    step_name = step_names.get(step, step.capitalize())
                    
                    # Sprawdź status kroku
                    is_completed = st.session_state.lesson_progress.get(step, False)
                    is_current = (step == st.session_state.lesson_step)
                    
                    # Ikony statusu
                    check_icon = "✅ " if is_completed else ""
                    current_icon = "👉 " if is_current else ""
                    
                    # Tekst przycisku - bez ikony dla aktualnego kroku jeśli jest już ikona ukończenia
                    if is_current and is_completed:
                        button_text = f"{current_icon}{i+1}. {step_name}"
                    else:
                        button_text = f"{current_icon if is_current else ''}{check_icon if is_completed and not is_current else ''}{i+1}. {step_name}"
                    
                    # Wyświetl element w odpowiednim stylu
                    if is_current:
                        # Element aktualny - niebieski przycisk (ten sam kształt co ukończone elementy)
                        st.button(button_text, key=f"current_step_{step}", disabled=True, use_container_width=True)
                        # Stylizuj przycisk za pomocą CSS
                        st.markdown("""
                        <style>
                        button[data-testid="baseButton-secondary"]:disabled {
                            background-color: #1976D2 !important;
                            color: white !important;
                            opacity: 1 !important;
                            font-weight: bold !important;
                            cursor: default !important;
                            border-radius: 5px !important;
                            box-shadow: none !important;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                    elif is_completed:
                        # Ukończony element - zielony, klikalny
                        if st.button(button_text, key=f"completed_step_{step}", use_container_width=True):
                            # Przejdź do wybranego kroku po kliknięciu
                            st.session_state.lesson_step = step
                            st.rerun()
                        # Stylizuj przycisk za pomocą CSS
                        st.markdown("""
                        <style>
                        button[data-testid="baseButton-secondary"]:not(:disabled) {
                            background-color: #4CAF50 !important;
                            color: white !important;
                            border-radius: 5px !important;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                    else:
                        # Przyszły element - szary div
                        st.markdown(
                            f"""
                            <div style="color: #666; padding: 8px; 
                                      border-radius: 5px; margin-bottom: 5px; text-align: center;">
                                {i+1}. {step_name}
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )

        # Main content
        st.markdown("<div class='st-bx'>", unsafe_allow_html=True)
        
        # Nagłówek sekcji
        st.markdown(f"<h1>{step_names.get(st.session_state.lesson_step, st.session_state.lesson_step.capitalize())}</h1>", unsafe_allow_html=True)
        
        # Main content logic for each step
        if st.session_state.lesson_step == 'intro':
            # Podziel wprowadzenie na dwie zakładki
            intro_tabs = st.tabs(["Wprowadzenie", "Case Study"])
            
            with intro_tabs[0]:
                # Wyświetl główne wprowadzenie
                if isinstance(lesson.get("intro"), dict) and "main" in lesson["intro"]:
                    st.markdown(lesson["intro"]["main"], unsafe_allow_html=True)
                elif isinstance(lesson.get("intro"), str):
                    st.markdown(lesson["intro"], unsafe_allow_html=True)
                else:
                    st.warning("Brak treści wprowadzenia.")
            
            with intro_tabs[1]:
                # Wyświetl studium przypadku
                if isinstance(lesson.get("intro"), dict) and "case_study" in lesson["intro"]:
                    st.markdown(lesson["intro"]["case_study"], unsafe_allow_html=True)
                else:
                    st.warning("Brak studium przypadku w tej lekcji.")
            
            # Przycisk "Dalej" po wprowadzeniu
            st.markdown("<div class='next-button'>", unsafe_allow_html=True)
            if zen_button(f"Dalej: {step_names.get(next_step, next_step.capitalize())} (+{step_xp_values['intro']} XP)", use_container_width=False):
                # Oznacz wprowadzenie jako ukończone, jeśli jeszcze nie było
                if not st.session_state.lesson_progress['intro']:
                    st.session_state.lesson_progress['intro'] = True
                    st.session_state.lesson_progress['steps_completed'] += 1
                    st.session_state.lesson_progress['total_xp_earned'] += step_xp_values['intro']
                    
                    # Powiadomienie o zdobytych XP
                    st.session_state.show_xp_notification = f"Zdobyłeś {step_xp_values['intro']} XP za ukończenie wprowadzenia!"
                
                # Przejdź do następnego kroku
                st.session_state.lesson_step = next_step
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        elif st.session_state.lesson_step == 'opening_quiz' and 'opening_quiz' in lesson.get('sections', {}):
            # Wyświetl quiz startowy
            quiz_data = lesson['sections']['opening_quiz']
            quiz_complete, _, earned_points = display_quiz(quiz_data)
            
            # Przycisk "Dalej" po quizie startowym - ZAWSZE aktywny
            st.markdown("<div class='next-button'>", unsafe_allow_html=True)
            
            # Przycisk jest zawsze aktywny, niezależnie od ukończenia quizu
            if zen_button(f"Dalej: {step_names.get(next_step, next_step.capitalize())} (+{step_xp_values['opening_quiz']} XP)", use_container_width=False):
                # Oznacz quiz jako ukończony, jeśli jeszcze nie był
                if not st.session_state.lesson_progress['opening_quiz']:
                    st.session_state.lesson_progress['opening_quiz'] = True
                    st.session_state.lesson_progress['steps_completed'] += 1
                    
                    # Podstawowe XP za quiz - przyznawane zawsze, bez bonusu
                    quiz_xp = step_xp_values['opening_quiz']
                    
                    # Dodaj XP do konta - bez bonusu
                    st.session_state.lesson_progress['total_xp_earned'] += quiz_xp
                    
                    # Powiadomienie o zdobytych XP - uproszczone, bez informacji o wyniku
                    st.session_state.show_xp_notification = f"Zdobyłeś {quiz_xp} XP za udział w quizie startowym!"
                
                # Przejdź do następnego kroku
                st.session_state.lesson_step = next_step
                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        elif st.session_state.lesson_step == 'content':
            # Diagnozowanie problemu z wyświetlaniem treści
            if 'sections' not in lesson:
                st.error("Lekcja nie zawiera klucza 'sections'!")
            elif 'learning' not in lesson.get('sections', {}):
                st.error("Lekcja nie zawiera sekcji 'learning'!")
            elif 'sections' not in lesson['sections'].get('learning', {}):
                st.error("Sekcja 'learning' nie zawiera klucza 'sections'!")
            else:
                # Sprawdź, czy sekcja learning istnieje i czy zawiera sections
                for i, section in enumerate(lesson["sections"]["learning"]["sections"]):
                    with st.expander(section.get("title", f"Sekcja {i+1}"), expanded=False):
                        st.markdown(section.get("content", "Brak treści"), unsafe_allow_html=True)
    
            # Przycisk "Dalej" po treści lekcji
            st.markdown("<div class='next-button'>", unsafe_allow_html=True)
            if zen_button(f"Dalej: {step_names.get(next_step, next_step.capitalize())} (+{step_xp_values['content']} XP)", use_container_width=False):
                # Oznacz treść jako ukończoną, jeśli jeszcze nie była
                if not st.session_state.lesson_progress['content']:
                    st.session_state.lesson_progress['content'] = True
                    st.session_state.lesson_progress['steps_completed'] += 1
                    st.session_state.lesson_progress['total_xp_earned'] += step_xp_values['content']                    
                    # Powiadomienie o zdobytych XP
                    st.session_state.show_xp_notification = f"Zdobyłeś {step_xp_values['content']} XP za zapoznanie się z materiałem!"
                  # Przejdź do następnego kroku
                st.session_state.lesson_step = next_step
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        
        elif st.session_state.lesson_step == 'reflection':
            # Wyświetl sekcje refleksji
            if 'sections' not in lesson:
                st.error("Lekcja nie zawiera klucza 'sections'!")
            elif 'reflection' not in lesson.get('sections', {}):
                st.error("Lekcja nie zawiera sekcji 'reflection'!")
            elif 'sections' not in lesson['sections'].get('reflection', {}):
                st.error("Sekcja 'reflection' nie zawiera klucza 'sections'!")
            else:
                # Wyświetl sekcje refleksji
                for section in lesson["sections"]["reflection"]["sections"]:
                    st.markdown(f"### {section.get('title', 'Zadanie refleksyjne')}")
                    st.markdown(section.get("content", "Brak treści"), unsafe_allow_html=True)
                    
                    # Generuj klucz dla przechowywania odpowiedzi
                    reflection_key = f"reflection_{section.get('title', '').replace(' ', '_').lower()}"
                    
                    # Generuj INNY klucz dla widgetu tekstowego
                    widget_key = f"input_{reflection_key}"
                    
                    # Użyj formularza, aby uniknąć problemów z aktualizacją stanu sesji
                    with st.form(key=f"form_{reflection_key}"):
                        # Pobierz istniejącą odpowiedź (jeśli jest)
                        existing_response = st.session_state.get(reflection_key, "")
                        
                        # Wyświetl pole tekstowe z istniejącą odpowiedzią
                        user_reflection = st.text_area(
                            "Twoja odpowiedź:",
                            value=existing_response,
                            height=200,
                            key=widget_key
                        )
                        
                        # Przycisk do zapisywania odpowiedzi w formularzu
                        submitted = st.form_submit_button("Zapisz odpowiedź")
                        
                        if submitted:
                            # Zapisz odpowiedź w stanie sesji
                            st.session_state[reflection_key] = user_reflection
                            st.success("Twoja odpowiedź została zapisana!")
            
            # Przycisk "Dalej" po refleksji
            st.markdown("<div class='next-button'>", unsafe_allow_html=True)
            if zen_button(f"Dalej: {step_names.get(next_step, next_step.capitalize())} (+{step_xp_values['reflection']} XP)", use_container_width=False):                
                # Oznacz refleksję jako ukończoną, jeśli jeszcze nie była
                if not st.session_state.lesson_progress['reflection']:
                    st.session_state.lesson_progress['reflection'] = True
                    st.session_state.lesson_progress['steps_completed'] += 1
                    st.session_state.lesson_progress['total_xp_earned'] += step_xp_values['reflection']
                    
                    # Powiadomienie o zdobytych XP
                    st.session_state.show_xp_notification = f"Zdobyłeś {step_xp_values['reflection']} XP za wykonanie zadań refleksyjnych!"
                
                # Przejdź do następnego kroku
                st.session_state.lesson_step = next_step
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        
        elif st.session_state.lesson_step == 'application':
            # Wyświetl zadania praktyczne
            if 'sections' not in lesson:
                st.error("Lekcja nie zawiera klucza 'sections'!")
            elif 'application' not in lesson.get('sections', {}):
                st.error("Lekcja nie zawiera sekcji 'application'!")
            elif 'sections' not in lesson['sections'].get('application', {}):
                st.error("Sekcja 'application' nie zawiera klucza 'sections'!")
            else:
                # Wyświetl zadania praktyczne
                for section in lesson["sections"]["application"]["sections"]:
                    st.markdown(f"### {section.get('title', 'Zadanie praktyczne')}")
                    st.markdown(section.get("content", "Brak treści"), unsafe_allow_html=True)
                    
                    # Generuj klucz dla przechowywania odpowiedzi
                    task_key = f"application_{section.get('title', '').replace(' ', '_').lower()}"
                    
                    # Użyj formularza, aby uniknąć problemów z aktualizacją stanu sesji
                    with st.form(key=f"form_{task_key}"):
                        # Pobierz istniejącą odpowiedź (jeśli jest)
                        existing_solution = st.session_state.get(task_key, "")
                        
                        # Wyświetl pole tekstowe z istniejącą odpowiedzią
                        user_solution = st.text_area(
                            "Twoje rozwiązanie:",
                            value=existing_solution,
                            height=200,
                            key=f"input_{task_key}"
                        )
                        
                        # Przycisk do zapisywania odpowiedzi w formularzu
                        submitted = st.form_submit_button("Zapisz rozwiązanie")
                        
                        if submitted:
                            # Zapisz odpowiedź w stanie sesji
                            st.session_state[task_key] = user_solution
                            st.success("Twoje rozwiązanie zostało zapisana!")
                            # Dodaj odświeżenie strony po zapisaniu
                            st.rerun()
            
            # Przycisk "Dalej" po zadaniach praktycznych
            st.markdown("<div class='next-button'>", unsafe_allow_html=True)
            if zen_button(f"Dalej: {step_names.get(next_step, next_step.capitalize())} (+{step_xp_values['application']} XP)", use_container_width=False):
                # Oznacz zadania praktyczne jako ukończone, jeśli jeszcze nie były
                if not st.session_state.lesson_progress['application']:
                    st.session_state.lesson_progress['application'] = True
                    st.session_state.lesson_progress['steps_completed'] += 1
                    st.session_state.lesson_progress['total_xp_earned'] += step_xp_values['application']
                    
                    # Powiadomienie o zdobytych XP
                    st.session_state.show_xp_notification = f"Zdobyłeś {step_xp_values['application']} XP za wykonanie zadań praktycznych!"
                
                # Przejdź do następnego kroku
                st.session_state.lesson_step = next_step
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        
        elif st.session_state.lesson_step == 'closing_quiz':
            # Wyświetl quiz końcowy
            if 'sections' not in lesson:
                st.error("Lekcja nie zawiera klucza 'sections'!")
            elif 'closing_quiz' not in lesson.get('sections', {}):
                st.error("Lekcja nie zawiera sekcji 'closing_quiz'!")
            else:
                # Użyj funkcji display_quiz do wyświetlenia quizu
                quiz_completed, quiz_passed, earned_points = display_quiz(lesson['sections']['closing_quiz'])
                
                # Jeśli quiz został ukończony i zaliczony, umożliw przejście dalej
                if quiz_completed:
                    # Przycisk "Dalej" po quizie końcowym
                    st.markdown("<div class='next-button'>", unsafe_allow_html=True)
                    if zen_button(f"Dalej: {step_names.get(next_step, next_step.capitalize())} (+{step_xp_values['closing_quiz']} XP)", use_container_width=False):
                        # Oznacz quiz końcowy jako ukończony, jeśli jeszcze nie był
                        if not st.session_state.lesson_progress['closing_quiz']:
                            st.session_state.lesson_progress['closing_quiz'] = True
                            st.session_state.lesson_progress['steps_completed'] += 1
                            st.session_state.lesson_progress['total_xp_earned'] += earned_points
                            
                            # Powiadomienie o zdobytych XP
                            st.session_state.show_xp_notification = f"Zdobyłeś {earned_points} XP za ukończenie quizu końcowego!"
                        
                        # Przejdź do następnego kroku
                        st.session_state.lesson_step = next_step
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
        
        elif st.session_state.lesson_step == 'summary':
            # Wyświetl podsumowanie lekcji w podziale na zakładki, podobnie jak wprowadzenie
            if 'outro' in lesson:
                # Podziel podsumowanie na dwie zakładki
                summary_tabs = st.tabs(["Podsumowanie", "Case Study"])
                
                with summary_tabs[0]:
                    # Wyświetl główne podsumowanie
                    if 'main' in lesson['outro']:
                        st.markdown(lesson['outro']['main'], unsafe_allow_html=True)
                    else:
                        st.warning("Brak głównego podsumowania.")
                
                with summary_tabs[1]:
                    # Wyświetl studium przypadku
                    if 'case_study' in lesson['outro']:
                        st.markdown(lesson['outro']['case_study'], unsafe_allow_html=True)
                    else:
                        st.warning("Brak studium przypadku w podsumowaniu.")
                
                # Wyświetl całkowitą zdobytą ilość XP
                total_xp = st.session_state.lesson_progress['total_xp_earned']
                st.success(f"Gratulacje! Ukończyłeś lekcję i zdobyłeś łącznie {total_xp} XP!")
                
                # Przycisk powrotu do wszystkich lekcji
                if zen_button("Wróć do wszystkich lekcji", use_container_width=False):
                    # Zapisz informację o ukończeniu lekcji w danych użytkownika
                    users_data = load_user_data()
                    if st.session_state.username in users_data:
                        if 'completed_lessons' not in users_data[st.session_state.username]:
                            users_data[st.session_state.username]['completed_lessons'] = []
                        
                        # Dodaj lekcję do ukończonych, jeśli jeszcze nie została dodana
                        lesson_id = st.session_state.current_lesson
                        if lesson_id not in users_data[st.session_state.username]['completed_lessons']:
                            users_data[st.session_state.username]['completed_lessons'].append(lesson_id)
                            
                            # Aktualizuj XP użytkownika
                            users_data[st.session_state.username]['xp'] = users_data[st.session_state.username].get('xp', 0) + total_xp
                            
                            # Zapisz zaktualizowane dane
                            save_user_data(users_data)
                    
                    # Powrót do przeglądu lekcji
                    st.session_state.current_lesson = None
                    st.rerun()
            elif 'summary' in lesson:
                # Obsługa starszego formatu, gdzie podsumowanie było bezpośrednio w lesson['summary']
                st.markdown(lesson['summary'], unsafe_allow_html=True)
            else:
                # Brak podsumowania w danych lekcji
                st.error("Lekcja nie zawiera podsumowania!")
        
        # Zamknij div .st-bx
        st.markdown("</div>", unsafe_allow_html=True)
def display_lesson(lesson_data):
    """Wyświetla lekcję z nowymi sekcjami quizów"""
    
    # Wyświetl tytuł lekcji
    st.markdown(f"<h1>{lesson_data['title']}</h1>", unsafe_allow_html=True)
    
    # Wyświetl wprowadzenie
    if 'intro' in lesson_data:
        st.markdown(lesson_data['intro'], unsafe_allow_html=True)
    
    # Przygotuj dane zakładek
    tab_data = []
    
    # Dodaj zakładki w odpowiedniej kolejności
    if 'opening_quiz' in lesson_data.get('sections', {}):
        tab_data.append(("Quiz startowy", "opening_quiz"))
    
    if 'learning' in lesson_data.get('sections', {}):
        tab_data.append(("Nauka", "learning"))
    
    if 'reflection' in lesson_data.get('sections', {}):
        tab_data.append(("Refleksja", "reflection"))
    
    if 'closing_quiz' in lesson_data.get('sections', {}):
        tab_data.append(("Quiz końcowy", "closing_quiz"))
    
    # Wyodrębnij tytuły zakładek
    tab_titles = [title for title, _ in tab_data]
    
    # Wyświetl zakładki tylko jeśli są jakieś dane do wyświetlenia
    if tab_titles:
        tabs = st.tabs(tab_titles)
          # Dla każdej zakładki wyświetl odpowiednią zawartość
        for i, (_, tab_name) in enumerate(tab_data):
            with tabs[i]:
                if tab_name in ["opening_quiz", "closing_quiz"]:
                    display_quiz(lesson_data['sections'][tab_name])
                elif tab_name == "learning":
                    display_learning_sections(lesson_data['sections'][tab_name])
                elif tab_name == "reflection":
                    display_reflection_sections(lesson_data['sections'][tab_name])
    else:
        st.warning("Ta lekcja nie zawiera żadnych sekcji do wyświetlenia.")


# Dodanie brakujących funkcji
def display_learning_sections(learning_data):
    """Wyświetla sekcje nauki z lekcji"""
    if not learning_data or 'sections' not in learning_data:
        st.warning("Brak treści edukacyjnych w tej lekcji.")
        return
        
    for section in learning_data['sections']:
        content_section(
            section.get("title", "Tytuł sekcji"), 
            section.get("content", "Brak treści"), 
            collapsed=False
        )


def display_reflection_sections(reflection_data):
    """Wyświetla sekcje refleksji z lekcji"""
    if not reflection_data:
        st.warning("Brak zadań refleksyjnych w tej lekcji.")
        return
        
    # Check if there are sections in the data
    if 'sections' not in reflection_data:
        st.warning("Dane refleksji nie zawierają sekcji.")
        return
        
    for section in reflection_data['sections']:
        st.markdown(f"### {section.get('title', 'Zadanie refleksyjne')}")
        st.markdown(section.get("content", "Brak treści"), unsafe_allow_html=True)
        
        # Dodaj pole tekstowe do wprowadzania odpowiedzi
        reflection_key = f"reflection_{section.get('title', '').replace(' ', '_').lower()}"
        user_reflection = st.text_area(
            "Twoja odpowiedź:",
            value=st.session_state.get(reflection_key, ""),
            height=200,
            key=reflection_key
        )
        
        # Dodaj przycisk do zapisywania odpowiedzi
        if st.button("Zapisz odpowiedź", key=f"save_{reflection_key}"):
            st.session_state[reflection_key] = user_reflection
            st.success("Twoja odpowiedź została zapisana!")

def display_quiz(quiz_data):
    """Wyświetla quiz z pytaniami i opcjami odpowiedzi. Zwraca True, gdy quiz jest ukończony."""
    
    if not quiz_data or "questions" not in quiz_data:
        st.warning("Ten quiz nie zawiera żadnych pytań.")
        return False, False, 0
        
    st.markdown(f"<h2>{quiz_data.get('title', 'Quiz')}</h2>", unsafe_allow_html=True)
    
    if "description" in quiz_data:
        st.markdown(quiz_data['description'])
    
    # Inicjalizacja stanu quizu jeśli jeszcze nie istnieje
    quiz_id = f"quiz_{quiz_data.get('title', '').replace(' ', '_').lower()}"
    if quiz_id not in st.session_state:
        st.session_state[quiz_id] = {
            "answered_questions": [],
            "correct_answers": 0,
            "total_questions": len(quiz_data['questions']),
            "completed": False
        }
    
    # Wyświetl wszystkie pytania
    for i, question in enumerate(quiz_data['questions']):
        question_id = f"{quiz_id}_q{i}"
        
        # Kontener dla pytania z własnymi stylami
        st.markdown(f"""
        <div class="quiz-question">
            <h3>Pytanie {i+1}: {question['question']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Jeśli pytanie już zostało odpowiedziane, pokaż wynik
        if i in st.session_state[quiz_id]["answered_questions"]:
            selected = st.session_state.get(f"{question_id}_selected")
            is_correct = selected == question.get('correct_answer')
            
            # Wyświetl odpowiedzi z oznaczeniem poprawnej
            for j, option in enumerate(question['options']):
                # Dodaj walidację correct_answer
                correct_answer = question.get('correct_answer', 0)
                if correct_answer < 0 or correct_answer >= len(question['options']):
                    correct_answer = 0  # Ustaw domyślną wartość, jeśli indeks jest nieprawidłowy
                
                if j == correct_answer:
                    st.markdown(f"✅ **{option}** _(Poprawna odpowiedź)_")
                elif j == selected and not is_correct:
                    st.markdown(f"❌ **{option}** _(Twoja odpowiedź)_")
                else:
                    st.markdown(f"○ {option}")
            
            # Wyświetl wyjaśnienie
            if "explanation" in question:
                st.info(question['explanation'])
            
            st.markdown("---")
        else:
            # Wyświetl opcje odpowiedzi jako przyciski
            options = []
            for j, option in enumerate(question['options']):
                if st.button(option, key=f"{question_id}_opt{j}"):
                    # Zapisz wybraną odpowiedź
                    st.session_state[f"{question_id}_selected"] = j
                    st.session_state[quiz_id]["answered_questions"].append(i)
                    
                    # Aktualizuj liczbę poprawnych odpowiedzi
                    if j == question.get('correct_answer'):
                        st.session_state[quiz_id]["correct_answers"] += 1
                        
                        # Aktualizuj wynik quizu (dla podsumowania lekcji)
                        if "quiz_score" in st.session_state:
                            st.session_state.quiz_score += 5  # 5 XP za poprawną odpowiedź
                    
                    # Sprawdź, czy quiz został ukończony
                    if len(st.session_state[quiz_id]["answered_questions"]) == st.session_state[quiz_id]["total_questions"]:
                        st.session_state[quiz_id]["completed"] = True
                    
                    # Odświeżenie strony
                    st.rerun()
            
            st.markdown("---")
    
    # Sprawdź czy quiz jest ukończony i oblicz punkty
    is_completed = st.session_state[quiz_id].get("completed", False)
    
    if is_completed:
        correct = st.session_state[quiz_id]["correct_answers"]
        total = st.session_state[quiz_id]["total_questions"]
        percentage = (correct / total) * 100
          # Oblicz punkty - wartość zależy od procentu odpowiedzi poprawnych
        # Domyślna wartość, jeśli nie mamy dostępu do step_xp_values
        quiz_xp_value = 15
        earned_points = int(quiz_xp_value * (percentage / 100))
        
        # Czy quiz został zdany (ponad 60%)
        is_passed = percentage >= 60
        
        st.markdown(f"""
        <div class="quiz-summary">
            <h3>Twój wynik: {correct}/{total} ({percentage:.0f}%)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if percentage >= 80:
            st.success("Świetnie! Doskonale rozumiesz ten temat.")
        elif percentage >= 60:
            st.info("Dobrze! Masz solidną wiedzę, ale warto jeszcze powtórzyć niektóre zagadnienia.")
        else:
            st.warning("Warto powtórzyć materiał z tej lekcji, aby lepiej zrozumieć kluczowe zagadnienia.")
        
        return is_completed, is_passed, earned_points
    
    # Quiz nie jest jeszcze ukończony
    return is_completed, False, 0

# Dodaj CSS do poprawy wyglądu expanderów, z uwzględnieniem urządzeń mobilnych
st.markdown("""
<style>
/* Style dla expanderów */
.st-emotion-cache-1oe5cao {
    padding: 10px;
    border-radius: 8px;
    margin-bottom: 16px;
    background-color: rgba(248,249,251,0.8);
}
.st-emotion-cache-1oe5cao:hover {
    background-color: rgba(242,244,248,1); 
}
.st-emotion-cache-16idsys p {
    font-size: 1rem;
    line-height: 1.6;
}
.st-expander {
    border: none !important;
}

/* Specjalne style dla urządzeń mobilnych */
@media (max-width: 768px) {
    /* Większy obszar klikalny dla expanderów */
    .st-expander {
        margin-bottom: 12px;
    }
    
    .st-expander .st-emotion-cache-16idsys p {
        font-size: 0.95rem; /* Nieco mniejsza czcionka na małych ekranach */
    }
    
    /* Zwiększony obszar kliknięcia dla nagłówka expandera */
    .st-expander-header {
        padding: 15px 10px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        min-height: 50px;
    }
    
    /* Dodaj wskaźnik rozwijania */
    .st-expander:not(.st-emotion-cache-xujm5h) .st-expander-header::after {
        content: '▼';
        float: right;
        margin-left: 10px;
        transition: transform 0.3s;
    }
    
    .st-expander.st-emotion-cache-xujm5h .st-expander-header::after {
        content: '▲';
        float: right;
        margin-left: 10px;
    }
}
</style>
""", unsafe_allow_html=True)
