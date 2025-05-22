import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import json
import os
from datetime import datetime, timedelta
from data.users import load_user_data, save_user_data
from utils.components import zen_header, data_chart
from utils.material3_components import apply_material3_theme
from utils.card_layout import create_card, create_grid, zen_section, data_panel
from utils.layout import get_device_type

def show_admin_dashboard():
    """
    Wyświetla panel administracyjny z układem kart
    """
    # Zastosuj style Material 3
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    num_columns = 1 if device_type == "mobile" else 2
    
    # Sprawdź uprawnienia administratora
    users_data = load_user_data()
    user_data = users_data.get(st.session_state.username, {})
    
    if user_data.get('role') != 'admin':
        st.error("Brak uprawnień administratora!")
        return
    
    # Nagłówek strony
    zen_section("Panel Administracyjny", "Zarządzaj użytkownikami i monitoruj aktywność w aplikacji", "🛠️")
    
    # Inicjalizacja zakładek w sesji
    if 'admin_tab' not in st.session_state:
        st.session_state.admin_tab = 'overview'
    
    # Opcje zakładek
    tab_options = ['Przegląd', 'Użytkownicy', 'Statystyki', 'Konfiguracja']
    tab_ids = ['overview', 'users', 'stats', 'config']
    
    # Wyświetl przyciski zakładek
    tab_cols = st.columns(len(tab_options))
    for i, (tab_name, tab_id) in enumerate(zip(tab_options, tab_ids)):
        with tab_cols[i]:
            button_type = "primary" if st.session_state.admin_tab == tab_id else "secondary"
            if st.button(tab_name, key=f"tab_{tab_id}", type=button_type):
                st.session_state.admin_tab = tab_id
                st.rerun()
    
    # Wyświetl zawartość wybranej zakładki
    if st.session_state.admin_tab == 'overview':
        show_overview_tab(users_data, num_columns)
    elif st.session_state.admin_tab == 'users':
        show_users_tab(users_data, num_columns)
    elif st.session_state.admin_tab == 'stats':
        show_stats_tab(users_data, num_columns)
    elif st.session_state.admin_tab == 'config':
        show_config_tab(num_columns)

def show_overview_tab(users_data, num_columns):
    """
    Wyświetla zakładkę z przeglądem w układzie kart
    """
    # Oblicz podstawowe statystyki
    total_users = len(users_data)
    active_users = sum(1 for user in users_data.values() if user.get('last_login', '') != '')
    total_lessons_completed = sum(len(user.get('completed_lessons', [])) for user in users_data.values())
    avg_user_level = sum(user.get('level', 0) for user in users_data.values()) / total_users if total_users > 0 else 0
    
    # Nagłówek sekcji
    st.markdown("### Przegląd systemu")
    
    # Wyświetl karty z kluczowymi metrykami
    metric_cols = create_grid(num_columns)
    
    with metric_cols[0]:
        create_card(
            title="Liczba użytkowników",
            icon="👥",
            content=f"""
            <div style='padding: 20px 0; text-align: center;'>
                <h1 style='font-size: 3em; margin: 0;'>{total_users}</h1>
                <p style='color: #666;'>Zarejestrowanych użytkowników</p>
            </div>
            """,
            key="total_users_card"
        )
    
    with metric_cols[1 % num_columns]:
        create_card(
            title="Aktywni użytkownicy",
            icon="🔥",
            content=f"""
            <div style='padding: 20px 0; text-align: center;'>
                <h1 style='font-size: 3em; margin: 0;'>{active_users}</h1>
                <p style='color: #666;'>{round(active_users/total_users*100) if total_users > 0 else 0}% wszystkich użytkowników</p>
            </div>
            """,
            key="active_users_card"
        )
    
    with metric_cols[2 % num_columns]:
        create_card(
            title="Ukończone lekcje",
            icon="📚",
            content=f"""
            <div style='padding: 20px 0; text-align: center;'>
                <h1 style='font-size: 3em; margin: 0;'>{total_lessons_completed}</h1>
                <p style='color: #666;'>Średnio {round(total_lessons_completed/total_users) if total_users > 0 else 0} na użytkownika</p>
            </div>
            """,
            key="lessons_completed_card"
        )
    
    with metric_cols[3 % num_columns]:
        create_card(
            title="Średni poziom",
            icon="⭐",
            content=f"""
            <div style='padding: 20px 0; text-align: center;'>
                <h1 style='font-size: 3em; margin: 0;'>{round(avg_user_level, 1)}</h1>
                <p style='color: #666;'>Średni poziom użytkowników</p>
            </div>
            """,
            key="avg_level_card"
        )
    
    # Nagłówek sekcji wykresów
    st.markdown("### Analityka platformy")
    
    # Przygotuj dane dla wykresów
    chart_cols = create_grid(num_columns)
    
    # Wykres aktywności w czasie
    with chart_cols[0]:
        create_card(
            title="Aktywność użytkowników w czasie",
            icon="📊",
            content=f"""
            <div style='padding: 10px 0;'>
                <div id="activity_chart_placeholder" style='height: 300px; background-color: #f5f5f5; 
                     display: flex; align-items: center; justify-content: center;'>
                    Tutaj będzie wykres aktywności
                </div>
            </div>
            """,
            key="activity_chart_card"
        )
        
        # Dodaj prawdziwy wykres w Streamlit
        # Przykładowe dane
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
        activity = np.random.randint(5, 50, size=len(dates))
        activity_df = pd.DataFrame({'date': dates, 'active_users': activity})
        
        # Stwórz wykres Altair
        chart = alt.Chart(activity_df).mark_line(point=True).encode(
            x=alt.X('date:T', title='Data'),
            y=alt.Y('active_users:Q', title='Liczba aktywnych użytkowników'),
            tooltip=['date:T', 'active_users:Q']
        ).properties(
            height=300
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)
    
    # Wykres postępów użytkowników
    with chart_cols[1 % num_columns]:
        create_card(
            title="Postępy użytkowników",
            icon="📈",
            content=f"""
            <div style='padding: 10px 0;'>
                <div id="progress_chart_placeholder" style='height: 300px; background-color: #f5f5f5; 
                     display: flex; align-items: center; justify-content: center;'>
                    Tutaj będzie wykres postępów
                </div>
            </div>
            """,
            key="progress_chart_card"
        )
        
        # Dodaj prawdziwy wykres w Streamlit
        # Przykładowe dane
        progress_data = {
            'Poziom 1': len([u for u in users_data.values() if u.get('level', 0) == 1]),
            'Poziom 2': len([u for u in users_data.values() if u.get('level', 0) == 2]),
            'Poziom 3': len([u for u in users_data.values() if u.get('level', 0) == 3]),
            'Poziom 4': len([u for u in users_data.values() if u.get('level', 0) == 4]),
            'Poziom 5+': len([u for u in users_data.values() if u.get('level', 0) >= 5])
        }
        progress_df = pd.DataFrame(list(progress_data.items()), columns=['level', 'count'])
        
        # Stwórz wykres Altair
        chart = alt.Chart(progress_df).mark_bar().encode(
            x=alt.X('level:N', title='Poziom'),
            y=alt.Y('count:Q', title='Liczba użytkowników'),
            color=alt.Color('level:N', scale=alt.Scale(scheme='category10')),
            tooltip=['level:N', 'count:Q']
        ).properties(
            height=300
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)

def show_users_tab(users_data, num_columns):
    """
    Wyświetla zakładkę zarządzania użytkownikami w układzie kart
    """
    # Nagłówek sekcji
    st.markdown("### Zarządzanie użytkownikami")
    
    # Pole wyszukiwania
    search_query = st.text_input("Wyszukaj użytkownika", placeholder="Wpisz nazwę użytkownika")
    
    # Filtruj użytkowników
    filtered_users = {}
    if search_query:
        filtered_users = {username: data for username, data in users_data.items() 
                           if search_query.lower() in username.lower()}
    else:
        filtered_users = users_data
    
    # Stworz karty użytkowników
    if not filtered_users:
        st.info("Nie znaleziono użytkowników.")
    else:
        user_cols = create_grid(num_columns)
        
        for i, (username, user_data) in enumerate(filtered_users.items()):
            with user_cols[i % num_columns]:
                # Pobierz dane użytkownika
                level = user_data.get('level', 0)
                role = user_data.get('role', 'user')
                xp = user_data.get('xp', 0)
                coins = user_data.get('degen_coins', 0)
                completed_lessons = len(user_data.get('completed_lessons', []))
                last_login = user_data.get('last_login', 'Nigdy')
                
                # Wybierz ikonę na podstawie roli
                icon = "👑" if role == 'admin' else "👤"
                
                # Stwórz kartę użytkownika
                create_card(
                    title=username,
                    icon=icon,
                    content=f"""
                    <div style='padding: 10px 0;'>
                        <p><strong>Rola:</strong> {role}</p>
                        <p><strong>Poziom:</strong> {level}</p>
                        <p><strong>XP:</strong> {xp}</p>
                        <p><strong>DegenCoins:</strong> {coins}</p>
                        <p><strong>Ukończone lekcje:</strong> {completed_lessons}</p>
                        <p><strong>Ostatnie logowanie:</strong> {last_login}</p>
                        <div style='margin-top: 15px;'>
                            <button class='material-button' 
                                onclick="document.getElementById('btn-edit-{username}').click()">
                                Edytuj użytkownika
                            </button>
                            <button class='material-button secondary' 
                                onclick="document.getElementById('btn-reset-{username}').click()">
                                Resetuj hasło
                            </button>
                        </div>
                    </div>
                    """,
                    key=f"user_{username}_card"
                )
                
                # Ukryte przyciski do obsługi akcji
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Edytuj", key=f"btn-edit-{username}", help="", label_visibility="collapsed"):
                        st.session_state.edit_user = username
                        st.rerun()
                with col2:
                    if st.button("Resetuj", key=f"btn-reset-{username}", help="", label_visibility="collapsed"):
                        # Implementacja resetowania hasła
                        st.success(f"Hasło użytkownika {username} zostało zresetowane.")
    
    # Formularz edycji użytkownika
    if 'edit_user' in st.session_state:
        show_user_edit_form(st.session_state.edit_user, users_data)

def show_user_edit_form(username, users_data):
    """
    Wyświetla formularz edycji użytkownika
    """
    st.markdown("---")
    st.markdown(f"### Edycja użytkownika: {username}")
    
    user_data = users_data.get(username, {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_role = st.selectbox("Rola", options=['user', 'admin'], index=0 if user_data.get('role') != 'admin' else 1)
        new_level = st.number_input("Poziom", min_value=0, value=user_data.get('level', 0))
        new_xp = st.number_input("XP", min_value=0, value=user_data.get('xp', 0))
    
    with col2:
        new_coins = st.number_input("DegenCoins", min_value=0, value=user_data.get('degen_coins', 0))
        new_status = st.selectbox("Status konta", options=['active', 'suspended', 'banned'], 
                                 index=0 if user_data.get('status', 'active') == 'active' else 
                                       (1 if user_data.get('status') == 'suspended' else 2))
    
    save_col, cancel_col = st.columns(2)
    
    with save_col:
        if st.button("Zapisz zmiany"):
            # Aktualizuj dane użytkownika
            user_data['role'] = new_role
            user_data['level'] = new_level
            user_data['xp'] = new_xp
            user_data['degen_coins'] = new_coins
            user_data['status'] = new_status
            
            # Zapisz zmiany
            save_user_data(users_data)
            
            st.success(f"Dane użytkownika {username} zostały zaktualizowane.")
            del st.session_state.edit_user
            st.rerun()
    
    with cancel_col:
        if st.button("Anuluj"):
            del st.session_state.edit_user
            st.rerun()

def show_stats_tab(users_data, num_columns):
    """
    Wyświetla zakładkę ze statystykami w układzie kart
    """
    # Nagłówek sekcji
    st.markdown("### Statystyki platformy")
    
    # Przygotuj dane statystyczne
    stats_cols = create_grid(num_columns)
    
    # Statystyki dotyczące zaangażowania
    with stats_cols[0]:
        create_card(
            title="Zaangażowanie użytkowników",
            icon="📊",
            content=f"""
            <div style='padding: 10px 0;'>
                <div id="engagement_chart_placeholder" style='height: 300px; background-color: #f5f5f5; 
                     display: flex; align-items: center; justify-content: center;'>
                    Tutaj będzie wykres zaangażowania
                </div>
            </div>
            """,
            key="engagement_stats_card"
        )
        
        # Przykładowe dane dla wykresu
        engagement_data = {
            '0-5 lekcji': len([u for u in users_data.values() if len(u.get('completed_lessons', [])) < 5]),
            '5-10 lekcji': len([u for u in users_data.values() if 5 <= len(u.get('completed_lessons', [])) < 10]),
            '10-15 lekcji': len([u for u in users_data.values() if 10 <= len(u.get('completed_lessons', [])) < 15]),
            '15+ lekcji': len([u for u in users_data.values() if len(u.get('completed_lessons', [])) >= 15])
        }
        
        engagement_df = pd.DataFrame(list(engagement_data.items()), columns=['range', 'count'])
        
        # Stwórz wykres
        chart = alt.Chart(engagement_df).mark_bar().encode(
            x=alt.X('range:N', title='Liczba ukończonych lekcji'),
            y=alt.Y('count:Q', title='Liczba użytkowników'),
            color=alt.Color('range:N', scale=alt.Scale(scheme='blues')),
            tooltip=['range:N', 'count:Q']
        ).properties(
            height=300
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)
    
    # Statystyki dotyczące quizów
    with stats_cols[1 % num_columns]:
        create_card(
            title="Wyniki quizów",
            icon="❓",
            content=f"""
            <div style='padding: 10px 0;'>
                <div id="quiz_chart_placeholder" style='height: 300px; background-color: #f5f5f5; 
                     display: flex; align-items: center; justify-content: center;'>
                    Tutaj będzie wykres wyników quizów
                </div>
            </div>
            """,
            key="quiz_stats_card"
        )
        
        # Przykładowe dane dla wykresu
        np.random.seed(42)
        quiz_scores = np.random.normal(75, 15, 100)  # Średni wynik 75%, odchylenie standardowe 15%
        quiz_scores = np.clip(quiz_scores, 0, 100)   # Ogranicz wartości do zakresu 0-100%
        
        quiz_df = pd.DataFrame({
            'score': quiz_scores
        })
        
        # Stwórz histogram
        chart = alt.Chart(quiz_df).mark_bar().encode(
            x=alt.X('score:Q', bin=alt.Bin(step=10), title='Wynik (%)'),
            y=alt.Y('count()', title='Liczba quizów'),
            tooltip=['count()', alt.Tooltip('score:Q', bin=alt.Bin(step=10))]
        ).properties(
            height=300
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)
    
    # Nagłówek sekcji raportów
    st.markdown("### Generowanie raportów")
    
    # Karty raportów
    report_cols = create_grid(num_columns)
    
    with report_cols[0]:
        create_card(
            title="Raport aktywności",
            icon="📈",
            content=f"""
            <div style='padding: 10px 0;'>
                <p>Generuj raport aktywności użytkowników w wybranym okresie.</p>
                <div style='margin-top: 15px;'>
                    <button class='material-button' 
                        onclick="document.getElementById('btn-report-activity').click()">
                        Generuj raport
                    </button>
                </div>
            </div>
            """,
            key="activity_report_card"
        )
        
        # Ukryty przycisk
        if st.button("Generuj", key="btn-report-activity", help="", label_visibility="collapsed"):
            # Tutaj logika generowania raportu
            st.info("Generowanie raportu aktywności...")
            # Symulacja generowania raportu
            st.success("Raport aktywności został wygenerowany.")
    
    with report_cols[1 % num_columns]:
        create_card(
            title="Raport postępów",
            icon="🏆",
            content=f"""
            <div style='padding: 10px 0;'>
                <p>Generuj raport postępów użytkowników w nauce.</p>
                <div style='margin-top: 15px;'>
                    <button class='material-button' 
                        onclick="document.getElementById('btn-report-progress').click()">
                        Generuj raport
                    </button>
                </div>
            </div>
            """,
            key="progress_report_card"
        )
        
        # Ukryty przycisk
        if st.button("Generuj", key="btn-report-progress", help="", label_visibility="collapsed"):
            # Tutaj logika generowania raportu
            st.info("Generowanie raportu postępów...")
            # Symulacja generowania raportu
            st.success("Raport postępów został wygenerowany.")

def show_config_tab(num_columns):
    """
    Wyświetla zakładkę konfiguracji w układzie kart
    """
    # Nagłówek sekcji
    st.markdown("### Konfiguracja systemu")
    
    # Karty konfiguracji
    config_cols = create_grid(num_columns)
    
    with config_cols[0]:
        create_card(
            title="Ustawienia aplikacji",
            icon="⚙️",
            content=f"""
            <div style='padding: 10px 0;'>
                <p>Skonfiguruj podstawowe ustawienia aplikacji.</p>
                <div style='margin-top: 15px;'>
                    <button class='material-button' 
                        onclick="document.getElementById('btn-edit-app-settings').click()">
                        Edytuj ustawienia
                    </button>
                </div>
            </div>
            """,
            key="app_settings_card"
        )
        
        # Ukryty przycisk
        if st.button("Edytuj", key="btn-edit-app-settings", help="", label_visibility="collapsed"):
            st.session_state.edit_app_settings = True
            st.rerun()
    
    with config_cols[1 % num_columns]:
        create_card(
            title="Zarządzanie lekcjami",
            icon="📚",
            content=f"""
            <div style='padding: 10px 0;'>
                <p>Dodawaj, edytuj i usuwaj lekcje w systemie.</p>
                <div style='margin-top: 15px;'>
                    <button class='material-button' 
                        onclick="document.getElementById('btn-manage-lessons').click()">
                        Zarządzaj lekcjami
                    </button>
                </div>
            </div>
            """,
            key="lessons_management_card"
        )
        
        # Ukryty przycisk
        if st.button("Zarządzaj", key="btn-manage-lessons", help="", label_visibility="collapsed"):
            st.session_state.manage_lessons = True
            st.rerun()
    
    with config_cols[2 % num_columns]:
        create_card(
            title="Kopie zapasowe",
            icon="💾",
            content=f"""
            <div style='padding: 10px 0;'>
                <p>Zarządzaj kopiami zapasowymi danych.</p>
                <div style='margin-top: 15px;'>
                    <button class='material-button' 
                        onclick="document.getElementById('btn-create-backup').click()">
                        Utwórz kopię
                    </button>
                    <button class='material-button secondary' 
                        onclick="document.getElementById('btn-restore-backup').click()">
                        Przywróć
                    </button>
                </div>
            </div>
            """,
            key="backups_card"
        )
        
        # Ukryte przyciski
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Utwórz", key="btn-create-backup", help="", label_visibility="collapsed"):
                # Symulacja tworzenia kopii zapasowej
                st.info("Tworzenie kopii zapasowej...")
                st.success("Kopia zapasowa została utworzona pomyślnie.")
                
        with col2:
            if st.button("Przywróć", key="btn-restore-backup", help="", label_visibility="collapsed"):
                st.session_state.restore_backup = True
                st.rerun()
    
    with config_cols[3 % num_columns]:
        create_card(
            title="Logi systemowe",
            icon="📋",
            content=f"""
            <div style='padding: 10px 0;'>
                <p>Przeglądaj logi systemowe aplikacji.</p>
                <div style='margin-top: 15px;'>
                    <button class='material-button' 
                        onclick="document.getElementById('btn-view-logs').click()">
                        Przeglądaj logi
                    </button>
                </div>
            </div>
            """,
            key="logs_card"
        )
        
        # Ukryty przycisk
        if st.button("Przeglądaj", key="btn-view-logs", help="", label_visibility="collapsed"):
            # Symulacja wyświetlania logów
            st.info("Ładowanie logów systemu...")
            st.code("""
INFO  2023-11-12 08:15:23 - System started
INFO  2023-11-12 08:17:45 - User login: admin
INFO  2023-11-12 09:22:10 - New user registered: testuser1
WARNING 2023-11-12 10:05:32 - Failed login attempt: unknown_user
INFO  2023-11-12 11:30:45 - Backup created: backup_20231112.zip
INFO  2023-11-12 12:45:12 - User login: testuser1
INFO  2023-11-12 13:20:05 - Lesson completed: testuser1 - lesson_id: 5
INFO  2023-11-12 14:10:33 - User logout: testuser1
            """)
    
    # Formularze edycji ustawień
    if st.session_state.get('edit_app_settings', False):
        show_app_settings_form()
    
    if st.session_state.get('manage_lessons', False):
        show_lessons_management_form()
    
    if st.session_state.get('restore_backup', False):
        show_restore_backup_form()

def show_app_settings_form():
    """
    Wyświetla formularz edycji ustawień aplikacji
    """
    st.markdown("---")
    st.markdown("### Edycja ustawień aplikacji")
    
    col1, col2 = st.columns(2)
    
    with col1:
        app_name = st.text_input("Nazwa aplikacji", value="Neuroliderzy")
        primary_color = st.color_picker("Główny kolor", value="#4CAF50")
        xp_multiplier = st.number_input("Mnożnik XP", min_value=0.1, value=1.0, step=0.1)
    
    with col2:
        enable_shop = st.checkbox("Włącz sklep", value=True)
        maintenance_mode = st.checkbox("Tryb konserwacji", value=False)
        enable_achievements = st.checkbox("Włącz osiągnięcia", value=True)
    
    save_col, cancel_col = st.columns(2)
    
    with save_col:
        if st.button("Zapisz ustawienia"):
            # Tutaj logika zapisywania ustawień
            st.success("Ustawienia zostały zaktualizowane.")
            st.session_state.edit_app_settings = False
            st.rerun()
    
    with cancel_col:
        if st.button("Anuluj"):
            st.session_state.edit_app_settings = False
            st.rerun()

def show_lessons_management_form():
    """
    Wyświetla formularz zarządzania lekcjami
    """
    st.markdown("---")
    st.markdown("### Zarządzanie lekcjami")
    
    # Przykładowa lista lekcji
    lessons = [
        {"id": 1, "title": "Wprowadzenie do neuroprzywództwa", "module": "Neurobiologia przywództwa"},
        {"id": 2, "title": "Struktura mózgu lidera", "module": "Neurobiologia przywództwa"},
        {"id": 3, "title": "Inteligencja emocjonalna", "module": "Emocje i decyzje"},
        {"id": 4, "title": "Zarządzanie stresem", "module": "Psychologia przywództwa"},
        {"id": 5, "title": "Podejmowanie decyzji", "module": "Procesy decyzyjne"}
    ]
    
    # Wyświetl tabelę lekcji
    lessons_df = pd.DataFrame(lessons)
    st.dataframe(lessons_df, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Dodaj nową lekcję"):
            st.session_state.add_new_lesson = True
            st.rerun()
    
    with col2:
        lesson_to_edit = st.selectbox("Wybierz lekcję do edycji", 
                                     options=[f"{lesson['id']} - {lesson['title']}" for lesson in lessons])
        if st.button("Edytuj wybraną lekcję"):
            lesson_id = int(lesson_to_edit.split(" - ")[0])
            st.session_state.edit_lesson_id = lesson_id
            st.rerun()
    
    with col3:
        lesson_to_delete = st.selectbox("Wybierz lekcję do usunięcia", 
                                       options=[f"{lesson['id']} - {lesson['title']}" for lesson in lessons])
        if st.button("Usuń wybraną lekcję"):
            lesson_id = int(lesson_to_delete.split(" - ")[0])
            # Tutaj logika usuwania lekcji
            st.success(f"Lekcja ID: {lesson_id} została usunięta.")
    
    if st.button("Zamknij"):
        st.session_state.manage_lessons = False
        st.rerun()

def show_restore_backup_form():
    """
    Wyświetla formularz przywracania kopii zapasowej
    """
    st.markdown("---")
    st.markdown("### Przywracanie kopii zapasowej")
    
    # Przykładowa lista kopii zapasowych
    backups = [
        "backup_20231112.zip",
        "backup_20231105.zip",
        "backup_20231029.zip",
        "backup_20231022.zip"
    ]
    
    selected_backup = st.selectbox("Wybierz kopię zapasową do przywrócenia", options=backups)
    
    st.warning("Uwaga! Przywrócenie kopii zapasowej spowoduje utratę wszystkich danych wprowadzonych po jej utworzeniu.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Przywróć kopię"):
            # Tutaj logika przywracania kopii
            st.info(f"Przywracanie kopii {selected_backup}...")
            st.success(f"Kopia {selected_backup} została pomyślnie przywrócona.")
            st.session_state.restore_backup = False
            st.rerun()
    
    with col2:
        if st.button("Anuluj przywracanie"):
            st.session_state.restore_backup = False
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
    
    .material-button.secondary {
        background-color: #f0f0f0;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)
