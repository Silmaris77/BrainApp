import streamlit as st
from utils.components import zen_header, zen_button, notification, skill_node
from utils.material3_components import apply_material3_theme
from utils.layout import get_device_type, responsive_grid, responsive_container, toggle_device_view
from data.users import load_user_data, save_user_data
import random

def show_skill_tree():
    # Zastosuj style Material 3
    apply_material3_theme()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    # Inicjalizacja trybu ciemnego
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    
    # Dodaj CSS z nowymi stylami
    add_custom_css()
    
    # Inicjalizuj stan kontekstowego menu
    if 'context_menu_open' not in st.session_state:
        st.session_state.context_menu_open = False
        st.session_state.context_menu_category = None
    
    # Pobierz dane użytkownika
    users_data = load_user_data()
    user_data = users_data.get(st.session_state.username, {})
    user_skills = user_data.get("skills", {})
    user_xp = user_data.get("xp", 0)
    user_completed_lessons = set(user_data.get("completed_lessons", []))
      # Definicja bloków tematycznych - ZAKTUALIZOWANE dla Neuroliderów
    blocks = {
        1: {
            'name': '🔥 Blok 1: Neurobiologia przywództwa',
            'description': 'Poznaj neurobiologiczne podstawy przywództwa, wpływ mózgu na emocje i decyzje liderów.',
            'categories': [1, 2, 3],  # ID kategorii należących do tego bloku (moduły 1, 2, 3)
            'color': 'linear-gradient(135deg, #FF9950, #FF5E62)'
        },
        2: {
            'name': '🧠 Blok 2: Procesy decyzyjne lidera',
            'description': 'Modele podejmowania decyzji, błędy poznawcze i neurologiczne aspekty zmiany w przywództwie.',
            'categories': [4, 5, 6],
            'color': 'linear-gradient(135deg, #43C6AC, #191654)'
        },
        3: {
            'name': '🌍 Blok 3: Psychologia i motywacja w przywództwie',
            'description': 'Motywowanie siebie i innych, radzenie sobie ze stresem i zarządzanie emocjami w przywództwie.',
            'categories': [7, 8, 9],
            'color': 'linear-gradient(135deg, #6DD5FA, #2980B9)'
        },
        4: {
            'name': '💪 Blok 4: Praktyczne aspekty neuroprzywództwa',
            'description': 'Budowanie odporności, efektywność przywódcza i neuroprzywództwo w kontekście globalnym.',
            'categories': [10, 11, 12],
            'color': 'linear-gradient(135deg, #8E2DE2, #4A00E0)'
        },
        5: {
            'name': '🌍 Blok 5: Przyszłość neuroprzywództwa',
            'description': 'Wyzwania przyszłości, praca z umysłem lidera i transformacja przywódcza.',
            'categories': [13, 14, 15],
            'color': 'linear-gradient(135deg, #56ab2f, #a8e063)'
        }
    }
      # Definicja kategorii (modułów) - ZAKTUALIZOWANE dla Neuroliderów
    categories = {
        1: {
            'name': '🧠 Wprowadzenie do neuroprzywództwa',
            'id': 'neuro_leadership_intro',
            'block': 1,
            'icon': '🧠',
            'description': 'Podstawy neuroprzywództwa, struktura mózgu lidera i neurobiologiczne podstawy podejmowania decyzji',
            'lessons': get_lessons_for_category(1),
            'level': user_skills.get('neuro_leadership_intro', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,  # Zawsze odblokowane
            'cost': 50  # Koszt ulepszenia w XP
        },
        2: {
            'name': '💡 Mózg, emocje i decyzje',
            'id': 'brain_emotions_decisions',
            'block': 1,
            'icon': '💡',
            'description': 'Wpływ emocji na decyzje liderów, rola układu limbicznego i inteligencja emocjonalna',
            'lessons': get_lessons_for_category(2),
            'level': user_skills.get('brain_emotions_decisions', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 60
        },
        3: {
            'name': 'Mechanizmy mózgu w interakcjach społecznych',
            'id': 'brain_social_interactions',            'block': 1,
            'icon': '👥',
            'description': 'Współczucie i empatia w przywództwie, neurologiczne podstawy komunikacji i budowanie relacji',
            'lessons': get_lessons_for_category(3),
            'level': user_skills.get('brain_social_interactions', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 70
        },
        4: {
            'name': '⚖️ Modele podejmowania decyzji',
            'id': 'decision_models',
            'block': 2,
            'icon': '⚖️',
            'description': 'Teoria perspektywy, heurystyki, model SEEDS i analiza ryzyka w podejmowaniu decyzji',
            'lessons': get_lessons_for_category(4),
            'level': user_skills.get('decision_models', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 80
        },
        5: {
            'name': 'Błędy poznawcze w decyzjach',
            'id': 'cognitive_biases_leadership',
            'block': 2,
            'icon': '⚠️',
            'description': 'Rozpoznawanie i przeciwdziałanie błędom poznawczym w decyzjach liderów',
            'lessons': get_lessons_for_category(5),
            'level': user_skills.get('cognitive_biases_leadership', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 80
        },        6: {
            'name': 'Neurologiczne aspekty zmiany i innowacji',
            'id': 'neuro_change_innovation',
            'block': 2,
            'icon': '🔄',
            'description': 'Neuroplastyczność, reakcje mózgu na zmiany i neurobiologia innowacji i kreatywności',
            'lessons': get_lessons_for_category(6),
            'level': user_skills.get('neuro_change_innovation', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 80
        },
        7: {
            'name': 'Motywowanie siebie i innych',
            'id': 'motivation_leadership',
            'block': 3,
            'icon': '🔥',
            'description': 'Neurobiologia motywacji, budowanie zaangażowania i wzmacnianie poczucia sensu w zespole',
            'lessons': get_lessons_for_category(7),
            'level': user_skills.get('motivation_leadership', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 90
        },
        8: {
            'name': 'Neurobiologia stresu w przywództwie',
            'id': 'stress_neurobiology',
            'block': 3,
            'icon': '😓',
            'description': 'Mechanizmy neurobiologiczne stresu i techniki zarządzania stresem dla liderów',
            'lessons': get_lessons_for_category(8),
            'level': user_skills.get('stress_neurobiology', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 90
        },        9: {
            'name': 'Rola emocji w przywództwie',
            'id': 'emotions_leadership',
            'block': 3,
            'icon': '❤️',
            'description': 'Inteligencja emocjonalna, zarządzanie emocjami w trudnych sytuacjach i empatia w przywództwie',
            'lessons': get_lessons_for_category(9),
            'level': user_skills.get('emotions_leadership', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 100
        },
        10: {
            'name': 'Budowanie odporności lidera',
            'id': 'leader_resilience',
            'block': 4,
            'icon': '🛡️',
            'description': 'Odporność psychiczna, radzenie sobie z kryzysami i przekształcanie porażek w doświadczenia',
            'lessons': get_lessons_for_category(10),
            'level': user_skills.get('leader_resilience', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 100
        },
        11: {
            'name': 'Efektywność przywódcza w praktyce',
            'id': 'leadership_effectiveness',
            'block': 4,
            'icon': '📊',
            'description': 'Praktyczne zastosowanie neuroprzywództwa, delegowanie zadań i budowanie kultury organizacyjnej',
            'lessons': get_lessons_for_category(11),            'level': user_skills.get('leadership_effectiveness', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 110
        },12: {
            'name': 'Neuroprzywództwo w kontekście globalnym',
            'id': 'global_neuroleadership',
            'block': 4,
            'icon': '🌍',
            'description': 'Przywództwo w zespołach wielokulturowych, adaptacja stylów i globalne trendy',
            'lessons': get_lessons_for_category(12),
            'level': user_skills.get('global_neuroleadership', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 110
        },        13: {
            'name': 'Wyzwania przyszłości',
            'id': 'future_challenges',
            'block': 5,
            'icon': '🔮',
            'description': 'Przywództwo w erze AI, etyczne aspekty neurotechnologii i przyszłe trendy neuroprzywództwa',
            'lessons': get_lessons_for_category(13),
            'level': user_skills.get('future_challenges', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 120
        },        14: {
            'name': 'Praca z umysłem lidera',
            'id': 'leader_mind_work',
            'block': 5,
            'icon': '🧠',
            'description': 'Mindfulness dla liderów, techniki koncentracji i zarządzanie stresem w warunkach presji',
            'lessons': get_lessons_for_category(14),
            'level': user_skills.get('leader_mind_work', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 120
        },        15: {
            'name': 'Transformacja przywódcza',
            'id': 'leadership_transformation',
            'block': 5,
            'icon': '🔄',
            'description': 'Modele transformacji, coaching oparty na neuronaukach i budowanie uczącej się organizacji',
            'lessons': get_lessons_for_category(15),
            'level': user_skills.get('leadership_transformation', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 150
        }
    }
    
    # Zaktualizuj wszystkie kategorie jako odblokowane
    for cat_id in categories:
        categories[cat_id]['unlocked'] = True
      # Header i nowy tytuł
    st.markdown("<h1 class='skills-header'>Mapa Rozwoju Neuroliderów 🧠</h1>", unsafe_allow_html=True)
    
    # Dashboard postępu
    show_progress_dashboard(user_skills, user_xp, user_completed_lessons, categories)
    
    # Opcje filtrowania
    st.markdown("<h3 class='section-header'>Filtrowanie umiejętności</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        filter_option = st.selectbox(
            "Pokaż umiejętności:",
            ["Wszystkie", "W trakcie nauki", "Ukończone", "Nierozpoczęte"],
            index=0
        )
    
    with col2:
        sort_option = st.selectbox(
            "Sortuj według:",
            ["Bloku tematycznego", "Poziomu (rosnąco)", "Poziomu (malejąco)", "Alfabetycznie"],
            index=0
        )

    # Sekcja bloków ze zmienioną wizualizacją
    for block_id, block in blocks.items():
        display_block_with_skills(block_id, block, categories, user_skills, user_xp, users_data, 
                                  user_data, user_completed_lessons, filter_option, device_type)


def show_progress_dashboard(user_skills, user_xp, user_completed_lessons, categories):
    """Wyświetla dashboard postępu użytkownika"""
    
    # Oblicz średni poziom umiejętności
    skill_levels = [skill.get('level', 0) for skill in user_skills.values()]
    avg_level = sum(skill_levels) / len(skill_levels) if skill_levels else 0
    
    # Oblicz całkowity postęp (jako procent wszystkich możliwych umiejętności)
    total_possible_skills = sum(cat['max_level'] for cat in categories.values())
    current_total_level = sum(skill_levels)
    overall_progress = (current_total_level / total_possible_skills) * 100 if total_possible_skills > 0 else 0
    
    # Znajdź najwyższy poziom umiejętności
    max_skill_level = max(skill_levels) if skill_levels else 0
    
    # Liczba ukończonych lekcji
    completed_lessons_count = len(user_completed_lessons)
    
    # Oblicz estymowany czas do ukończenia (w dniach)
    total_lessons = sum(len(cat['lessons']) for cat in categories.values())
    remaining_lessons = total_lessons - completed_lessons_count
    estimated_completion_days = max(1, int(remaining_lessons / 2))  # Zakładając 2 lekcje dziennie
    
    # Dashboard z statystykami
    st.markdown("<div class='progress-dashboard'>", unsafe_allow_html=True)
    
    cols = st.columns(5)  # Zwiększamy ilość kolumn, aby dodać nową statystykę
    
    with cols[0]:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-icon'>🏆</div>
            <div class='stat-value'>{int(overall_progress)}%</div>
            <div class='stat-label'>Całkowity postęp</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-icon'>📚</div>
            <div class='stat-value'>{completed_lessons_count}</div>
            <div class='stat-label'>Ukończone lekcje</div>
        </div>
        """, unsafe_allow_html=True)
        
    with cols[2]:  # Naprawiam ten fragment - usuwam dwukropek
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-icon'>⭐</div>
            <div class='stat-value'>{int(avg_level)}</div>
            <div class='stat-label'>Średni poziom</div>
        </div>
        """, unsafe_allow_html=True)
        
    with cols[3]:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-icon'>💎</div>
            <div class='stat-value'>{user_xp}</div>
            <div class='stat-label'>Posiadane XP</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[4]:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-icon'>⏱️</div>
            <div class='stat-value'>{estimated_completion_days}</div>
            <div class='stat-label'>Dni do ukończenia</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Dodaj wizualizację postępu w różnych blokach umiejętności
    # Zbierz dane o postępie w każdym bloku
    block_progress = {}
    blocks_data = {}
    
    for cat_id, category in categories.items():
        block_id = category['block']
        
        # Inicjalizuj dane dla bloku jeśli nie istnieją
        if block_id not in blocks_data:
            blocks_data[block_id] = {
                'total_lessons': 0,
                'completed_lessons': 0,
                'name': f"Blok {block_id}"
            }
        
        # Dodaj lekcje do bloku
        category_lessons = category['lessons']
        blocks_data[block_id]['total_lessons'] += len(category_lessons)
        
        # Policz ukończone lekcje
        for lesson in category_lessons:
            if lesson['id'] in user_completed_lessons:
                blocks_data[block_id]['completed_lessons'] += 1
    
    # Oblicz procent ukończenia dla każdego bloku
    for block_id, data in blocks_data.items():
        if data['total_lessons'] > 0:
            completion_percent = (data['completed_lessons'] / data['total_lessons']) * 100
        else:
            completion_percent = 0
        
        block_progress[block_id] = {
            'name': data['name'],
            'progress': completion_percent
        }
    
    # Wyświetl wykres postępu bloków
    st.markdown("<h4 class='chart-title'>Postęp w blokach tematycznych</h4>", unsafe_allow_html=True)
    
    # Tworzenie danych dla wykresu
    chart_data = []
    for block_id, data in block_progress.items():
        chart_data.append({
            'Blok': f"Blok {block_id}",
            'Postęp (%)': data['progress']
        })
    
    if chart_data:
        import pandas as pd
        import altair as alt
        
        # Konwertuj do dataframe
        df = pd.DataFrame(chart_data)
        
        # Stwórz wykres
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('Blok:N', sort=None),
            y=alt.Y('Postęp (%):Q', scale=alt.Scale(domain=[0, 100])),
            color=alt.Color('Blok:N', scale=alt.Scale(scheme='category10')),
            tooltip=['Blok', 'Postęp (%)'
        ]).properties(
            width='container',
            height=200
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        )
        
        st.altair_chart(chart, use_container_width=True)
    
    # Krótka informacja o mechanice zdobywania poziomów
    st.markdown("""
        <div class="info-box">
            <h4>📋 Jak zdobywać poziomy umiejętności?</h4>
            <p>Każda ukończona lekcja zwiększa poziom danej umiejętności. Ukończ wszystkie 10 lekcji, aby osiągnąć maksymalny poziom!</p>
            <p>Wszystkie kategorie umiejętności są od razu dostępne - możesz rozpocząć naukę od dowolnego tematu.</p>
        </div>
    """, unsafe_allow_html=True)


def display_block_with_skills(block_id, block, categories, user_skills, user_xp, users_data, 
                             user_data, user_completed_lessons, filter_option, device_type):
    """Wyświetla blok tematyczny z kartami umiejętności w nowym układzie"""
    
    # Nagłówek bloku z nowym stylem
    st.markdown(f"""
        <div class="skill-block-header" style="background: {block['color']}">
            <h2>{block['name']}</h2>
            <p>{block['description']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Znajdź kategorie należące do bloku
    block_categories = [cat_id for cat_id, cat in categories.items() if cat['block'] == block_id]
    
    # Filtrowanie kategorii
    filtered_categories = []
    for cat_id in block_categories:
        category = categories[cat_id]
        category_lessons_ids = [lesson["id"] for lesson in category['lessons']]
        completed_category_lessons = [lesson_id for lesson_id in user_completed_lessons if lesson_id in category_lessons_ids]
        lessons_completed_count = len(completed_category_lessons)
        
        # Filtruj według wybranych opcji
        if filter_option == "W trakcie nauki" and (lessons_completed_count == 0 or lessons_completed_count == 10):
            continue
        elif filter_option == "Ukończone" and lessons_completed_count < 10:
            continue
        elif filter_option == "Nierozpoczęte" and lessons_completed_count > 0:
            continue
        
        filtered_categories.append(cat_id)
    
    if not filtered_categories:
        st.info(f"Brak umiejętności spełniających kryteria filtrowania w bloku '{block['name']}'")
        return
    
    # Określ liczbę kolumn w zależności od urządzenia
    if device_type == 'mobile':
        num_cols = 1
    elif device_type == 'tablet':
        num_cols = 2
    else:
        num_cols = 1
    
    # Utwórz siatkę dla kart umiejętności
    cols = st.columns(num_cols)
    
    # Wyświetl karty umiejętności
    for i, cat_id in enumerate(filtered_categories):
        category = categories[cat_id]
        with cols[i % num_cols]:
            display_skill_card(category, user_completed_lessons, user_skills, users_data, user_data, card_index=i)


def display_skill_card(category, user_completed_lessons, user_skills, users_data, user_data, card_index=0):
    """Wyświetla kartę umiejętności w nowym stylu"""
    
    # Oblicz poziom na podstawie ukończonych lekcji
    category_lessons_ids = [lesson["id"] for lesson in category['lessons']]
    completed_category_lessons = [lesson_id for lesson_id in user_completed_lessons if lesson_id in category_lessons_ids]
    lessons_completed_count = len(completed_category_lessons)
    
    # Poziom = liczba ukończonych lekcji (max 10)
    calculated_level = min(lessons_completed_count, 10)
    
    # Aktualizuj poziom w danych użytkownika jeśli się zmienił
    if calculated_level != category['level']:
        if category['id'] not in user_skills:
            user_skills[category['id']] = {'level': 0}
        
        user_skills[category['id']]['level'] = calculated_level
        user_data['skills'] = user_skills
        users_data[st.session_state.username] = user_data
        save_user_data(users_data)
    
    # Wyświetl kartę umiejętności w nowoczesnym stylu
    progress = int((calculated_level / category['max_level']) * 100)
    card_status = "max-level" if calculated_level == category['max_level'] else "in-progress" if calculated_level > 0 else "not-started"
    
    # Unikalny identyfikator karty
    card_id = f"skill-card-{category['id']}"
    
    # Dodaj obsługę menu kontekstowego
    context_menu_html = f"""
    <div id="context-menu-{card_id}" class="context-menu" style="display: none;">
        <div class="context-menu-item" onclick="showLessons('{category['id']}')">
            <span class="context-menu-item-icon">📚</span>
            <span>Pokaż lekcje</span>
        </div>
        <div class="context-menu-divider"></div>
        <div class="context-menu-item" onclick="hideMenu()">
            <span class="context-menu-item-icon">❌</span>
            <span>Zamknij</span>
        </div>
    </div>
    """
    
    st.markdown(f"""
    <div id="{card_id}" class="skill-card {card_status}" style="--card-index: {card_index};" 
         oncontextmenu="showContextMenu(event, '{card_id}'); return false;">
        <div class="skill-card-icon">{category['icon']}</div>
        <h4>{category['name']}</h4>
        <div class="level-indicator">Poziom {calculated_level}/{category['max_level']}</div>
        <div class="skill-progress-bar">
            <div class="skill-progress" style="width: {progress}%;"></div>
        </div>
        <p class="skill-description">{category['description']}</p>
        <p class="completed-lessons">Ukończone lekcje: {lessons_completed_count}/10</p>
    </div>
    {context_menu_html}
    
    <script>
    function showContextMenu(event, cardId) {{
        // Ukryj wszystkie inne menu
        document.querySelectorAll('.context-menu').forEach(menu => {{
            menu.style.display = 'none';
        }});
        
        // Pokaż menu dla tej karty
        const menu = document.getElementById('context-menu-' + cardId);
        menu.style.display = 'block';
        menu.style.left = event.pageX + 'px';
        menu.style.top = event.pageY + 'px';
        
        // Zamknij menu po kliknięciu poza nim
        document.addEventListener('click', function closeMenu(e) {{
            if (!menu.contains(e.target)) {{
                menu.style.display = 'none';
                document.removeEventListener('click', closeMenu);
            }}
        }});
    }}
    
    function hideMenu() {{
        document.querySelectorAll('.context-menu').forEach(menu => {{
            menu.style.display = 'none';
        }});
    }}
      function showLessons(categoryId) {{
        // Znajdź i kliknij odpowiedni przycisk
        document.querySelector(`button[key="btn_show_lessons_${{categoryId}}"]`).click();
    }}
    </script>
    """, unsafe_allow_html=True)
    
    # Przyciski akcji - ZMODYFIKOWANE, BEZ "UKOŃCZ WSZYSTKIE"
    col1, col2 = st.columns(2)  # Zmienione z 3 na 2 kolumny
    
    with col1:
        # Przycisk do pokazania lekcji
        if st.button(f"Pokaż lekcje", key=f"btn_show_lessons_{category['id']}"):
            lessons_state_key = f"show_lessons_{category['id']}"
            st.session_state[lessons_state_key] = not st.session_state.get(lessons_state_key, False)
            # Ukryj analitykę, jeśli była otwarta
            analytics_state_key = f"show_analytics_{category['id']}"
            if st.session_state.get(analytics_state_key, False):
                st.session_state[analytics_state_key] = False
    
    with col2:
        # Przycisk do pokazania analityki
        if st.button(f"Analityka", key=f"btn_show_analytics_{category['id']}"):
            analytics_state_key = f"show_analytics_{category['id']}"
            st.session_state[analytics_state_key] = not st.session_state.get(analytics_state_key, False)
            # Ukryj lekcje, jeśli były otwarte
            lessons_state_key = f"show_lessons_{category['id']}"
            if st.session_state.get(lessons_state_key, False):
                st.session_state[lessons_state_key] = False
    
    # Usunięto przycisk "Ukończ wszystkie" i trzecią kolumnę
    
    # Wyświetl lekcje jeśli przycisk został naciśnięty
    lessons_state_key = f"show_lessons_{category['id']}"
    if st.session_state.get(lessons_state_key, False):
        display_category_lessons(category, calculated_level, user_completed_lessons)
    
    # Wyświetl analitykę jeśli przycisk został naciśnięty
    analytics_state_key = f"show_analytics_{category['id']}"
    if st.session_state.get(analytics_state_key, False):
        show_skill_analytics(category, user_completed_lessons)


def display_category_lessons(category, current_level, completed_lessons):
    """Wyświetla lekcje dla danej kategorii z oznaczeniem dostępności"""
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    # Pobierz listę dostępnych lekcji
    available_lessons_data = get_available_lessons()
    
    # Utwórz listę ID dostępnych lekcji dla łatwiejszego porównywania
    available_lessons_ids = []
    for lesson in available_lessons_data:
        if isinstance(lesson, dict):
            available_lessons_ids.append(lesson['id'])
        else:
            available_lessons_ids.append(lesson)
    
    st.markdown("<div class='lessons-container'>", unsafe_allow_html=True)
    
    # Dodaj obsługę nawigacji za pomocą klawiatury
    st.markdown("""
    <div class="keyboard-nav-info">
        <span>💡 Wskazówka: Użyj klawiszy strzałek ↑↓ do nawigacji między lekcjami, Enter aby rozpocząć wybraną lekcję</span>
    </div>
    """, unsafe_allow_html=True)
    
    for i, lesson in enumerate(category['lessons']):
        lesson_id = lesson['id']
        lesson_completed = lesson_id in completed_lessons
        lesson_available = lesson_id in available_lessons_ids
        
        # Generuj unikalny klucz dla przycisku
        button_key = f"lesson_{lesson_id}_{random.randint(1000,9999)}"
        
        # Dostosuj wygląd lekcji w zależności od urządzenia
        if device_type == 'mobile':
            # Na telefonach używamy prostszego układu
            lesson_status_icon = ""
            if lesson_completed:
                lesson_status_icon = "✅"
            elif not lesson_available:
                lesson_status_icon = "🔒"
            else:
                lesson_status_icon = "⬜"
                
            lesson_status_class = "completed" if lesson_completed else ("unavailable" if not lesson_available else "available")
            
            st.markdown(f"""
            <div class="lesson-item {lesson_status_class}" tabindex="0" role="button" 
                 aria-label="Lekcja {i+1}: {lesson['title']}, 
                 {('ukończona' if lesson_completed else ('niedostępna' if not lesson_available else 'dostępna'))}">
                <span class="lesson-title">{lesson['title']}</span>
                <span class="lesson-status">{lesson_status_icon}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Bezpośredni przycisk do rozpoczęcia lekcji tylko dla dostępnych lekcji
            if not lesson_completed and lesson_available:
                if st.button("▶️", key=f"start_{button_key}", help="Rozpocznij lekcję"):
                    st.session_state.current_lesson = lesson_id
                    st.session_state.current_lesson_category = category['id']
                    st.session_state.page = 'lesson'
                    st.rerun()
            elif not lesson_available:
                st.button("🔒", key=f"locked_{button_key}", help="Lekcja niedostępna", disabled=True)
        else:
            # Na tabletach i desktopach używamy bardziej rozbudowanego układu
            col1, col2 = st.columns([5,1])
            
            with col1:
                lesson_status_class = "completed" if lesson_completed else ("unavailable" if not lesson_available else "available")
                
                st.markdown(f"""
                <div class="lesson-item {lesson_status_class}" tabindex="0" role="button" 
                     aria-label="Lekcja {i+1}: {lesson['title']}, 
                     {('ukończona' if lesson_completed else ('niedostępna' if not lesson_available else 'dostępna'))}">
                    <span class="lesson-title">{lesson['title']}</span>
                    {'' if lesson_available else '<span class="lesson-locked-icon">🔒</span>'}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Przycisk do oznaczania lekcji jako ukończonej lub rozpoczęcia lekcji
                if lesson_completed:
                    if st.button("✅", key=f"mark_{button_key}", help="Oznacz jako nieukończoną"):
                        # Usuń lekcję z ukończonych
                        users_data = load_user_data()
                        user_data = users_data.get(st.session_state.username, {})
                        user_completed = set(user_data.get("completed_lessons", []))
                        user_completed.discard(lesson_id)
                        user_data["completed_lessons"] = list(user_completed)
                        users_data[st.session_state.username] = user_data
                        save_user_data(users_data)
                        st.rerun()
                elif lesson_available:
                    if st.button("▶️", key=f"mark_{button_key}", help="Rozpocznij lekcję"):
                        # Przejdź do lekcji
                        st.session_state.current_lesson = lesson_id
                        st.session_state.current_lesson_category = category['id']
                        st.session_state.page = 'lesson'
                        st.rerun()
                else:
                    # Lekcja niedostępna - wyświetl zablokowany przycisk
                    st.button("🔒", key=f"locked_{button_key}", help="Lekcja niedostępna", disabled=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def add_custom_css():
    """Dodaje niestandardowe style CSS dla nowego wyglądu zakładki Umiejętności"""
    
    st.markdown("""
    <style>
    /* Nowy nagłówek strony */
    .skills-header {
        text-align: center;
        font-size: 2.5rem;
        background: linear-gradient(90deg, #6DD5FA, #2980B9);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    /* Dashboard postępu */
    .progress-dashboard {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin-bottom: 30px;
    }
    
    .stat-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(240,240,250,0.9));
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .stat-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    
    .stat-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2980B9;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #555;
    }
    
    /* Nagłówki bloków umiejętności */
    .section-header {
        margin: 30px 0 15px 0;
        font-size: 1.5rem;
        color: #333;
        border-bottom: 2px solid #eee;
        padding-bottom: 10px;
    }
    
    .skill-block-header {
        background: linear-gradient(135deg, #6DD5FA, #2980B9);
        border-radius: 15px;
        padding: 20px;
        margin: 30px 0 20px 0;
        color: white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .skill-block-header:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .skill-block-header h2 {
        margin: 0 0 10px 0;
        font-size: 1.8rem;
    }
    
    .skill-block-header p {
        margin: 0;
        opacity: 0.9;
        font-size: 1rem;
    }
    
    /* Karty umiejętności */
    .skill-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(245,245,255,0.9));
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        border-left: 4px solid #ccc;
    }
    
    .skill-card.not-started {
        border-left-color: #ccc;
    }
    
    .skill-card.in-progress {
        border-left-color: #3498db;
    }
    
    .skill-card.max-level {
        border-left-color: #27ae60;
    }
    
    .skill-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .skill-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, transparent, rgba(100,180,255,0.3), transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .skill-card:hover::before {
        opacity: 1;
    }
    
    .skill-card-icon {
        font-size: 2rem;
        margin-bottom: 10px;
        display: inline-block;
    }
    
    .skill-card h4 {
        margin: 0 0 10px 0;
        color: #333;
        font-size: 1.3rem;
    }
    
    .skill-description {
        color: #555;
        margin-bottom: 15px;
        font-size: 0.9rem;
    }
    
    .level-indicator {
        font-size: 0.9rem;
        color: #555;
        margin-bottom: 8px;
    }
    
    .skill-progress-bar {
        height: 8px;
        background: rgba(200,200,220,0.3);
        border-radius: 4px;
        margin: 10px 0;
        overflow: hidden;
    }
    
    .skill-progress {
        height: 100%;
        background: linear-gradient(90deg, #3498db, #2ecc71);
        border-radius: 4px;
        transition: width 0.8s ease;
    }
    
    .completed-lessons {
        margin-top: 15px;
        font-size: 0.85rem;
        color: #555;
    }
    
    .skill-card.max-level .completed-lessons {
        color: #27ae60;
        font-weight: bold;
    }
    
    /* Lekcje */
    .lessons-container {
        background: rgba(245,245,255,0.7);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0 20px 0;
        border-left: 3px solid #3498db;
    }
    
    .lesson-item {
        padding: 10px 15px;
        margin: 8px 0;
        border-radius: 8px;
        background: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.2s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        cursor: pointer;
    }
    
    .lesson-item:hover {
        transform: translateX(5px);
        box-shadow: 0 3px 8px rgba(0,0,0,0.1);
    }
    
    .lesson-item:focus {
        outline: 2px solid #3498db;
        box-shadow: 0 0 0 4px rgba(52, 152, 219, 0.3);
        transform: translateX(5px);
    }
    
    .lesson-item.completed {
        border-left: 3px solid #27ae60;
    }
    
    .lesson-item.available {
        border-left: 3px solid #3498db;
    }
    
    .lesson-item.unavailable {
        border-left: 3px solid #bbb;
        opacity: 0.7;
        background-color: #f5f5f5;
        cursor: not-allowed;
    }
    
    .lesson-item.unavailable:hover {
        transform: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .lesson-title {
        font-weight: 500;
        color: #333;
    }
    
    .lesson-status {
        font-size: 18px;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(135deg, rgba(100, 180, 255, 0.1) 0%, rgba(70, 150, 220, 0.2) 100%);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 30px;
        border: 1px solid rgba(70, 150, 220, 0.2);
        box-shadow: 0 3px 10px rgba(0,0,0,0.03);
    }
    
    .info-box h4 {
        margin-top: 0;
        color: #2980B9;
        font-size: 1.2rem;
    }
    
    /* Menu kontekstowe */
    .context-menu {
        position: absolute;
        background: white;
        border-radius: 8px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        padding: 10px 0;
        z-index: 1000;
        min-width: 200px;
        animation: fadeIn 0.2s ease;
    }
    
    .context-menu-item {
        padding: 8px 15px;
        cursor: pointer;
        transition: all 0.2s;
        display: flex;
        align-items: center;
    }
    
    .context-menu-item:hover {
        background: rgba(52, 152, 219, 0.1);
    }
    
    .context-menu-item-icon {
        margin-right: 10px;
        font-size: 16px;
        width: 20px;
        text-align: center;
    }
    
    .context-menu-divider {
        height: 1px;
        background: #eee;
        margin: 5px 0;
    }
    
    /* Wskazówki nawigacji klawiaturą */
    .keyboard-nav-info {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 15px;
        padding: 8px 12px;
        background-color: rgba(52, 152, 219, 0.1);
        border-radius: 6px;
        border-left: 3px solid #3498db;
    }
    
    /* Animacje przejść */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .skill-card {
        animation: fadeIn 0.5s ease forwards;
        opacity: 0;
        animation-delay: calc(var(--card-index, 0) * 0.1s);
    }
    
    /* Responsywność */
    @media (max-width: 768px) {
        .skills-header {
            font-size: 1.8rem;
            padding: 15px;
        }
        
        .stat-icon {
            font-size: 1.5rem;
        }
        
        .stat-value {
            font-size: 1.4rem;
        }
        
        .skill-block-header h2 {
            font-size: 1.5rem;
        }
        
        .skill-card h4 {
            font-size: 1.2rem;
        }
        
        .keyboard-nav-info {
            display: none; /* Ukryj na telefonach */
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Dodaj skrypt JavaScript dla obsługi nawigacji klawiaturą
    st.markdown("""
    <script>
    document.addEventListener('DOMContentLoaded', () => {
        const lessonItems = document.querySelectorAll('.lesson-item');
        let currentFocus = -1;
        
        // Dodaj opóźnione animacje dla kart umiejętności
        document.querySelectorAll('.skill-card').forEach((card, index) => {
            card.style.setProperty('--card-index', index);
        });
        
        // Obsługa nawigacji klawiaturą
        document.addEventListener('keydown', (e) => {
            // Strzałka w dół
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                if (currentFocus < lessonItems.length - 1) {
                    currentFocus++;
                    lessonItems[currentFocus].focus();
                }
            }
            // Strzałka w górę
            else if (e.key === 'ArrowUp') {
                e.preventDefault();
                if (currentFocus > 0) {
                    currentFocus--;
                    lessonItems[currentFocus].focus();
                }
            }
            // Enter - symuluj kliknięcie
            else if (e.key === 'Enter' && currentFocus >= 0) {
                e.preventDefault();
                lessonItems[currentFocus].click();
            }
        });
        
        // Kliknięcie w lekcję
        lessonItems.forEach((item, index) => {
            item.addEventListener('focus', () => {
                currentFocus = index;
            });
            
            item.addEventListener('click', () => {
                // Znajdź przycisk rozpoczęcia dla tego elementu i kliknij go
                const buttons = document.querySelectorAll(`button[kind="secondary"]`);
                buttons.forEach(button => {
                    if (button.textContent.includes('Rozpocznij lekcję') || 
                        button.textContent.includes('▶️')) {
                        button.click();
                    }
                });
            });
        });
    });
    </script>
    """, unsafe_allow_html=True)


def get_lessons_for_category(category_id):
    """Generuje listę lekcji dla danej kategorii na podstawie danych kursu dla Neuroliderów"""
    
    # Dane lekcji dla poszczególnych kategorii - ZAKTUALIZOWANE dla Neuroliderów
    lessons_data = {
        1: [  # Wprowadzenie do neuroprzywództwa
            {"id": "B1C1L1", "title": "Co to jest neuroprzywództwo?"},
            {"id": "B1C1L2", "title": "Mózg lidera – struktura i funkcje"},
            {"id": "B1C1L3", "title": "Neuronaukowe podstawy podejmowania decyzji"},
            {"id": "B1C1L4", "title": "Jak mózg przetwarza stres i zmienność?"},
            {"id": "B1C1L5", "title": "Neurobiologia emocji a zarządzanie"},
            {"id": "B1C1L6", "title": "Rola oksytocyny w przywództwie"},
            {"id": "B1C1L7", "title": "Dopamina – motywacja i nagroda"},
            {"id": "B1C1L8", "title": "Neuroprzywództwo a zarządzanie stresem"},
            {"id": "B1C1L9", "title": "Przewodzenie w kontekście teorii neurobiologicznych"},
            {"id": "B1C1L10", "title": "Neuroprzywództwo w praktyce – przykłady z życia"}
        ],
        2: [  # Mózg, emocje i decyzje
            {"id": "B1C2L1", "title": "Jak emocje wpływają na decyzje liderów?"},
            {"id": "B1C2L2", "title": "Rola limbicznego układu w podejmowaniu decyzji"},
            {"id": "B1C2L3", "title": "Przeciwdziałanie błędom poznawczym"},
            {"id": "B1C2L4", "title": "Jak zrozumieć emocje w pracy zespołowej?"},
            {"id": "B1C2L5", "title": "Mechanizmy adaptacji do stresu"},
            {"id": "B1C2L6", "title": "Inteligencja emocjonalna lidera"},
            {"id": "B1C2L7", "title": "Decyzje pod wpływem emocji a efektywność"},
            {"id": "B1C2L8", "title": "Mózg a odporność na krytykę"},
            {"id": "B1C2L9", "title": "Przykłady z życia liderów: jak radzili sobie z emocjami"},
            {"id": "B1C2L10", "title": "Neurobiologia współczucia w przywództwie"}
        ],
        3: [  # Mechanizmy mózgu w interakcjach społecznych
            {"id": "B1C3L1", "title": "Współczucie jako narzędzie przywódcze"},
            {"id": "B1C3L2", "title": "Jak mózg interpretuje zachowanie innych?"},
            {"id": "B1C3L3", "title": "Neurologiczne podstawy komunikacji"},
            {"id": "B1C3L4", "title": "Zarządzanie konfliktem – mózg i emocje"},
            {"id": "B1C3L5", "title": "Teoria przywództwa opartego na empatii"},
            {"id": "B1C3L6", "title": "Mózg gadzi vs. racjonalny: jak to wpływa na decyzje?"},
            {"id": "B1C3L7", "title": "Jak skutecznie motywować zespół?"},
            {"id": "B1C3L8", "title": "Mechanizmy wpływu i perswazji"},
            {"id": "B1C3L9", "title": "Neuroprzywództwo a budowanie relacji"},
            {"id": "B1C3L10", "title": "Mózg a dynamika grupy"}
        ],        4: [  # Modele podejmowania decyzji
            {"id": "B2C4L1", "title": "Wprowadzenie do modeli decyzyjnych"},
            {"id": "B2C4L2", "title": "Teoria perspektywy i jej zastosowanie w decyzjach"},
            {"id": "B2C4L3", "title": "Proces podejmowania decyzji w grupie"},
            {"id": "B2C4L4", "title": "Teoria wyboru a proces decyzyjny"},
            {"id": "B2C4L5", "title": "Zrozumienie heurystyk i błędów poznawczych"},
            {"id": "B2C4L6", "title": "Model SEEDS w neuroprzywództwie"},
            {"id": "B2C4L7", "title": "Analiza ryzyka i ocena potencjalnych konsekwencji"},
            {"id": "B2C4L8", "title": "Modele podejmowania decyzji w kontekście neurobiologicznym"},
            {"id": "B2C4L9", "title": "Jak rozwiązywać problemy z podejmowaniem decyzji?"},
            {"id": "B2C4L10", "title": "Zastosowanie sztucznej inteligencji w podejmowaniu decyzji"}
        ],        5: [  # Błędy poznawcze w decyzjach
            {"id": "B2C5L1", "title": "Rozpoznawanie błędów poznawczych"},
            {"id": "B2C5L2", "title": "Efekt potwierdzenia w pracy lidera"},
            {"id": "B2C5L3", "title": "Efekt pewności wstecznej i jego wpływ na zarządzanie"},
            {"id": "B2C5L4", "title": "Nadmierny optymizm – rozpoznanie i równoważenie"},
            {"id": "B2C5L5", "title": "Błąd dostępności w decyzjach kierowniczych"},
            {"id": "B2C5L6", "title": "Efekt zakotwiczenia w negocjacjach i planowaniu"},
            {"id": "B2C5L7", "title": "Błędy atrybucji w ocenie pracowników"},
            {"id": "B2C5L8", "title": "Przeciwdziałanie błędom poznawczym w zespole"},
            {"id": "B2C5L9", "title": "Strategie redukcji błędów poznawczych"},
            {"id": "B2C5L10", "title": "Systematyczne podejmowanie decyzji jako przeciwwaga dla błędów"}
        ],        6: [  # Neurologiczne aspekty zmiany i innowacji
            {"id": "B2C6L1", "title": "Neuroplastyczność i jej zastosowanie w przywództwie"},
            {"id": "B2C6L2", "title": "Jak mózg reaguje na zmiany organizacyjne"},
            {"id": "B2C6L3", "title": "Opór przed zmianą z perspektywy neurobiologicznej"},
            {"id": "B2C6L4", "title": "Wspieranie innowacyjności z uwzględnieniem funkcji mózgu"},
            {"id": "B2C6L5", "title": "Kreowanie środowiska wspierającego neuroplastyczność"},
            {"id": "B2C6L6", "title": "Neurobiologia kreatywności i innowacji"},
            {"id": "B2C6L7", "title": "Zarządzanie stresem związanym ze zmianą"},
            {"id": "B2C6L8", "title": "Tworzenie nawyków wspierających adaptację"},
            {"id": "B2C6L9", "title": "Wdrażanie zmian z uwzględnieniem reakcji mózgu"},
            {"id": "B2C6L10", "title": "Budowanie odporności zespołu na zmiany"}
        ],        7: [  # Motywowanie siebie i innych
            {"id": "B3C7L1", "title": "Neurobiologia motywacji"},
            {"id": "B3C7L2", "title": "Układ nagrody w mózgu i jego rola w motywacji"},
            {"id": "B3C7L3", "title": "Wewnętrzna vs zewnętrzna motywacja - podejście naukowe"},
            {"id": "B3C7L4", "title": "Jak budować zaangażowanie zespołu?"},
            {"id": "B3C7L5", "title": "Motywacja a hormony i neuroprzekaźniki"},
            {"id": "B3C7L6", "title": "Rozpoznawanie i wspieranie potrzeb motywacyjnych pracowników"},
            {"id": "B3C7L7", "title": "Techniki wzmacniania długoterminowej motywacji"},
            {"id": "B3C7L8", "title": "Poczucie sensu jako kluczowy czynnik motywacyjny"},
            {"id": "B3C7L9", "title": "Budowanie środowiska wspierającego motywację"},
            {"id": "B3C7L10", "title": "Neuronaukowe podejście do celów i ich realizacji"}
        ],        8: [  # Neurobiologia stresu w przywództwie
            {"id": "B3C8L1", "title": "Reakcja stresu w mózgu lidera"},
            {"id": "B3C8L2", "title": "Wpływ przewlekłego stresu na podejmowanie decyzji"},
            {"id": "B3C8L3", "title": "Techniki redukcji stresu oparte na neurobadaniach"},
            {"id": "B3C8L4", "title": "Rozpoznawanie objawów wypalenia zawodowego"},
            {"id": "B3C8L5", "title": "Regeneracja mózgu po stresie – praktyczne strategie"},
            {"id": "B3C8L6", "title": "Stres a funkcje poznawcze istotne w przywództwie"},
            {"id": "B3C8L7", "title": "Regulacja emocjonalna w sytuacjach wysokiego stresu"},
            {"id": "B3C8L8", "title": "Budowanie odporności psychicznej zespołu"},
            {"id": "B3C8L9", "title": "Zarządzanie stresem w sytuacjach kryzysowych"},
            {"id": "B3C8L10", "title": "Prewencja stresu i zdrowie psychiczne lidera"}
        ],        9: [  # Rola emocji w przywództwie
            {"id": "B3C9L1", "title": "Inteligencja emocjonalna a skuteczność przywódcza"},
            {"id": "B3C9L2", "title": "Neurobiologiczne podstawy empatii"},
            {"id": "B3C9L3", "title": "Rozpoznawanie i zarządzanie własnymi emocjami"},
            {"id": "B3C9L4", "title": "Emocje w procesie podejmowania decyzji"},
            {"id": "B3C9L5", "title": "Zarządzanie emocjami w sytuacjach konfliktowych"},
            {"id": "B3C9L6", "title": "Budowanie zaufania przez inteligencję emocjonalną"},
            {"id": "B3C9L7", "title": "Empatia jako kluczowa kompetencja lidera"},
            {"id": "B3C9L8", "title": "Emocjonalna odporność w trudnych sytuacjach"},
            {"id": "B3C9L9", "title": "Komunikacja emocjonalna w zespole"},
            {"id": "B3C9L10", "title": "Rozwój inteligencji emocjonalnej – praktyczne techniki"}
        ],        10: [  # Budowanie odporności lidera
            {"id": "B4C10L1", "title": "Neurobiologiczne podstawy odporności psychicznej"},
            {"id": "B4C10L2", "title": "Budowanie odporności poprzez świadome praktyki"},
            {"id": "B4C10L3", "title": "Radzenie sobie z niepewnością i zmiennością"},
            {"id": "B4C10L4", "title": "Techniki szybkiej regeneracji dla liderów"},
            {"id": "B4C10L5", "title": "Przekształcanie porażek w doświadczenia rozwojowe"},
            {"id": "B4C10L6", "title": "Akceptacja i praca z własnymi ograniczeniami"},
            {"id": "B4C10L7", "title": "Wzmacnianie elastyczności poznawczej"},
            {"id": "B4C10L8", "title": "Zarządzanie energią psychiczną i fizyczną"},
            {"id": "B4C10L9", "title": "Praca z przekonaniami ograniczającymi"},
            {"id": "B4C10L10", "title": "Budowanie długotrwałej stabilności psychicznej"}
        ],        11: [  # Efektywność przywódcza w praktyce
            {"id": "B4C11L1", "title": "Praktyczne zastosowanie neuroprzywództwa"},
            {"id": "B4C11L2", "title": "Skuteczne delegowanie z uwzględnieniem mocnych stron"},
            {"id": "B4C11L3", "title": "Budowanie kultury organizacyjnej wspierającej rozwój"},
            {"id": "B4C11L4", "title": "Facylitacja spotkań z wykorzystaniem neurotechnik"},
            {"id": "B4C11L5", "title": "Przekazywanie informacji zwrotnej wspierającej rozwój"},
            {"id": "B4C11L6", "title": "Efektywne zarządzanie czasem i priorytetami"},
            {"id": "B4C11L7", "title": "Zarządzanie projektami z perspektywy neuroprzywództwa"},
            {"id": "B4C11L8", "title": "Strategie osiągania długoterminowych celów"},
            {"id": "B4C11L9", "title": "Zarządzanie zespołami zdalnymi i hybrydowymi"},
            {"id": "B4C11L10", "title": "Budowanie współpracy międzydziałowej"}
        ],        12: [  # Neuroprzywództwo w kontekście globalnym
            {"id": "B4C12L1", "title": "Przywództwo w zespołach wielokulturowych"},
            {"id": "B4C12L2", "title": "Adaptacja stylów przywódczych do różnych kultur"},
            {"id": "B4C12L3", "title": "Komunikacja międzykulturowa w biznesie"},
            {"id": "B4C12L4", "title": "Neurobiologia uprzedzeń i stereotypów"},
            {"id": "B4C12L5", "title": "Budowanie zróżnicowanych zespołów (diversity & inclusion)"},
            {"id": "B4C12L6", "title": "Zarządzanie konfliktami w kontekście międzykulturowym"},
            {"id": "B4C12L7", "title": "Globalne trendy w przywództwie"},
            {"id": "B4C12L8", "title": "Adaptacja do dynamicznie zmieniającego się otoczenia"},
            {"id": "B4C12L9", "title": "Przywództwo w świecie VUCA i BANI"},
            {"id": "B4C12L10", "title": "Budowanie globalnych relacji biznesowych"}
        ],        13: [  # Wyzwania przyszłości
            {"id": "B5C13L1", "title": "Przyszłość neuroprzywództwa"},
            {"id": "B5C13L2", "title": "Przywództwo w erze sztucznej inteligencji"},
            {"id": "B5C13L3", "title": "Etyczne aspekty neurotechnologii w przywództwie"},
            {"id": "B5C13L4", "title": "Budowanie organizacji opartych na neuroprzywództwie"},
            {"id": "B5C13L5", "title": "Adaptacja do zmian technologicznych i ich wpływ na mózg"},
            {"id": "B5C13L6", "title": "Innowacje w neuronaukach i ich zastosowanie"},
            {"id": "B5C13L7", "title": "Trendy i kierunki rozwoju neuroprzywództwa"},
            {"id": "B5C13L8", "title": "Zrównoważone przywództwo w kontekście globalnych wyzwań"},
            {"id": "B5C13L9", "title": "Neuronauka a zrównoważony rozwój przedsiębiorstw"},
            {"id": "B5C13L10", "title": "Wizja przyszłości przywództwa opartego na wiedzy o mózgu"}
        ],        14: [  # Praca z umysłem lidera
            {"id": "B5C14L1", "title": "Świadome przywództwo i praca z umysłem"},
            {"id": "B5C14L2", "title": "Techniki mindfulness dla liderów"},
            {"id": "B5C14L3", "title": "Rozwijanie koncentracji i skupienia"},
            {"id": "B5C14L4", "title": "Zarządzanie sobą w warunkach wysokiej presji"},
            {"id": "B5C14L5", "title": "Neuroplastyczność w praktyce przywódczej"},
            {"id": "B5C14L6", "title": "Równowaga życiowa a efektywność poznawcza"},
            {"id": "B5C14L7", "title": "Techniki regeneracji mózgu dla liderów"},
            {"id": "B5C14L8", "title": "Rozwijanie kreatywności przez praktyki umysłowe"},
            {"id": "B5C14L9", "title": "Praca z wewnętrznym krytykiem w przywództwie"},
            {"id": "B5C14L10", "title": "Zarządzanie emocjami w sytuacjach wysokiego stresu"}
        ],        15: [  # Transformacja przywódcza
            {"id": "B5C15L1", "title": "Modele transformacji przywódczej"},
            {"id": "B5C15L2", "title": "Neurobiologiczne podstawy zmiany i rozwoju"},
            {"id": "B5C15L3", "title": "Przekształcanie organizacji poprzez neuroprzywództwo"},
            {"id": "B5C15L4", "title": "Budowanie wizji z wykorzystaniem wiedzy o mózgu"},
            {"id": "B5C15L5", "title": "Przywództwo służebne w kontekście neurobiologicznym"},
            {"id": "B5C15L6", "title": "Coaching oparty na neuronaukach"},
            {"id": "B5C15L7", "title": "Budowanie organizacji uczącej się"},
            {"id": "B5C15L8", "title": "Zarządzanie transformacją w kontekście funkcji mózgu"},
            {"id": "B5C15L9", "title": "Neuronaukowe podejście do zarządzania zmianą"},
            {"id": "B5C15L10", "title": "Przywództwo przyszłości – integracja wszystkich poziomów"}
        ]
    }
    
    return lessons_data.get(category_id, [])

def mark_all_lessons_as_completed(category, users_data, user_data):
    """Oznacza wszystkie lekcje w kategorii jako ukończone"""
    user_completed_lessons = set(user_data.get("completed_lessons", []))
    
    # Dodaj wszystkie lekcje z kategorii do ukończonych
    for lesson in category['lessons']:
        user_completed_lessons.add(lesson["id"])
    
    # Zapisz zaktualizowane dane
    user_data["completed_lessons"] = list(user_completed_lessons)
    users_data[st.session_state.username] = user_data
    save_user_data(users_data)
    
    # Wyświetl powiadomienie o sukcesie
    st.toast(f"Wszystkie lekcje w kategorii {category['name']} zostały oznaczone jako ukończone!", icon="✅")
    
    return user_completed_lessons

def show_skill_analytics(category, user_completed_lessons):
    """Wyświetla szczegółową analizę nauki dla wybranej umiejętności"""
    
    st.markdown(f"<h3 class='analytics-header'>Analityka nauki: {category['name']}</h3>", unsafe_allow_html=True)
    
    # Przygotuj dane o ukończonych lekcjach
    category_lessons_ids = [lesson["id"] for lesson in category['lessons']]
    completed_category_lessons = [lesson_id for lesson_id in user_completed_lessons if lesson_id in category_lessons_ids]
    lessons_completed_count = len(completed_category_lessons)
    progress_percent = (lessons_completed_count / 10) * 100
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Postęp nauki", f"{int(progress_percent)}%", delta=f"{lessons_completed_count}/10 lekcji")
    
    with col2:
        # Status nauki
        if lessons_completed_count == 0:
            status = "Nie rozpoczęto"
            status_color = "gray"
        elif lessons_completed_count < 5:
            status = "Początkujący"
            status_color = "orange"
        elif lessons_completed_count < 10:
            status = "Zaawansowany"
            status_color = "blue"
        else:
            status = "Ukończono"
            status_color = "green"
        
        st.markdown(f"""
        <div style="padding: 10px; border-radius: 8px; background-color: rgba(0,0,0,0.05); text-align: center;">
            <h4 style="margin:0; color: {status_color};">{status}</h4>
            <p style="margin:5px 0 0 0; font-size: 12px;">Status nauki</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Szacowany czas do ukończenia
        remaining_lessons = 10 - lessons_completed_count
        estimated_days = max(1, int(remaining_lessons / 2))  # Zakładając 2 lekcje dziennie
        
        st.markdown(f"""
        <div style="padding: 10px; border-radius: 8px; background-color: rgba(0,0,0,0.05); text-align: center;">
            <h4 style="margin:0;">{estimated_days} dni</h4>
            <p style="margin:5px 0 0 0; font-size: 12px;">Czas do ukończenia</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Wyświetl interaktywny wykres postępu nauki
    import pandas as pd
    import altair as alt
    
    # Utwórz dane do wykresu
    chart_data = []
    for i, lesson in enumerate(category['lessons']):
        lesson_status = "Ukończona" if lesson["id"] in user_completed_lessons else "Nieukończona"
        order = i + 1
        chart_data.append({
            "Numer lekcji": order,
            "Status": lesson_status,
            "Tytuł": lesson["title"]
        })
    
    if chart_data:
        df = pd.DataFrame(chart_data)
        
        # Stwórz wykres
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('Numer lekcji:O', sort=None),
            y=alt.Y('count():Q', title="Status"),
            color=alt.Color('Status:N', scale=alt.Scale(
                domain=['Ukończona', 'Nieukończona'],
                range=['#27ae60', '#e0e0e0']
            )),
            tooltip=['Numer lekcji', 'Tytuł', 'Status']
        ).properties(
            width='container',
            height=200,
            title="Postęp lekcji"
        )
        
        st.altair_chart(chart, use_container_width=True)
    
    # Rekomendacje dalszej nauki
    st.markdown("### Rekomendacje dalszej nauki")
    
    if lessons_completed_count < 10:        # Znajdź pierwszą nieukończoną lekcję
        next_lesson = None
        for lesson in category['lessons']:
            if lesson["id"] not in user_completed_lessons:
                next_lesson = lesson
                break
        
        if next_lesson:
            # Naprawiamy problematyczny skrypt JavaScript            
            st.markdown(f"""
            <div class="next-lesson-recommendation">
                <h4>Następna rekomendowana lekcja:</h4>
                <div class="recommended-lesson-item">
                    <span class="recommended-lesson-icon">📝</span>
                    <span class="recommended-lesson-title">{next_lesson['title']}</span>
                </div>
                <button id="start-recommended-lesson" class="start-recommended-button">Rozpocznij naukę</button>
            </div>
            
            <script>
                document.getElementById('start-recommended-lesson').addEventListener('click', function() {{
                    /* Symuluj kliknięcie w odpowiedni przycisk rozpoczęcia lekcji */
                    const buttons = document.querySelectorAll('button[kind="secondary"]');
                    for (let button of buttons) {{
                        if (button.textContent.includes('▶️')) {{
                            button.click();
                            break;
                        }}
                    }}
                }});
            </script>
            """, unsafe_allow_html=True)
    else:
        st.success("Gratulacje! Ukończyłeś wszystkie lekcje w tej kategorii. Spróbuj sprawdzić inne powiązane kategorie.")
    
    # Dodaj style CSS dla tego komponentu
    st.markdown("""
    <style>
    .analytics-header {
        color: #2980B9;
        border-bottom: 2px solid #eee;
        padding-bottom: 10px;
        margin-top: 30px;
    }
    
    .next-lesson-recommendation {
        background: linear-gradient(135deg, rgba(100, 180, 255, 0.1) 0%, rgba(70, 150, 220, 0.2) 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid rgba(70, 150, 220, 0.2);
    }
    
    .recommended-lesson-item {
        display: flex;
        align-items: center;
        background: white;
        padding: 12px;
        border-radius: 8px;
        margin: 10px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .recommended-lesson-icon {
        font-size: 24px;
        margin-right: 15px;
    }
    
    .recommended-lesson-title {
        font-weight: 500;
    }
    
    .start-recommended-button {
        background: #2980B9;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 20px;
        margin-top: 10px;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.3s;
    }
    
    .start-recommended-button:hover {
        background: #3498db;
        transform: translateY(-2px);
        box-shadow: 0 5px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    return

def get_available_lessons():
    """Odczytuje dostępne lekcje z plików i przyporządkowuje je do odpowiednich bloków i kategorii"""
    import os
    import json
    
    # Ścieżka do folderu z lekcjami
    lessons_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "lessons")
    
    # Sprawdź, czy folder istnieje
    if not os.path.exists(lessons_dir):
        st.warning(f"Folder lekcji nie istnieje: {lessons_dir}")
        return []
    
    # Lista dostępnych lekcji
    available_lessons = []
    
    # Przeszukaj folder lessons
    for file_name in os.listdir(lessons_dir):
        # Każdy plik z .json to lekcja
        if file_name.endswith('.json'):
            try:
                # Pełna ścieżka do pliku
                file_path = os.path.join(lessons_dir, file_name)
                
                # Odczytaj zawartość pliku JSON
                with open(file_path, 'r', encoding='utf-8') as file:
                    lesson_data = json.load(file)
                
                # Pobierz ID lekcji z pliku
                lesson_id = lesson_data.get('id', '')
                
                # Sprawdź, czy ID jest zgodne z formatem "BxCyLz" (np. B1C1L1)
                if lesson_id and lesson_id.startswith('B') and 'C' in lesson_id and 'L' in lesson_id:
                    # Wyodrębnij numery bloku, kategorii i lekcji z ID
                    block_num, rest = lesson_id.split('B')[1].split('C')
                    category_num, lesson_num = rest.split('L')
                    
                    # Konwersja na liczby całkowite
                    try:
                        block_num = int(block_num)
                        category_num = int(category_num)
                        lesson_num = int(lesson_num)
                        
                        # Dodaj informacje do listy dostępnych lekcji
                        available_lessons.append({
                            'id': lesson_id,
                            'title': lesson_data.get('title', 'Brak tytułu'),
                            'block': block_num,
                            'category': category_num,
                            'lesson_number': lesson_num,
                            'difficulty': lesson_data.get('difficulty', 'beginner'),
                            'file_path': file_path
                        })
                    except ValueError:
                        # Jeśli nie można przekonwertować na liczby całkowite, dodaj samą nazwę pliku
                        available_lessons.append(lesson_id)
                else:
                    # Jeśli ID nie pasuje do formatu, po prostu dodaj nazwę pliku bez rozszerzenia
                    lesson_id = os.path.splitext(file_name)[0]
                    available_lessons.append(lesson_id)
                    
            except (json.JSONDecodeError, IOError) as e:
                st.error(f"Błąd odczytu pliku {file_name}: {e}")
                # Dodaj samą nazwę pliku w przypadku błędu
                lesson_id = os.path.splitext(file_name)[0]
                available_lessons.append(lesson_id)
        
        # Obsługa plików Markdown, które mogą nie mieć struktury JSON
        elif file_name.endswith('.md'):
            lesson_id = os.path.splitext(file_name)[0]
            available_lessons.append(lesson_id)
    
    # Opcjonalnie - wyświetl debug info
    if st.session_state.get('dev_mode', False) and st.sidebar.checkbox("Debug lekcji", False):
        st.sidebar.write("Znalezione lekcje:")
        for lesson in available_lessons:
            if isinstance(lesson, dict):
                st.sidebar.write(f"- {lesson['id']}: Blok {lesson['block']}, Kategoria {lesson['category']}, Numer {lesson['lesson_number']}")
            else:
                st.sidebar.write(f"- {lesson} (tylko ID)")
    
    return available_lessons

# Dodajmy funkcję get_categories, której brakuje

def get_categories():
    """
    Zwraca słownik wszystkich kategorii umiejętności.
    
    Returns:
        dict: Słownik kategorii umiejętności
    """
    return {
        "neuroanatomy": {
            "name": "Neuroanatomia przywództwa",
            "icon": "🧠",
            "description": "Podstawy budowy i funkcji mózgu związane z przywództwem",
            "block": 1
        },
        "neurocognition": {
            "name": "Funkcje poznawcze lidera",
            "icon": "🔍",
            "description": "Procesy poznawcze istotne w przywództwie: uwaga, pamięć, podejmowanie decyzji",
            "block": 1
        },
        "neuroplasticity": {
            "name": "Neuroplastyczność w przywództwie",
            "icon": "🔄",
            "description": "Zdolność mózgu do adaptacji i zmiany w kontekście rozwoju umiejętności przywódczych",
            "block": 1
        },
        "decision_making": {
            "name": "Neurobiologia decyzji",
            "icon": "⚖️",
            "description": "Procesy neuronalne towarzyszące podejmowaniu decyzji liderskich",
            "block": 2
        },
        "risk_assessment": {
            "name": "Ocena ryzyka",
            "icon": "📊",
            "description": "Neuronalne podstawy szacowania i zarządzania ryzykiem",
            "block": 2
        },
        "emotional_intelligence": {
            "name": "Inteligencja emocjonalna",
            "icon": "❤️",
            "description": "Rozpoznawanie i zarządzanie emocjami w kontekście przywództwa",
            "block": 3
        },
        "motivation": {
            "name": "Systemy motywacyjne",
            "icon": "🚀",
            "description": "Neurobiologiczne podstawy motywacji i ich znaczenie w przywództwie",
            "block": 3
        },
        "stress_management": {
            "name": "Zarządzanie stresem",
            "icon": "🧘",
            "description": "Wpływ stresu na mózg i techniki zarządzania nim w roli lidera",
            "block": 3
        },
        "communication": {
            "name": "Neuronauka komunikacji",
            "icon": "💬",
            "description": "Neurobiologiczne podstawy efektywnej komunikacji liderskiej",
            "block": 4
        },
        "team_dynamics": {
            "name": "Dynamika zespołu",
            "icon": "👥",
            "description": "Neuronaukowe podejście do budowania i prowadzenia zespołów",
            "block": 4
        },
        "adaptability": {
            "name": "Adaptacyjność",
            "icon": "🦎",
            "description": "Neuroplastyczność i zdolność do adaptacji w zmieniającym się środowisku",
            "block": 4
        },
        "innovation": {
            "name": "Neurobiologia innowacji",
            "icon": "💡",
            "description": "Neuronalne podstawy kreatywności i innowacyjności w przywództwie",
            "block": 5
        },
        "future_leadership": {
            "name": "Przywództwo przyszłości",
            "icon": "🔮",
            "description": "Integracja neurotechnologii z rozwojem umiejętności przywódczych",
            "block": 5
        }
    }
