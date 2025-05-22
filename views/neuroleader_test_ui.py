import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
from data.neuroleader_types import NEUROLEADER_TYPES
from data.neuroleader_details import neuroleader_details
from data.users import load_user_data, save_user_data
from utils.ui import initialize_ui
from utils.ui.components.interactive import zen_button, notification
from utils.ui.components.text import section_container, zen_header, tip_block
from utils.ui.components.progress import progress_bar
from utils.ui.layouts.grid import responsive_grid, responsive_container
from utils.ui.layouts.responsive import get_device_type, get_responsive_figure_size

# Lista pytań testowych z oryginału
NEUROLEADER_TEST_QUESTIONS = [
    {
        "question": "W jaki sposób najczęściej podejmujesz decyzje?",
        "type": "decision_making",
        "answers": [
            (4, "Analizuję wszystkie dostępne dane i podejmuję decyzję na podstawie logicznej analizy"),
            (3, "Konsultuję się z zespołem i podejmuję decyzję uwzględniając różne perspektywy"),
            (2, "Opieram się na intuicji i doświadczeniu, podejmuję decyzję szybko"),
            (1, "Rozważam, jak decyzja wpłynie na ludzi i ich potrzeby")
        ]
    },
    {
        "question": "Jak reagujesz na zmiany w organizacji?",
        "type": "adaptability",
        "answers": [
            (1, "Chcę zrozumieć powody i analizuję potencjalne konsekwencje"),
            (4, "Entuzjastycznie przyjmuję zmiany i szukam nowych możliwości"),
            (3, "Akceptuję zmiany, jeśli widzę korzyści dla zespołu"),
            (2, "Akceptuję zmiany, ale wolę stabilne środowisko pracy")
        ]
    },
    {
        "question": "Jak radzisz sobie ze stresem w pracy?",
        "type": "stress_management",
        "answers": [
            (3, "Koncentruję się na rozwiązaniach i działam metodycznie"),
            (2, "Szukam pomocy i wsparcia u innych"),
            (4, "Znajduję sposób, by odreagować (sport, hobby, relaks)"),
            (1, "Analizuję przyczyny stresu i planuję, jak im przeciwdziałać")
        ]
    },
    {
        "question": "Jaki jest Twój styl komunikacji?",
        "type": "communication",
        "answers": [
            (2, "Bezpośredni i nastawiony na fakty"),
            (4, "Inspirujący i motywujący"),
            (1, "Precyzyjny i analityczny"),
            (3, "Empatyczny i wspierający")
        ]
    },
    {
        "question": "Co motywuje Cię najbardziej?",
        "type": "motivation",
        "answers": [
            (3, "Wpływ na innych i możliwość pomagania innym"),
            (1, "Osiąganie mierzalnych rezultatów i sukcesów"),
            (4, "Nowe wyzwania i możliwości rozwoju"),
            (2, "Stabilność i równowaga między życiem zawodowym a prywatnym")
        ]
    }
]

def calculate_test_results(scores):
    """
    Calculate the neuroleader type based on scores
    """
    max_score = max(scores.values())
    max_types = [t for t, s in scores.items() if s == max_score]
    
    # If there's a tie, return the first one for simplicity
    return max_types[0]

def plot_radar_chart(scores, device_type=None):
    """
    Generate a radar chart visualizing test results
    
    Args:
        scores: Dictionary of neuroleader types and their scores
        device_type: 'mobile', 'tablet', or 'desktop'
    """
    if device_type is None:
        device_type = get_device_type()
    
    # Ensure labels and values are properly formatted
    labels = list(scores.keys())
    values = [float(v) for v in scores.values()]
    
    # Set up angles
    num_vars = len(labels)
    angles_degrees = np.linspace(0, 360, num_vars, endpoint=False)
    angles_radians = np.radians(angles_degrees)
    
    # Create closed lists for radar chart
    values_closed = np.concatenate((values, [values[0]]))
    angles_radians_closed = np.concatenate((angles_radians, [angles_radians[0]]))
    
    # Responsive figure size
    fig_size = get_responsive_figure_size(device_type)
    
    # Adjust parameters based on device type
    if device_type == 'mobile':
        title_size = 14
        font_size = 8
        grid_alpha = 0.3
        line_width = 1.5
        marker_size = 4
    elif device_type == 'tablet':
        title_size = 16
        font_size = 9
        grid_alpha = 0.25
        line_width = 2
        marker_size = 6
    else:  # desktop
        title_size = 18
        font_size = 10
        grid_alpha = 0.2
        line_width = 2.5
        marker_size = 8
    
    # Create the plot
    fig = plt.figure(figsize=fig_size)
    ax = fig.add_subplot(111, polar=True)
    
    # Grid
    ax.set_rgrids([20, 40, 60, 80, 100], angle=angles_radians[0], alpha=grid_alpha, 
                  fontsize=font_size)
    
    # Labels
    ax.set_thetagrids(angles_degrees, labels, fontsize=font_size)
    
    # Plot the data
    ax.plot(angles_radians_closed, values_closed, 'o-', linewidth=line_width, 
            markersize=marker_size)
    ax.fill(angles_radians_closed, values_closed, alpha=0.25)
    
    # Title
    dominant_type = calculate_test_results(scores)
    ax.set_title(f"Twój profil: {dominant_type}", fontsize=title_size, 
                 fontweight='bold', pad=20)
    
    # Limits
    ax.set_ylim(0, 100)
    
    # Remove unnecessary elements
    ax.spines['polar'].set_visible(False)
    
    return fig

def reset_test():
    """Reset the neuroleader test state"""
    if 'neuroleader_test_current_question' in st.session_state:
        del st.session_state.neuroleader_test_current_question
    if 'neuroleader_test_answers' in st.session_state:
        del st.session_state.neuroleader_test_answers
    if 'neuroleader_test_scores' in st.session_state:
        del st.session_state.neuroleader_test_scores
    if 'neuroleader_test_completed' in st.session_state:
        del st.session_state.neuroleader_test_completed
    if 'show_test_info' in st.session_state:
        del st.session_state.show_test_info

def handle_test_completion(scores):
    """
    Process test completion and update user data
    """
    # Calculate the dominant type
    dominant_type = calculate_test_results(scores)
    
    # Save to user data
    try:
        users_data = load_user_data()
        username = st.session_state.username
        
        if username not in users_data:
            users_data[username] = {}
        
        if 'tests' not in users_data[username]:
            users_data[username]['tests'] = {}
        
        # Save the test results
        users_data[username]['tests']['neuroleader'] = {
            'scores': scores,
            'type': dominant_type
        }
        
        # Mark test as completed for badges
        if 'completed_tasks' not in users_data[username]:
            users_data[username]['completed_tasks'] = {}
        
        users_data[username]['completed_tasks']['neuroleader_test'] = True
        
        # Save data
        save_user_data(users_data)
        
        notification("Wyniki testu zostały zapisane!", type="success")
    except Exception as e:
        st.error(f"Błąd podczas zapisywania wyników: {str(e)}")

def show_neuroleader_test():
    """
    Display the neuroleader test UI
    """
    # Initialize UI
    initialize_ui()
    
    # Header
    zen_header("Test Neuroliderera", "Odkryj swój dominujący typ Neuroliderera")
    
    # Initialize test state if needed
    if 'neuroleader_test_current_question' not in st.session_state:
        st.session_state.neuroleader_test_current_question = 0
    
    if 'neuroleader_test_answers' not in st.session_state:
        st.session_state.neuroleader_test_answers = {}
    
    if 'neuroleader_test_scores' not in st.session_state:
        st.session_state.neuroleader_test_scores = {neuroleader_type: 0 for neuroleader_type in NEUROLEADER_TYPES}
    
    if 'neuroleader_test_completed' not in st.session_state:
        st.session_state.neuroleader_test_completed = False
    
    if 'show_test_info' not in st.session_state:
        st.session_state.show_test_info = True
    
    # Main content container - ZMIENIONE, aby usunąć błąd
    # Zamiast używać responsive_container jako kontekstowego menedżera,
    # bezpośrednio wyświetlamy zawartość
    
    def show_test_content():
        if st.session_state.show_test_info:
            show_test_info()
        elif st.session_state.neuroleader_test_completed:
            show_test_results()
        else:
            show_test_questions()

    # Użycie responsive_container z funkcją jako argumentem
    responsive_container(show_test_content)

def show_test_info():
    """
    Display information about the neuroleader test
    """
    zen_header("Test Neuroliderera", "Odkryj swój dominujący styl przywództwa")
    
    # Zmień te bloki:
    with section_container("Jak działa ten test?"):
        st.markdown("""
        Ten test pomoże Ci odkryć Twój dominujący styl przywództwa neurobiologicznego. 
        Odpowiedz na serię pytań, a my przeanalizujemy Twoje odpowiedzi, aby określić, 
        który typ neuroliderera najlepiej pasuje do Twojego stylu.
        """)
    
    with section_container("Co zyskasz?"):
        st.markdown("""
        * Identyfikację Twojego dominującego typu neuroliderera
        * Zrozumienie Twoich mocnych stron i wyzwań jako lider
        * Spersonalizowane wskazówki do rozwoju Twoich umiejętności przywódczych
        * Lepsze zrozumienie, jak Twój mózg wpływa na Twój styl przywództwa
        """)
    
    # Na:
    st.markdown("## Jak działa ten test?")
    st.markdown("""
    Ten test pomoże Ci odkryć Twój dominujący styl przywództwa neurobiologicznego. 
    Odpowiedz na serię pytań, a my przeanalizujemy Twoje odpowiedzi, aby określić, 
    który typ neuroliderera najlepiej pasuje do Twojego stylu.
    """)
    
    st.markdown("## Co zyskasz?")
    st.markdown("""
    * Identyfikację Twojego dominującego typu neuroliderera
    * Zrozumienie Twoich mocnych stron i wyzwań jako lider
    * Spersonalizowane wskazówki do rozwoju Twoich umiejętności przywódczych
    * Lepsze zrozumienie, jak Twój mózg wpływa na Twój styl przywództwa
    """)
    
    # Sprawdź też inne podobne bloki w tej funkcji i zamień je analogicznie

    if zen_button("Rozpocznij test", key="start_test_button"):
        st.session_state.show_test_info = False
        st.rerun()

def show_test_questions():
    """Display the current test question"""
    # Get current question
    current_question_idx = st.session_state.neuroleader_test_current_question
    total_questions = len(NEUROLEADER_TEST_QUESTIONS)
    
    # Show progress
    progress_value = (current_question_idx / total_questions) * 100
    progress_bar(progress_value, f"Pytanie {current_question_idx + 1} z {total_questions}")
    
    # Display current question
    if current_question_idx < total_questions:
        question_data = NEUROLEADER_TEST_QUESTIONS[current_question_idx]
        
        with section_container("Pytanie testowe"):  # lub inny odpowiedni tytuł
            st.markdown(f"### {question_data['question']}")
            
            # Create columns for responsive layout
            cols = st.columns([1, 2, 1])
            
            with cols[1]:
                # Display answer options
                for points, answer in question_data['answers']:
                    # Create a unique key for each button
                    button_key = f"nl_answer_{current_question_idx}_{points}"
                    
                    if zen_button(answer, full_width=True, key=button_key):
                        # Save the answer
                        st.session_state.neuroleader_test_answers[current_question_idx] = (points, answer)
                        
                        # Calculate scores
                        calculate_scores()
                        
                        # Move to the next question
                        st.session_state.neuroleader_test_current_question += 1
                        
                        # Check if test is completed
                        if st.session_state.neuroleader_test_current_question >= total_questions:
                            st.session_state.neuroleader_test_completed = True
                            handle_test_completion(st.session_state.neuroleader_test_scores)
                            
                        # Force a rerun to show the next question or results
                        st.rerun()

def calculate_scores():
    """Calculate the scores based on the answers"""
    # Map question types to neuroleader types
    type_mapping = {
        'decision_making': 'Strateg',
        'adaptability': 'Wizjoner',
        'stress_management': 'Mentor', 
        'communication': 'Motywator',
        'motivation': 'Inspirator'
    }
    
    # Initialize scores
    scores = {neuroleader_type: 0 for neuroleader_type in NEUROLEADER_TYPES}
    
    # Calculate points for each answer
    for q_idx, (points, _) in st.session_state.neuroleader_test_answers.items():
        question = NEUROLEADER_TEST_QUESTIONS[q_idx]
        question_type = question['type']
        
        # Map to neuroleader type
        if question_type in type_mapping:
            neuroleader_type = type_mapping[question_type]
            if neuroleader_type in scores:
                scores[neuroleader_type] += points
    
    # Normalize scores to 0-100 scale
    max_possible_per_type = 4  # Assume max 4 points per question
    for neuroleader_type in scores:
        if scores[neuroleader_type] > 0:
            scores[neuroleader_type] = round((scores[neuroleader_type] / max_possible_per_type) * 100)
    
    # Update the session state
    st.session_state.neuroleader_test_scores = scores

def show_test_results():
    """Display the test results"""
    scores = st.session_state.neuroleader_test_scores
    dominant_type = calculate_test_results(scores)
    
    # Header for results
    zen_header("Wyniki Testu Neuroliderera", f"Twój dominujący typ: {dominant_type}")
    
    # Layout for different sections
    cols = responsive_grid(2, mobile_cols=1)
    
    # Left column - Radar chart
    with cols[0]:
        with section_container("Twoje wyniki"):
            # Show radar chart
            fig = plot_radar_chart(scores)
            st.pyplot(fig)
            
            # Display scores as a table
            st.markdown("### Szczegółowe wyniki:")
            
            # Convert scores to DataFrame for better display
            df = pd.DataFrame({
                'Typ Neuroliderera': list(scores.keys()),
                'Wynik (%)': list(scores.values())
            })
            
            # Sort by score descending
            df = df.sort_values('Wynik (%)', ascending=False).reset_index(drop=True)
            
            # Display the table
            st.dataframe(df, hide_index=True, use_container_width=True)
    
    # Right column - Type description
    with cols[1]:
        with section_container(f"Twój typ: {dominant_type}"):
            # Get type details
            if dominant_type in neuroleader_details:
                type_info = neuroleader_details[dominant_type]
                
                # Main description
                st.markdown(f"### {type_info['name']}")
                st.markdown(type_info['description'])
                
                # Strengths and weaknesses
                st.markdown("### Mocne strony:")
                for strength in type_info['strengths']:
                    st.markdown(f"- {strength}")
                
                st.markdown("### Wyzwania:")
                for challenge in type_info['challenges']:
                    st.markdown(f"- {challenge}")
                
                # Tips
                with tip_block():
                    st.markdown("### Jak rozwijać swój potencjał:")
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
    show_neuroleader_test()
