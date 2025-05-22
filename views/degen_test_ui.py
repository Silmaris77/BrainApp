import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
from data.test_questions import DEGEN_TYPES, TEST_QUESTIONS
from data.users import load_user_data, save_user_data
from data.degen_details import degen_details
from utils.ui import initialize_ui
from utils.ui.components.interactive import zen_button, notification
from utils.ui.components.text import content_section, zen_header, tip_block
from utils.ui.components.progress import progress_bar
from utils.ui.layouts.grid import responsive_grid, responsive_container
from utils.ui.layouts.responsive import get_device_type, get_responsive_figure_size

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
        
    # Upewnij się, że labels i values są listami o tym samym rozmiarze
    labels = list(scores.keys())
    values = [float(v) for v in scores.values()]
    
    # Utwórz kąty i od razu skonwertuj na stopnie
    num_vars = len(labels)
    angles_degrees = np.linspace(0, 360, num_vars, endpoint=False)
    angles_radians = np.radians(angles_degrees)
    
    # Tworzenie zamkniętych list bez używania wycinków [:-1]
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
        grid_alpha = 0.3
        line_width = 2
        marker_size = 6
    else:  # desktop
        title_size = 18
        font_size = 10
        grid_alpha = 0.2
        line_width = 2.5
        marker_size = 8

    # Tworzenie wykresu
    fig = plt.figure(figsize=fig_size)
    ax = fig.add_subplot(111, polar=True)
    
    # Wygląd siatki
    ax.set_rgrids([20, 40, 60, 80, 100], angle=angles_radians[0], alpha=grid_alpha, 
                  fontsize=font_size)
    
    # Etykiety kategorii z odpowiednim obrotem
    ax.set_thetagrids(angles_degrees, labels, fontsize=font_size)
    
    # Linia wykresu
    ax.plot(angles_radians_closed, values_closed, 'o-', linewidth=line_width, 
            markersize=marker_size)
    ax.fill(angles_radians_closed, values_closed, alpha=0.25)
    
    # Tytuł wykresu
    dominant_type = calculate_test_results(scores)
    ax.set_title(f"Twój wynik: {dominant_type}", fontsize=title_size, 
                 fontweight='bold', pad=20)
    
    # Limity osi
    ax.set_ylim(0, 100)
    
    # Usuń zbędne elementy
    ax.spines['polar'].set_visible(False)
    
    return fig

def reset_test():
    """Reset the test state"""
    if 'degen_test_current_question' in st.session_state:
        del st.session_state.degen_test_current_question
    if 'degen_test_answers' in st.session_state:
        del st.session_state.degen_test_answers
    if 'degen_test_scores' in st.session_state:
        del st.session_state.degen_test_scores
    if 'degen_test_completed' in st.session_state:
        del st.session_state.degen_test_completed

def handle_test_completion(scores):
    """Process test completion and update user data"""
    # Calculate the dominant degen type
    dominant_type = calculate_test_results(scores)
    
    # Save to user data
    try:
        users_data = load_user_data()
        username = st.session_state.username
        
        if username not in users_data:
            users_data[username] = {}
            
        if 'tests' not in users_data[username]:
            users_data[username]['tests'] = {}
            
        # Save test results
        users_data[username]['tests']['degen'] = {
            'scores': scores,
            'type': dominant_type
        }
        
        # Mark as completed in user profile for badges
        if 'completed_tasks' not in users_data[username]:
            users_data[username]['completed_tasks'] = {}
            
        users_data[username]['completed_tasks']['degen_test'] = True
        
        # Save updated data
        save_user_data(users_data)
        
        notification("Wyniki testu zostały zapisane!", type="success")
    except Exception as e:
        st.error(f"Błąd podczas zapisywania wyników: {str(e)}")

def show_degen_test():
    """Main function to show the degen test UI"""
    # Initialize UI
    initialize_ui()
    
    # Header
    zen_header("Test Degena", "Odkryj swój dominujący typ osobowości Degena")
    
    # Initialize test state if not already initialized
    if 'degen_test_current_question' not in st.session_state:
        st.session_state.degen_test_current_question = 0
    
    if 'degen_test_answers' not in st.session_state:
        st.session_state.degen_test_answers = {}
    
    if 'degen_test_scores' not in st.session_state:
        st.session_state.degen_test_scores = {degen_type: 0 for degen_type in DEGEN_TYPES}
    
    if 'degen_test_completed' not in st.session_state:
        st.session_state.degen_test_completed = False
    
    # Main content container
    with responsive_container():
        # Check if the test is completed
        if st.session_state.degen_test_completed:
            show_test_results()
        else:
            show_test_questions()

def show_test_questions():
    """Display the current test question"""
    # Get current question
    current_question_idx = st.session_state.degen_test_current_question
    total_questions = len(TEST_QUESTIONS)
    
    # Show progress
    progress_value = (current_question_idx / total_questions) * 100
    progress_bar(progress_value, f"Pytanie {current_question_idx + 1} z {total_questions}")
    
    # Display current question
    if current_question_idx < total_questions:
        question_data = TEST_QUESTIONS[current_question_idx]
        
        with content_section():
            st.markdown(f"### {question_data['question']}")
            
            # Create columns for responsive layout
            cols = st.columns([1, 2, 1])
            
            with cols[1]:
                # Display answer options
                for points, answer in question_data['answers']:
                    # Create a unique key for each button
                    button_key = f"answer_{current_question_idx}_{points}"
                    
                    if zen_button(answer, full_width=True, key=button_key):
                        # Save the answer
                        st.session_state.degen_test_answers[current_question_idx] = (points, answer)
                        
                        # Calculate scores
                        calculate_scores()
                        
                        # Move to the next question
                        st.session_state.degen_test_current_question += 1
                        
                        # Check if test is completed
                        if st.session_state.degen_test_current_question >= total_questions:
                            st.session_state.degen_test_completed = True
                            handle_test_completion(st.session_state.degen_test_scores)
                            
                        # Force a rerun to show the next question or results
                        st.rerun()

def calculate_scores():
    """Calculate the scores based on the current answers"""
    scores = {degen_type: 0 for degen_type in DEGEN_TYPES}
    
    for q_idx, (points, _) in st.session_state.degen_test_answers.items():
        question = TEST_QUESTIONS[q_idx]
        degen_type = question['type']
        
        # Add points to the corresponding degen type
        if degen_type in scores:
            scores[degen_type] += points
    
    # Normalize scores (0-100 scale)
    for degen_type in scores:
        # Calculate the maximum possible score for this type
        max_possible = 0
        count = 0
        
        for q in TEST_QUESTIONS:
            if q['type'] == degen_type:
                # Get the maximum points possible for this question
                max_points = max([p for p, _ in q['answers']])
                max_possible += max_points
                count += 1
        
        # Avoid division by zero
        if max_possible > 0 and scores[degen_type] > 0:
            scores[degen_type] = round((scores[degen_type] / max_possible) * 100)
    
    # Update the session state
    st.session_state.degen_test_scores = scores

def show_test_results():
    """Display the test results"""
    scores = st.session_state.degen_test_scores
    dominant_type = calculate_test_results(scores)
    
    # Header for results
    zen_header("Wyniki Testu Degena", f"Twój dominujący typ: {dominant_type}")
    
    # Layout for different sections
    cols = responsive_grid(2, mobile_cols=1)
    
    # Left column - Radar chart
    with cols[0]:
        with content_section("Twoje wyniki"):
            # Show radar chart
            fig = plot_radar_chart(scores)
            st.pyplot(fig)
            
            # Display scores as a table
            st.markdown("### Szczegółowe wyniki:")
            
            # Convert scores to DataFrame for better display
            df = pd.DataFrame({
                'Typ Degena': list(scores.keys()),
                'Wynik (%)': list(scores.values())
            })
            
            # Sort by score descending
            df = df.sort_values('Wynik (%)', ascending=False).reset_index(drop=True)
            
            # Display the table
            st.dataframe(df, hide_index=True, use_container_width=True)
    
    # Right column - Type description
    with cols[1]:
        with content_section(f"Twój typ: {dominant_type}"):
            # Get type details
            if dominant_type in degen_details:
                type_info = degen_details[dominant_type]
                
                # Main description
                st.markdown(f"### {type_info['name']}")
                st.markdown(type_info['description'])
                
                # Strengths and weaknesses
                st.markdown("### Mocne strony:")
                for strength in type_info['strengths']:
                    st.markdown(f"- {strength}")
                
                st.markdown("### Słabe strony:")
                for weakness in type_info['weaknesses']:
                    st.markdown(f"- {weakness}")
                
                # Tips
                with tip_block():
                    st.markdown("### Jak się rozwijać:")
                    st.markdown(type_info['development_tips'])
            else:
                st.error(f"Nie znaleziono informacji o typie {dominant_type}")
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if zen_button("Rozpocznij test od nowa", full_width=True):
            reset_test()
            st.rerun()
    
    with col2:
        if zen_button("Wróć do dashboardu", full_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

if __name__ == "__main__":
    # Test the module
    show_degen_test()
