import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
from data.neuroleader_types import NEUROLEADER_TYPES
from data.neuroleader_details import neuroleader_details
from data.users import load_user_data, save_user_data
from utils.components import zen_header, zen_button, progress_bar, notification, content_section, tip_block
from utils.material3_components import apply_material3_theme
from utils.layout import get_device_type, responsive_grid, responsive_container, toggle_device_view, apply_responsive_styles, get_responsive_figure_size
from utils.card_layout import load_card_layout, create_card, create_grid, zen_section, data_panel

# Pytania do testu typów neuroliderów - wykorzystujemy istniejące
from views.neuroleader_test import NEUROLEADER_TEST_QUESTIONS, calculate_test_results, plot_radar_chart

def show_neuroleader_test_card_layout():
    """
    Shows the neuroleader test page with card-based layout.
    """
    # Zastosuj style Material 3
    
    # Load card layout CSS
    load_card_layout()
    
    # Zastosuj responsywne style
    apply_responsive_styles()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    zen_header("Test Typu Neuroliderera")
    
    # Informacja o teście
    if 'show_test_info' not in st.session_state:
        st.session_state.show_test_info = True
    
    if st.session_state.show_test_info:
        # Intro section
        zen_section(
            "Jak działa ten test?",
            "Poznaj swój styl przywództwa neurobiologicznego",
            "🧠"
        )
        
        # Test instructions card
        create_card(
            title="Instrukcja testu",
            icon="📋",
            content=f"""
            <div style="padding: 10px 0;">
                <p>Ten test pomoże Ci sprawdzić, <strong>jakim typem neuroliderera jesteś</strong>.</p>
                
                <ul>
                    <li>Każde pytanie ma <strong>6 odpowiedzi</strong> – każda reprezentuje inny styl przywództwa neurobiologicznego.</li>
                    <li><strong>Wybierz tę odpowiedź, która najlepiej opisuje Twoje zachowanie lub sposób myślenia.</strong></li>
                    <li>Po zakończeniu zobaczysz graficzny wynik w postaci wykresu radarowego oraz szczegółowy opis Twojego dominującego typu neuroliderera.</li>
                </ul>
                
                <p style="margin-top: 20px; font-weight: 500;">🧠 Gotowy?</p>
            </div>
            """,
            footer_content='<button class="zen-button">Rozpocznij test</button>',
            key="start_test_card",
            on_click=lambda: (
                setattr(st.session_state, 'show_test_info', False),
                setattr(st.session_state, 'test_step', 0) if 'test_step' not in st.session_state else None,
                setattr(st.session_state, 'test_scores', {neuroleader_type: 0 for neuroleader_type in NEUROLEADER_TYPES}) if 'test_scores' not in st.session_state else None,
                st.rerun()
            )
        )
        
        # Optional section to browse neuroleader types
        zen_section(
            "Przeglądaj typy neuroliderów",
            "Zapoznaj się z różnymi typami przed rozpoczęciem testu",
            "📚"
        )
        
        # Type selector
        selected_type = st.selectbox("Wybierz typ neuroliderera:", list(NEUROLEADER_TYPES.keys()))
        
        if selected_type:
            # Display selected type info in card layout
            create_card(
                title=selected_type,
                icon="🧠",
                content=f"""
                <div style="padding: 10px 0; color: {NEUROLEADER_TYPES[selected_type]['color']};">
                    <p style="font-weight: 500;">{NEUROLEADER_TYPES[selected_type]['description']}</p>
                    
                    <h4>Mocne strony:</h4>
                    <ul>
                        {"".join([f"<li>✅ {strength}</li>" for strength in NEUROLEADER_TYPES[selected_type]['strengths']])}
                    </ul>
                    
                    <h4>Wyzwania:</h4>
                    <ul>
                        {"".join([f"<li>⚠️ {challenge}</li>" for challenge in NEUROLEADER_TYPES[selected_type]['challenges']])}
                    </ul>
                    
                    <h4>Rekomendowana strategia:</h4>
                    <p>{NEUROLEADER_TYPES[selected_type]['strategy']}</p>
                </div>
                """,
                key="browse_type_card"
            )
            
            # Show detailed description if requested
            if st.checkbox("Pokaż szczegółowy opis typu"):
                if selected_type in neuroleader_details:
                    st.markdown(neuroleader_details[selected_type])
                else:
                    st.warning("Szczegółowy opis dla tego typu neuroliderera nie jest jeszcze dostępny.")
    
    # Test mode
    elif 'test_step' not in st.session_state:
        st.session_state.test_step = 0
        st.session_state.test_scores = {neuroleader_type: 0 for neuroleader_type in NEUROLEADER_TYPES}
        st.rerun()
    
    elif st.session_state.test_step < len(NEUROLEADER_TEST_QUESTIONS):
        # Display current question
        question = NEUROLEADER_TEST_QUESTIONS[st.session_state.test_step]
        
        # Create question card
        create_card(
            title=f"Pytanie {st.session_state.test_step + 1} z {len(NEUROLEADER_TEST_QUESTIONS)}",
            icon="❓",
            content=f"""
            <div style="padding: 10px 0;">
                <h3 style="margin-bottom: 20px;">{question['question']}</h3>
            </div>
            """,
            key="question_card"
        )
        
        # Options layout
        options = question['options']
        
        # Use responsive layout based on device type
        if device_type == 'mobile':
            # On mobile phones show options stacked
            for i in range(len(options)):
                if zen_button(f"{options[i]['text']}", key=f"q{st.session_state.test_step}_opt{i}", use_container_width=True):
                    # Add scores for the answer
                    for neuroleader_type, score in options[i]['scores'].items():
                        st.session_state.test_scores[neuroleader_type] += score
                    
                    st.session_state.test_step += 1
                    st.rerun()
        else:
            # On tablets and desktops use two columns
            col1, col2 = st.columns(2)
            for i in range(len(options)):
                if i < len(options) // 2:
                    with col1:
                        if zen_button(f"{options[i]['text']}", key=f"q{st.session_state.test_step}_opt{i}", use_container_width=True):
                            # Add scores for the answer
                            for neuroleader_type, score in options[i]['scores'].items():
                                st.session_state.test_scores[neuroleader_type] += score
                            
                            st.session_state.test_step += 1
                            st.rerun()
                else:
                    with col2:
                        if zen_button(f"{options[i]['text']}", key=f"q{st.session_state.test_step}_opt{i}", use_container_width=True):
                            # Add scores for the answer
                            for neuroleader_type, score in options[i]['scores'].items():
                                st.session_state.test_scores[neuroleader_type] += score
                            
                            st.session_state.test_step += 1
                            st.rerun()
        
        # Progress bar
        progress_value = st.session_state.test_step / len(NEUROLEADER_TEST_QUESTIONS)
        progress_bar(progress=progress_value, color="#4CAF50")
        st.markdown(f"**Postęp testu: {int(progress_value * 100)}%**")
    
    else:
        # Show test results
        dominant_type = calculate_test_results(st.session_state.test_scores)
        
        # Update user data
        users_data = load_user_data()
        users_data[st.session_state.username]["neuroleader_type"] = dominant_type
        users_data[st.session_state.username]["neuroleader_test_taken"] = True
        users_data[st.session_state.username]["neuroleader_test_scores"] = st.session_state.test_scores
        users_data[st.session_state.username]["xp"] += 50  # Bonus XP for completing the test
        save_user_data(users_data)
        
        # Results section
        zen_section(
            "Wyniki testu",
            "Poznaj swój dominujący typ neuroliderera",
            "🏆"
        )
        
        # Results header card
        create_card(
            title=f"Twój dominujący typ to: {dominant_type}",
            icon="🧠",
            content=f"""
            <div style="padding: 20px 0; text-align: center;">
                <h2 style="color: {NEUROLEADER_TYPES[dominant_type]['color']}; margin-bottom: 15px;">{dominant_type}</h2>
                <p style="font-size: 1.1rem;">{NEUROLEADER_TYPES[dominant_type]['description']}</p>
            </div>
            """,
            key="results_header_card"
        )
        
        # Radar chart
        radar_fig = plot_radar_chart(st.session_state.test_scores, device_type=device_type)
        st.pyplot(radar_fig)
        
        # Display strengths and challenges based on device type
        col1, col2 = st.columns(2) if device_type != 'mobile' else [st.container(), st.container()]
        
        with col1:
            create_card(
                title="Twoje mocne strony",
                icon="💪",
                content=f"""
                <ul>
                    {"".join([f"<li>✅ {strength}</li>" for strength in NEUROLEADER_TYPES[dominant_type]['strengths']])}
                </ul>
                """,
                key="strengths_card"
            )
        
        with col2:
            create_card(
                title="Twoje wyzwania",
                icon="🚧",
                content=f"""
                <ul>
                    {"".join([f"<li>⚠️ {challenge}</li>" for challenge in NEUROLEADER_TYPES[dominant_type]['challenges']])}
                </ul>
                """,
                key="challenges_card"
            )
        
        # Strategy card
        create_card(
            title="Rekomendowana strategia",
            icon="🎯",
            content=f"""
            <div style="padding: 10px 0;">
                <p>{NEUROLEADER_TYPES[dominant_type]['strategy']}</p>
            </div>
            """,
            key="strategy_card"
        )
        
        # Detailed description
        with st.expander("Szczegółowy opis twojego typu neuroliderera", expanded=False):
            st.markdown(neuroleader_details.get(dominant_type, "Szczegółowy opis dla tego typu neuroliderera nie jest jeszcze dostępny."))
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if zen_button("Wykonaj test ponownie", use_container_width=True):
                st.session_state.test_step = 0
                st.session_state.test_scores = {neuroleader_type: 0 for neuroleader_type in NEUROLEADER_TYPES}
                st.session_state.show_test_info = True
                st.rerun()
        
        with col2:
            if zen_button("Przejdź do dashboardu", use_container_width=True):
                st.session_state.test_step = 0
                st.session_state.page = 'dashboard'
                st.rerun()
