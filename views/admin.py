import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
from datetime import datetime, timedelta
import time
import json
from data.users import load_user_data, save_user_data
from data.lessons import load_lessons
from data.test_questions import DEGEN_TYPES
from config.settings import XP_LEVELS
from utils.material3_components import apply_material3_theme
from utils.components import zen_header, zen_button, notification, data_chart, stat_card
from utils.layout import get_device_type, responsive_grid

def check_admin_auth():
    """Sprawdza uwierzytelnienie administratora"""

    # Oryginalna kontrola uprawnień (zakomentowana na czas testów)
    if not st.session_state.get('logged_in', False):
        st.error("Musisz być zalogowany, aby uzyskać dostęp do panelu administratora.")
        return False
       
    admin_users = ["admin", "zenmaster", "Anna"]  # Dodaj swój login
    if st.session_state.get('username') not in admin_users:
        st.error("Nie masz uprawnień do przeglądania panelu administratora.")
        return False
       
    return True

def get_user_activity_data():
    """Pobiera i przetwarza dane o aktywności użytkowników"""
    users_data = load_user_data()
    
    # Przygotuj dane do analizy
    activity_data = []
    for username, data in users_data.items():
        activity_data.append({
            'username': username,
            'xp': data.get('xp', 0),
            'level': data.get('level', 1),
            'completed_lessons': len(data.get('completed_lessons', [])),
            'degen_type': data.get('degen_type', 'Nieznany'),
            'registration_date': data.get('registration_date', '2023-01-01'),
            'last_login': data.get('last_login', '2023-01-01'),
            'test_taken': data.get('test_taken', False),
            'completed_missions': len(data.get('completed_missions', [])),
            'streak': data.get('streak', 0)
        })
    
    return pd.DataFrame(activity_data)

def get_lessons_stats():
    """Pobiera i analizuje statystyki lekcji"""
    users_data = load_user_data()
    lessons = load_lessons()
    
    # Inicjalizuj liczniki ukończeń dla każdej lekcji
    completion_count = {lesson_id: 0 for lesson_id in lessons.keys()}
    
    # Zlicz ukończenia lekcji
    for username, data in users_data.items():
        completed_lessons = data.get('completed_lessons', [])
        for lesson_id in completed_lessons:
            if lesson_id in completion_count:
                completion_count[lesson_id] += 1
    
    # Utwórz DataFrame ze statystykami lekcji
    lessons_stats = []
    for lesson_id, lesson in lessons.items():
        lessons_stats.append({
            'lesson_id': lesson_id,
            'title': lesson.get('title', 'Brak tytułu'),
            'category': lesson.get('tag', 'Brak kategorii'),
            'difficulty': lesson.get('difficulty', 'intermediate'),
            'completions': completion_count.get(lesson_id, 0),
            'completion_rate': round(completion_count.get(lesson_id, 0) / len(users_data) * 100, 2) if users_data else 0
        })
    
    return pd.DataFrame(lessons_stats)

def get_degen_type_distribution():
    """Analizuje rozkład typów degenów wśród użytkowników"""
    users_data = load_user_data()
    
    # Zlicz wystąpienia każdego typu degena
    degen_counts = {}
    for _, data in users_data.items():
        degen_type = data.get('degen_type', 'Nieznany')
        degen_counts[degen_type] = degen_counts.get(degen_type, 0) + 1
    
    # Utwórz DataFrame dla wizualizacji
    degen_distribution = []
    for degen_type, count in degen_counts.items():
        degen_distribution.append({
            'degen_type': degen_type,
            'count': count,
            'percentage': round(count / len(users_data) * 100, 2) if users_data else 0
        })
    
    return pd.DataFrame(degen_distribution)

def plot_user_activity_over_time():
    """Generuje wykres aktywności użytkowników w czasie"""
    users_data = load_user_data()
    
    # W rzeczywistej aplikacji te dane byłyby pobierane z historii logowań
    # Dla demonstracji generujemy przykładowe dane
    
    # Symulacja dziennej aktywności
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]
    
    # Symulacja liczby aktywnych użytkowników dziennie (losowo)
    np.random.seed(42)  # Dla powtarzalności
    total_users = len(users_data)
    active_users = [int(np.random.binomial(total_users, 0.3 + 0.1 * np.sin(i/5))) for i in range(30)]
    
    # Odwróć listy, aby najnowsze dane były na końcu
    dates.reverse()
    active_users.reverse()
    
    # Utwórz DataFrame
    activity_df = pd.DataFrame({
        'data': dates,
        'aktywni_użytkownicy': active_users
    })
    
    return activity_df

def show_admin_dashboard():
    """Wyświetla panel administratora"""
    # Zastosuj style Material 3 - tymczasowo wykomentowane
    # apply_material3_theme()
    
    # Dodaj informację diagnostyczną
    st.write("DEBUG - show_admin_dashboard() started")
    
    # Sprawdź uwierzytelnienie admina
    if not check_admin_auth():
        # Jeśli użytkownik nie jest administratorem, wyświetl przycisk powrotu
        if zen_button("Powrót do strony głównej"):
            st.session_state.page = 'dashboard'
            st.rerun()
        return
    
    # Nagłówek panelu administratora
    zen_header("🛡️ Panel Administratora")
    
    # Pobierz urządzenie
    device_type = get_device_type()
    
    # Dodaj informację o ostatnim odświeżeniu
    st.markdown(f"**Ostatnie odświeżenie:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Przycisk do odświeżania danych
    if zen_button("🔄 Odśwież dane"):
        st.rerun()
    
    # Zakładki główne panelu administratora
    admin_tabs = st.tabs(["Przegląd", "Użytkownicy", "Lekcje", "Testy", "Zarządzanie"])
    
    # 1. Zakładka Przegląd
    with admin_tabs[0]:
        st.subheader("Przegląd statystyk platformy")
        
        # Pobierz dane
        users_data = load_user_data()
        user_df = get_user_activity_data()
        
        # Podstawowe statystyki
        total_users = len(users_data)
        total_lessons_completed = user_df['completed_lessons'].sum()
        avg_xp = int(user_df['xp'].mean()) if not user_df.empty else 0
        tests_taken = user_df['test_taken'].sum()
        
        # Wyświetl statystyki w responsywnym układzie
        stats_cols = responsive_grid(4, 2, 1)
        
        with stats_cols[0]:
            stat_card("Liczba użytkowników", total_users, "👥")
        
        with stats_cols[1]:
            stat_card("Ukończone lekcje", int(total_lessons_completed), "📚")
        
        with stats_cols[2]:
            stat_card("Średnie XP", avg_xp, "⭐")
        
        with stats_cols[3]:
            stat_card("Wykonane testy", int(tests_taken), "📊")
        
        # Wykresy aktywności
        st.subheader("Aktywność użytkowników")
        
        activity_df = plot_user_activity_over_time()
        
        # Wykres aktywności użytkowników
        chart = alt.Chart(activity_df).mark_line(point=True).encode(
            x=alt.X('data:T', title='Data'),
            y=alt.Y('aktywni_użytkownicy:Q', title='Liczba aktywnych użytkowników'),
            tooltip=['data', 'aktywni_użytkownicy']
        ).properties(
            width='container',
            height=350,
            title='Dzienna aktywność użytkowników (ostatnie 30 dni)'
        )
        
        st.altair_chart(chart, use_container_width=True)
        
        # Rozkład typów degenów
        st.subheader("Rozkład typów degenów")
        
        degen_df = get_degen_type_distribution()
        
        if not degen_df.empty:
            # Wykres kołowy typów degenów
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.pie(degen_df['count'], labels=degen_df['degen_type'], autopct='%1.1f%%', 
                   startangle=90, shadow=False)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            st.pyplot(fig)
        else:
            st.info("Brak danych o typach degenów.")
    
    # 2. Zakładka Użytkownicy
    with admin_tabs[1]:
        st.subheader("Szczegóły użytkowników")
        
        # Pobierz dane
        user_df = get_user_activity_data()
        
        # Filtrowanie użytkowników
        filter_cols = st.columns(3)
        with filter_cols[0]:
            min_xp = st.number_input("Min XP", min_value=0, value=0)
        with filter_cols[1]:
            degen_filter = st.selectbox("Filtruj wg typu degena", 
                                       options=["Wszystkie"] + list(user_df['degen_type'].unique()))
        with filter_cols[2]:
            sort_by = st.selectbox("Sortuj wg", 
                                   options=["xp", "level", "completed_lessons", "username"])
        
        # Zastosuj filtry
        filtered_df = user_df
        if min_xp > 0:
            filtered_df = filtered_df[filtered_df['xp'] >= min_xp]
        
        if degen_filter != "Wszystkie":
            filtered_df = filtered_df[filtered_df['degen_type'] == degen_filter]
        
        # Sortuj dane
        filtered_df = filtered_df.sort_values(by=sort_by, ascending=False)
        
        # Wyświetl tabelę użytkowników
        st.dataframe(
            filtered_df,
            column_config={
                "username": "Nazwa użytkownika",
                "xp": "XP",
                "level": "Poziom",
                "completed_lessons": "Ukończone lekcje",
                "degen_type": "Typ degena",
                "test_taken": "Test wykonany",
                "streak": "Seria dni"
            },
            use_container_width=True
        )
        
        # Dodaj opcję eksportu danych
        if zen_button("Eksportuj dane użytkowników do CSV"):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Pobierz CSV",
                data=csv,
                file_name="users_data.csv",
                mime="text/csv"
            )
    
    # 3. Zakładka Lekcje
    with admin_tabs[2]:
        st.subheader("Statystyki lekcji")
        
        # Pobierz dane lekcji
        lessons_df = get_lessons_stats()
        
        # Wyświetl tabelę statystyk lekcji
        st.dataframe(
            lessons_df,
            column_config={
                "lesson_id": "ID lekcji",
                "title": "Tytuł",
                "category": "Kategoria",
                "difficulty": st.column_config.SelectboxColumn(
                    "Poziom trudności", 
                    options=["beginner", "intermediate", "advanced"],
                    required=True
                ),
                "completions": "Liczba ukończeń",
                "completion_rate": st.column_config.ProgressColumn(
                    "Wskaźnik ukończenia (%)",
                    min_value=0,
                    max_value=100,
                    format="%{value:.2f}"
                )
            },
            use_container_width=True
        )
        
        # Wykres popularności lekcji (top 10)
        st.subheader("Najpopularniejsze lekcje")
        
        top_lessons = lessons_df.sort_values('completions', ascending=False).head(10)
        
        if not top_lessons.empty:
            chart = alt.Chart(top_lessons).mark_bar().encode(
                x=alt.X('completions:Q', title='Liczba ukończeń'),
                y=alt.Y('title:N', title='Lekcja', sort='-x'),
                color=alt.Color('category:N', title='Kategoria'),
                tooltip=['title', 'category', 'completions', 'completion_rate']
            ).properties(
                width='container',
                height=400,
                title='Top 10 najpopularniejszych lekcji'
            )
            
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Brak danych o ukończonych lekcjach.")
    
    # 4. Zakładka Testy
    with admin_tabs[3]:
        st.subheader("Wyniki testów Degena")
        
        # Pobierz dane o użytkownikach
        users_data = load_user_data()
        
        # Zbierz dane o wynikach testów
        test_results = []
        for username, data in users_data.items():
            if data.get('test_scores'):
                for degen_type, score in data.get('test_scores', {}).items():
                    test_results.append({
                        'username': username,
                        'degen_type': degen_type,
                        'score': score
                    })
        
        test_df = pd.DataFrame(test_results)
        
        if not test_df.empty:
            # Średnie wyniki dla każdego typu degena
            st.subheader("Średnie wyniki dla typów degenów")
            
            avg_scores = test_df.groupby('degen_type')['score'].mean().reset_index()
            avg_scores['score'] = avg_scores['score'].round(2)
            
            chart = alt.Chart(avg_scores).mark_bar().encode(
                x=alt.X('degen_type:N', title='Typ degena'),
                y=alt.Y('score:Q', title='Średni wynik'),
                color=alt.Color('degen_type:N', title='Typ degena'),
                tooltip=['degen_type', 'score']
            ).properties(
                width='container',
                height=350,
                title='Średnie wyniki testów wg typu degena'
            )
            
            st.altair_chart(chart, use_container_width=True)
            
            # Tabela z wynikami testów
            st.subheader("Szczegółowe wyniki testów")
            st.dataframe(
                test_df,
                column_config={
                    "username": "Nazwa użytkownika",
                    "degen_type": "Typ degena",
                    "score": "Wynik"
                },
                use_container_width=True
            )
        else:
            st.info("Brak danych o wynikach testów.")
    
    # 5. Zakładka Zarządzanie
    with admin_tabs[4]:
        st.subheader("Zarządzanie użytkownikami")
        
        # Pobierz dane
        users_data = load_user_data()
        usernames = list(users_data.keys())
        
        # Wybór użytkownika
        selected_user = st.selectbox("Wybierz użytkownika", options=usernames)
        
        if selected_user:
            user_data = users_data.get(selected_user, {})
            
            # Wyświetl szczegóły użytkownika
            st.json(user_data)
            
            # Akcje zarządzania
            action_cols = st.columns(3)
            
            with action_cols[0]:
                if zen_button("🔄 Reset postępu XP", key="reset_xp"):
                    if st.session_state.get('confirm_reset_xp', False):
                        # Wykonaj reset XP
                        users_data[selected_user]['xp'] = 0
                        users_data[selected_user]['level'] = 1
                        save_user_data(users_data)
                        st.session_state.confirm_reset_xp = False
                        notification("Zresetowano XP użytkownika.", type="success")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.session_state.confirm_reset_xp = True
                        st.warning("Czy na pewno chcesz zresetować XP? Kliknij ponownie, aby potwierdzić.")
            
            with action_cols[1]:
                if zen_button("📚 Reset ukończonych lekcji", key="reset_lessons"):
                    if st.session_state.get('confirm_reset_lessons', False):
                        # Wykonaj reset ukończonych lekcji
                        users_data[selected_user]['completed_lessons'] = []
                        save_user_data(users_data)
                        st.session_state.confirm_reset_lessons = False
                        notification("Zresetowano ukończone lekcje użytkownika.", type="success")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.session_state.confirm_reset_lessons = True
                        st.warning("Czy na pewno chcesz zresetować ukończone lekcje? Kliknij ponownie, aby potwierdzić.")
            
            with action_cols[2]:
                if zen_button("🗑️ Usuń użytkownika", key="delete_user"):
                    if st.session_state.get('confirm_delete', False):
                        # Wykonaj usunięcie użytkownika
                        users_data.pop(selected_user, None)
                        save_user_data(users_data)
                        st.session_state.confirm_delete = False
                        notification("Usunięto użytkownika.", type="success")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.session_state.confirm_delete = True
                        st.warning("Czy na pewno chcesz usunąć tego użytkownika? Ta operacja jest nieodwracalna! Kliknij ponownie, aby potwierdzić.")
            
            # Dodatkowe ustawienia użytkownika
            st.subheader("Edycja danych użytkownika")
            
            edit_cols = st.columns(2)
            with edit_cols[0]:
                new_xp = st.number_input("Punkty XP", min_value=0, value=user_data.get('xp', 0))
            
            with edit_cols[1]:
                new_level = st.number_input("Poziom", min_value=1, value=user_data.get('level', 1))
            
            # Admin status
            is_admin = st.checkbox("Administrator", value=selected_user in ["admin", "zenmaster"])
            
            # Zapisz zmiany
            if zen_button("Zapisz zmiany"):
                users_data[selected_user]['xp'] = new_xp
                users_data[selected_user]['level'] = new_level
                
                # Zapisz dane
                save_user_data(users_data)
                notification("Zapisano zmiany.", type="success")
                time.sleep(1)
                st.rerun()
        
        # Przycisk eksportu kopii zapasowej
        st.subheader("Kopia zapasowa")
        if zen_button("💾 Eksportuj kopię zapasową danych"):
            # Konwertuj dane do formatu JSON
            users_json = json.dumps(users_data, indent=4)
            
            # Oferuj plik do pobrania
            st.download_button(
                label="Pobierz kopię zapasową (JSON)",
                data=users_json,
                file_name=f"zen_degen_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )