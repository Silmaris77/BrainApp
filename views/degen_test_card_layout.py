import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
from data.test_questions import DEGEN_TYPES, TEST_QUESTIONS
from data.users import load_user_data, save_user_data
from data.degen_details import degen_details
from utils.components import zen_header, zen_button, progress_bar, notification, content_section, tip_block
from utils.material3_components import apply_material3_theme
from utils.layout import get_device_type, responsive_grid, responsive_container, toggle_device_view, apply_responsive_styles, get_responsive_figure_size
from utils.card_layout import load_card_layout, create_card, create_grid, zen_section, data_panel

def calculate_test_results(scores):
    """Calculate the dominant degen type based on test scores"""
    return max(scores.items(), key=lambda x: x[1])[0]

def plot_radar_chart(scores, device_type=None):
    """Generate a radar chart for test results
    
    Args:
        scores: Dictionary of degen types and their scores
        device_type: Device type ('mobile', 'tablet', or 'desktop')
    """
    # Jeśli device_type nie został przekazany, pobierz go
    if device_type is None:
        device_type = get_device_type()
        
    # ZMIANA: Upewnij się, że labels i values są listami o tym samym rozmiarze
    labels = list(scores.keys())
    values = [float(v) for v in scores.values()]
    
    # ZMIANA: Utwórz kąty i od razu skonwertuj na stopnie
    num_vars = len(labels)
    angles_degrees = np.linspace(0, 360, num_vars, endpoint=False)
    angles_radians = np.radians(angles_degrees)
    
    # ZMIANA: Tworzenie zamkniętych list bez używania wycinków [:-1]
    values_closed = np.concatenate((values, [values[0]]))
    angles_radians_closed = np.concatenate((angles_radians, [angles_radians[0]]))
    
    # Użyj funkcji helper do ustalenia rozmiaru wykresu
    fig_size = get_responsive_figure_size(device_type)
    
    # Dostosuj pozostałe parametry w zależności od urządzenia
    if device_type == 'mobile':
        title_size = 14
        font_size = 6.5
        grid_alpha = 0.3
        line_width = 1.5
        marker_size = 4
    elif device_type == 'tablet':
        title_size = 16
        font_size = 8
        grid_alpha = 0.4
        line_width = 2
        marker_size = 5
    else:  # desktop
        title_size = 18
        font_size = 9
        grid_alpha = 0.5
        line_width = 2.5
        marker_size = 6
    
    # Tworzenie i konfiguracja wykresu
    fig, ax = plt.subplots(figsize=fig_size, subplot_kw=dict(polar=True))
    
    # Dodaj przezroczyste tło za etykietami dla lepszej czytelności
    ax.set_facecolor('white')
    if device_type == 'mobile':
        # Na telefonach zwiększ kontrast
        ax.set_facecolor('#f8f8f8')
    
    # Plot the radar chart with marker size adjusted for device
    ax.plot(angles_radians_closed, values_closed, 'o-', linewidth=line_width, markersize=marker_size)
    ax.fill(angles_radians_closed, values_closed, alpha=0.25)
    
    # Ensure we have a valid limit
    max_val = max(values) if max(values) > 0 else 1
    y_max = max_val * 1.2  # Add some padding at the top
    ax.set_ylim(0, y_max)
    
    # Adjust label positions and appearance for better device compatibility
    # For mobile, rotate labels to fit better on small screens
    if device_type == 'mobile':
        # Use shorter labels on mobile
        ax.set_thetagrids(angles_degrees, labels, fontsize=font_size-1)
        plt.setp(ax.get_xticklabels(), rotation=67.5)  # Rotate labels for better fit
    else:
        ax.set_thetagrids(angles_degrees, labels, fontsize=font_size)
    
    # Set title with responsive size
    ax.set_title("Twój profil inwestycyjny", size=title_size, pad=20)
    
    # Dostosuj siatkę i oś
    ax.grid(True, alpha=grid_alpha)
    
    # Dodaj etykiety z wartościami
    # Dostosuj odległość etykiet od wykresu
    label_pad = max_val * (0.05 if device_type == 'mobile' else 0.1)

    # Poprawiona wersja:
    for i, (angle, value) in enumerate(zip(angles_radians, values)):
        color = DEGEN_TYPES[labels[i]]["color"]
        
        # Na telefonach wyświetl tylko nazwę typu bez wyniku
        if device_type == 'mobile':
            display_text = f"{labels[i].split()[0]}"  # Use only the first word
        else:
            display_text = f"{labels[i]}\n({value})"
            
        # Add text labels with background for better visibility
        ax.text(angle, value + label_pad, display_text, 
                horizontalalignment='center', verticalalignment='center',
                fontsize=font_size, color=color, fontweight='bold',
                bbox=dict(facecolor='white', alpha=0.7, pad=1.5, edgecolor='none'))
    
    # Optimize layout
    plt.tight_layout(pad=1.0 if device_type == 'mobile' else 1.5)
    
    # Use high DPI for better rendering on high-resolution displays
    fig.set_dpi(120 if device_type == 'mobile' else 100)
    
    return fig

def show_degen_test_card_layout():
    # Zastosuj style Material 3
    
    # Zastosuj responsywne style
    apply_responsive_styles()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    # Determine the layout grid size based on device type
    num_columns = 1 if device_type == 'mobile' else 2
    
    zen_header("Test Typu Degena")
    
    # Informacja o teście
    if 'show_test_info' not in st.session_state:
        st.session_state.show_test_info = True
    
    if st.session_state.show_test_info:
        # Test information card
        create_card(
            title="Jak działa ten test?",
            icon="👉",
            content="""
            <div style="padding: 10px 0;">
                <p>Ten test pomoże Ci sprawdzić, <strong>jakim typem inwestora (degena)</strong> jesteś.</p>
                <ul style="margin-top: 10px; padding-left: 20px;">
                    <li>Każde pytanie ma <strong>8 odpowiedzi</strong> – każda reprezentuje inny styl inwestycyjny.</li>
                    <li><strong>Wybierz tę odpowiedź, która najlepiej opisuje Twoje zachowanie lub sposób myślenia.</strong></li>
                    <li>Po zakończeniu zobaczysz graficzny wynik w postaci wykresu radarowego.</li>
                </ul>
                <p style="margin-top: 15px; font-weight: 500;">🧩 Gotowy?</p>
            </div>
            """,
            key="test_info_card"
        )
        
        # Start button
        if zen_button("Rozpocznij test"):
            st.session_state.show_test_info = False
            if 'test_step' not in st.session_state:
                st.session_state.test_step = 0
                st.session_state.test_scores = {degen_type: 0 for degen_type in DEGEN_TYPES}
            st.rerun()
        
        # Learn more about degen types section
        zen_section("Chcesz dowiedzieć się więcej o typach degenów?", icon="📚")
        
        # Degen types explorer card
        create_card(
            title="Przeglądaj typy degenów",
            icon="🔍",
            content="""
            <p style="margin-bottom: 15px;">Wybierz typ degena, aby poznać jego charakterystykę:</p>
            """,
            key="degen_explorer_card"
        )
        
        selected_type = st.selectbox("Wybierz typ degena:", list(DEGEN_TYPES.keys()))
        
        if selected_type:
            # Create a grid layout for strengths and challenges
            cols = create_grid(num_columns)
            
            # Display the selected degen type in a card
            with cols[0]:
                # Strengths card
                create_card(
                    title="Mocne strony",
                    icon="💪",
                    content="""
                    <ul style="padding-left: 20px;">
                        {}
                    </ul>
                    """.format("\n".join([f"<li>✅ {strength}</li>" for strength in DEGEN_TYPES[selected_type]["strengths"]])),
                    key=f"strengths_{selected_type}"
                )
            
            with cols[1 if num_columns > 1 else 0]:
                # Challenges card
                create_card(
                    title="Wyzwania",
                    icon="🚧",
                    content="""
                    <ul style="padding-left: 20px;">
                        {}
                    </ul>
                    """.format("\n".join([f"<li>⚠️ {challenge}</li>" for challenge in DEGEN_TYPES[selected_type]["challenges"]])),
                    key=f"challenges_{selected_type}"
                )
            
            # Strategy card
            create_card(
                title="Rekomendowana strategia",
                icon="🎯",
                content=f"<p style='padding: 10px 0;'>{DEGEN_TYPES[selected_type]['strategy']}</p>",
                key=f"strategy_{selected_type}"
            )
            
            # Detailed description (expandable)
            with st.expander("Pokaż szczegółowy opis typu"):
                if selected_type in degen_details:
                    st.markdown(degen_details[selected_type])
                else:
                    st.info("Szczegółowy opis tego typu nie jest jeszcze dostępny.")
    else:
        # Test in progress - handle question flow
        if 'test_step' not in st.session_state:
            st.session_state.test_step = 0
            st.session_state.test_scores = {degen_type: 0 for degen_type in DEGEN_TYPES}
        
        # Progress bar
        progress = (st.session_state.test_step) / len(TEST_QUESTIONS) * 100
        progress_bar(progress, f"Pytanie {st.session_state.test_step + 1} z {len(TEST_QUESTIONS)}")
        
        # Get current question
        if st.session_state.test_step < len(TEST_QUESTIONS):
            question_data = TEST_QUESTIONS[st.session_state.test_step]
            
            # Question card
            create_card(
                title=f"Pytanie {st.session_state.test_step + 1}",
                icon="❓",
                content=f"""
                <div style="padding: 15px 0;">
                    <p style="font-size: 1.1rem; font-weight: 500; margin-bottom: 15px;">{question_data['question']}</p>
                </div>
                """,
                key=f"question_card_{st.session_state.test_step}"
            )
            
            # Answers as options
            answer_index = st.radio(
                "Wybierz odpowiedź, która najlepiej opisuje Ciebie:",
                options=range(len(question_data['answers'])),
                format_func=lambda i: question_data['answers'][i]['text'],
                key=f"q_{st.session_state.test_step}"
            )
            
            # Navigation buttons
            cols = st.columns([1, 1])
            
            with cols[1]:
                if st.button("Następne pytanie", key=f"next_{st.session_state.test_step}"):
                    # Update scores
                    answer_type = question_data['answers'][answer_index]['type']
                    st.session_state.test_scores[answer_type] += 1
                    
                    # Move to next question
                    st.session_state.test_step += 1
                    
                    # Check if test is complete
                    if st.session_state.test_step >= len(TEST_QUESTIONS):
                        # Test complete - calculate final result
                        dominant_type = calculate_test_results(st.session_state.test_scores)
                        
                        # Save results to user data
                        user_data = load_user_data().get(st.session_state.username, {})
                        user_data['degen_type'] = dominant_type
                        user_data['degen_scores'] = st.session_state.test_scores
                        save_user_data(st.session_state.username, user_data)
                        
                        # Award XP for completing the test
                        if not user_data.get('completed_degen_test', False):
                            user_data['xp'] = user_data.get('xp', 0) + 50
                            user_data['completed_degen_test'] = True
                            save_user_data(st.session_state.username, user_data)
                            notification("Zdobyłeś 50 XP za ukończenie testu!")
                    
                    st.rerun()
            
            with cols[0]:
                if st.session_state.test_step > 0:
                    if st.button("Wróć", key=f"back_{st.session_state.test_step}"):
                        # Go back to previous question
                        st.session_state.test_step -= 1
                        st.rerun()
        else:
            # Test complete - show results
            scores = st.session_state.test_scores
            dominant_type = calculate_test_results(scores)
            
            # Results header card
            create_card(
                title=f"Twój dominujący typ to: {dominant_type}",
                icon="🏆",
                content=f"""
                <div style="padding: 15px 0; text-align: center;">
                    <h2 style="color: {DEGEN_TYPES[dominant_type]['color']}; margin-bottom: 15px;">{dominant_type}</h2>
                    <p style="font-size: 1.1rem;">{DEGEN_TYPES[dominant_type]['description']}</p>
                </div>
                """,
                key="results_header_card"
            )
            
            # Results chart card
            chart_container = create_card(
                title="Twoje wyniki na wykresie",
                icon="📊",
                content="<div id='chart-container' style='padding: 10px 0; display: flex; justify-content: center;'></div>",
                key="results_chart_card"
            )
            
            with chart_container:
                fig = plot_radar_chart(scores)
                st.pyplot(fig)
            
            # Type details cards
            cols = create_grid(num_columns)
            
            with cols[0]:
                # Strengths card
                create_card(
                    title="Twoje mocne strony",
                    icon="💪",
                    content="""
                    <ul style="padding-left: 20px;">
                        {}
                    </ul>
                    """.format("\n".join([f"<li>✅ {strength}</li>" for strength in DEGEN_TYPES[dominant_type]["strengths"]])),
                    key="strengths_card"
                )
            
            with cols[1 if num_columns > 1 else 0]:
                # Challenges card
                create_card(
                    title="Twoje wyzwania",
                    icon="🚧",
                    content="""
                    <ul style="padding-left: 20px;">
                        {}
                    </ul>
                    """.format("\n".join([f"<li>⚠️ {challenge}</li>" for challenge in DEGEN_TYPES[dominant_type]["challenges"]])),
                    key="challenges_card"
                )
            
            # Strategy card
            create_card(
                title="Zalecana strategia",
                icon="🎯",
                content=f"<p style='padding: 10px 0;'>{DEGEN_TYPES[dominant_type]['strategy']}</p>",
                key="strategy_card"
            )
            
            # Detailed description (expandable)
            with st.expander("Pokaż szczegółowy opis typu"):
                if dominant_type in degen_details:
                    st.markdown(degen_details[dominant_type])
                else:
                    st.info("Szczegółowy opis tego typu nie jest jeszcze dostępny.")
            
            # Restart button
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("Zresetuj test"):
                    # Reset test state
                    st.session_state.test_step = 0
                    st.session_state.test_scores = {degen_type: 0 for degen_type in DEGEN_TYPES}
                    st.session_state.show_test_info = True
                    st.rerun()
