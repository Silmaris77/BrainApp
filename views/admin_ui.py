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

# Import from new UI system
from utils.ui import initialize_ui, theme_selector
from utils.ui.components.cards import stat_card
from utils.ui.components.interactive import zen_button, notification
from utils.ui.components.text import content_section
from utils.ui.layouts.grid import render_dashboard_header, render_stats_section, responsive_grid

def show_admin_dashboard():
    """
    Wyświetla panel administracyjny używając nowego systemu UI zgodnego z CSP
    """
    # Inicjalizacja nowego UI
    initialize_ui()
    
    # Sprawdź uprawnienia administratora
    users_data = load_user_data()
    user_data = users_data.get(st.session_state.username, {})
    
    if user_data.get('role') != 'admin':
        notification("Brak uprawnień administratora!", "error")
        return
    
    # Nagłówek strony
    render_dashboard_header("Panel Administracyjny", "Zarządzaj użytkownikami i monitoruj aktywność w aplikacji")
    
    # Theme selector
    with st.sidebar:
        st.header("Ustawienia panelu")
        theme_selector()
    
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
            if zen_button(tab_name, key=f"tab_{tab_id}"):
                st.session_state.admin_tab = tab_id
                st.rerun()
    
    # Wyświetl zawartość wybranej zakładki
    if st.session_state.admin_tab == 'overview':
        show_overview_tab(users_data)
    elif st.session_state.admin_tab == 'users':
        show_users_tab(users_data)
    elif st.session_state.admin_tab == 'stats':
        show_stats_tab(users_data)
    elif st.session_state.admin_tab == 'config':
        show_config_tab()

def show_overview_tab(users_data):
    """
    Wyświetla zakładkę z przeglądem używającą nowego systemu UI
    """
    # Oblicz podstawowe statystyki
    total_users = len(users_data)
    active_users = sum(1 for user in users_data.values() if user.get('last_login', '') != '')
    total_lessons_completed = sum(len(user.get('completed_lessons', [])) for user in users_data.values())
    avg_user_level = sum(user.get('level', 0) for user in users_data.values()) / total_users if total_users > 0 else 0
    
    # Nagłówek sekcji
    st.markdown("### Przegląd systemu")
    
    # Statystyki w formie kart
    stats_data = [
        ("👥", str(total_users), "Liczba użytkowników"),
        ("🔥", str(active_users), "Aktywni użytkownicy"),
        ("📚", str(total_lessons_completed), "Ukończone lekcje"),
        ("⭐", str(round(avg_user_level, 1)), "Średni poziom")
    ]
    render_stats_section(stats_data)
    
    # Sekcja analityki
    st.markdown("### Analityka platformy")
    
    # Używamy responsywnej siatki
    chart_cols = responsive_grid(columns_desktop=2, columns_tablet=1, columns_mobile=1)
    
    # Wykres aktywności w czasie
    with chart_cols[0]:
        st.markdown("#### Aktywność użytkowników w czasie")
        
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
    with chart_cols[1]:
        st.markdown("#### Postępy użytkowników")
        
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

def show_users_tab(users_data):
    """
    Wyświetla zakładkę zarządzania użytkownikami używając nowego systemu UI
    """
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
    
    if not filtered_users:
        st.info("Nie znaleziono użytkowników.")
    else:
        # Używamy responsywnej siatki
        user_cols = responsive_grid(columns_desktop=3, columns_tablet=2, columns_mobile=1)
        
        for i, (username, user_data) in enumerate(filtered_users.items()):
            with user_cols[i % len(user_cols)]:
                # Pobierz dane użytkownika
                level = user_data.get('level', 0)
                role = user_data.get('role', 'user')
                xp = user_data.get('xp', 0)
                coins = user_data.get('degen_coins', 0)
                completed_lessons = len(user_data.get('completed_lessons', []))
                last_login = user_data.get('last_login', 'Nigdy')
                
                # Wybierz ikonę na podstawie roli
                icon = "👑" if role == 'admin' else "👤"
                
                # Karta użytkownika
                st.markdown(f"#### {icon} {username}")
                st.markdown(f"**Rola:** {role}")
                st.markdown(f"**Poziom:** {level}")
                st.markdown(f"**XP:** {xp}")
                st.markdown(f"**DegenCoins:** {coins}")
                st.markdown(f"**Ukończone lekcje:** {completed_lessons}")
                st.markdown(f"**Ostatnie logowanie:** {last_login}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if zen_button("Edytuj użytkownika", key=f"edit_{username}"):
                        st.session_state.edit_user = username
                        st.rerun()
                with col2:
                    if zen_button("Resetuj hasło", key=f"reset_{username}"):
                        # Implementacja resetowania hasła
                        notification(f"Hasło użytkownika {username} zostało zresetowane.", "success")
    
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
        if zen_button("Zapisz zmiany", key="save_user_changes"):
            # Aktualizuj dane użytkownika
            user_data['role'] = new_role
            user_data['level'] = new_level
            user_data['xp'] = new_xp
            user_data['degen_coins'] = new_coins
            user_data['status'] = new_status
            
            # Zapisz zmiany
            save_user_data(users_data)
            
            notification(f"Dane użytkownika {username} zostały zaktualizowane.", "success")
            del st.session_state.edit_user
            st.rerun()
    
    with cancel_col:
        if zen_button("Anuluj", key="cancel_user_edit"):
            del st.session_state.edit_user
            st.rerun()

def show_stats_tab(users_data):
    """
    Wyświetla zakładkę ze statystykami używając nowego systemu UI
    """
    st.markdown("### Statystyki platformy")
    
    # Statystyki
    stats_cols = responsive_grid(columns_desktop=2, columns_tablet=1, columns_mobile=1)
    
    # Zaangażowanie użytkowników
    with stats_cols[0]:
        st.markdown("#### Zaangażowanie użytkowników")
        
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
    
    # Wyniki quizów
    with stats_cols[1]:
        st.markdown("#### Wyniki quizów")
        
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
    
    # Generowanie raportów
    st.markdown("### Generowanie raportów")
    report_cols = responsive_grid(columns_desktop=2, columns_tablet=1, columns_mobile=1)
    
    with report_cols[0]:
        st.markdown("#### Raport aktywności")
        st.write("Generuj raport aktywności użytkowników w wybranym okresie.")
        if zen_button("Generuj raport", key="generate_activity_report"):
            # Symulacja generowania raportu
            with st.spinner("Generowanie raportu aktywności..."):
                # Symulujemy opóźnienie
                import time
                time.sleep(2)
                notification("Raport aktywności został wygenerowany.", "success")
    
    with report_cols[1]:
        st.markdown("#### Raport postępów")
        st.write("Generuj raport postępów użytkowników w nauce.")
        if zen_button("Generuj raport", key="generate_progress_report"):
            # Symulacja generowania raportu
            with st.spinner("Generowanie raportu postępów..."):
                # Symulujemy opóźnienie
                import time
                time.sleep(2)
                notification("Raport postępów został wygenerowany.", "success")

def show_config_tab():
    """
    Wyświetla zakładkę konfiguracji używając nowego systemu UI
    """
    st.markdown("### Konfiguracja systemu")
    
    # Karty konfiguracji
    config_cols = responsive_grid(columns_desktop=2, columns_tablet=1, columns_mobile=1)
    
    with config_cols[0]:
        st.markdown("#### Ustawienia aplikacji")
        st.write("Skonfiguruj podstawowe ustawienia aplikacji.")
        if zen_button("Edytuj ustawienia", key="edit_app_settings_btn"):
            st.session_state.edit_app_settings = True
            st.rerun()
    
    with config_cols[1]:
        st.markdown("#### Zarządzanie lekcjami")
        st.write("Dodawaj, edytuj i usuwaj lekcje w systemie.")
        if zen_button("Zarządzaj lekcjami", key="manage_lessons_btn"):
            st.session_state.manage_lessons = True
            st.rerun()
    
    with config_cols[0]:
        st.markdown("#### Kopie zapasowe")
        st.write("Zarządzaj kopiami zapasowymi danych.")
        col1, col2 = st.columns(2)
        with col1:
            if zen_button("Utwórz kopię", key="create_backup_btn"):
                # Symulacja tworzenia kopii zapasowej
                with st.spinner("Tworzenie kopii zapasowej..."):
                    import time
                    time.sleep(2)
                    notification("Kopia zapasowa została utworzona pomyślnie.", "success")
        with col2:
            if zen_button("Przywróć", key="restore_backup_btn"):
                st.session_state.restore_backup = True
                st.rerun()
    
    with config_cols[1]:
        st.markdown("#### Logi systemowe")
        st.write("Przeglądaj logi systemowe aplikacji.")
        if zen_button("Przeglądaj logi", key="view_logs_btn"):
            # Symulacja wyświetlania logów
            with st.spinner("Ładowanie logów systemu..."):
                import time
                time.sleep(1)
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
    
    # Formularze edycji
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
        if zen_button("Zapisz ustawienia", key="save_app_settings"):
            # Tutaj logika zapisywania ustawień
            notification("Ustawienia zostały zaktualizowane.", "success")
            st.session_state.edit_app_settings = False
            st.rerun()
    
    with cancel_col:
        if zen_button("Anuluj", key="cancel_app_settings"):
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
        if zen_button("Dodaj nową lekcję", key="add_new_lesson_btn"):
            st.session_state.add_new_lesson = True
            st.rerun()
    
    with col2:
        lesson_to_edit = st.selectbox("Wybierz lekcję do edycji", 
                                   options=[f"{lesson['id']} - {lesson['title']}" for lesson in lessons])
        if zen_button("Edytuj wybraną lekcję", key="edit_lesson_btn"):
            lesson_id = int(lesson_to_edit.split(" - ")[0])
            st.session_state.edit_lesson_id = lesson_id
            st.rerun()
    
    with col3:
        lesson_to_delete = st.selectbox("Wybierz lekcję do usunięcia", 
                                     options=[f"{lesson['id']} - {lesson['title']}" for lesson in lessons],
                                     key="delete_lesson_select")
        if zen_button("Usuń wybraną lekcję", key="delete_lesson_btn"):
            lesson_id = int(lesson_to_delete.split(" - ")[0])
            # Tutaj logika usuwania lekcji
            notification(f"Lekcja ID: {lesson_id} została usunięta.", "success")
    
    if zen_button("Zamknij", key="close_lessons_management"):
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
        if zen_button("Przywróć kopię", key="restore_backup_confirm"):
            # Tutaj logika przywracania kopii
            with st.spinner(f"Przywracanie kopii {selected_backup}..."):
                import time
                time.sleep(2)
                notification(f"Kopia {selected_backup} została pomyślnie przywrócona.", "success")
                st.session_state.restore_backup = False
                st.rerun()
    
    with col2:
        if zen_button("Anuluj przywracanie", key="cancel_restore_backup"):
            st.session_state.restore_backup = False
            st.rerun()


if __name__ == "__main__":
    show_admin_dashboard()
