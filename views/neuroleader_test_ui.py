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

# Lista pytań testowych z pliku neuroleader_test.py
NEUROLEADER_TEST_QUESTIONS = [
    {
        "question": "Jak zazwyczaj podchodzisz do podejmowania decyzji w sytuacjach stresowych?",
        "options": [
            {"text": "Analizuję szczegółowo wszystkie dane, co czasem opóźnia decyzję.", "scores": {"Neuroanalityk": 3, "Neurobalanser": 1}},
            {"text": "Podejmuję szybkie decyzje pod wpływem emocji i impulsu.", "scores": {"Neuroreaktor": 3, "Neuroinnowator": 1}},
            {"text": "Staram się znaleźć równowagę między analizą a intuicją.", "scores": {"Neurobalanser": 3, "Neuroanalityk": 1}},
            {"text": "Myślę przede wszystkim o emocjonalnych potrzebach zespołu.", "scores": {"Neuroempata": 3, "Neurobalanser": 1}},
            {"text": "Dostosowuję się do sytuacji i szukam innowacyjnych rozwiązań.", "scores": {"Neuroinnowator": 3, "Neuroinspirator": 1}},
            {"text": "Inspiruję innych swoją wizją i entuzjazmem.", "scores": {"Neuroinspirator": 3, "Neuroempata": 1}}
        ]
    },
    {
        "question": "Jak reagujesz na niepowodzenia w pracy zespołowej?",
        "options": [
            {"text": "Dogłębnie analizuję, co poszło nie tak, by uniknąć podobnych błędów.", "scores": {"Neuroanalityk": 3, "Neurobalanser": 1}},
            {"text": "Odczuwam silne emocje i często reaguję impulsywnie.", "scores": {"Neuroreaktor": 3, "Neuroinnowator": 1}},
            {"text": "Szukam konstruktywnych rozwiązań, łącząc analizę z empatią.", "scores": {"Neurobalanser": 3, "Neuroempata": 1}},
            {"text": "Koncentruję się na emocjonalnym wsparciu członków zespołu.", "scores": {"Neuroempata": 3, "Neurobalanser": 1}},
            {"text": "Szybko adaptuję się do nowej sytuacji i szukam alternatywnych ścieżek.", "scores": {"Neuroinnowator": 3, "Neuroreaktor": 1}},
            {"text": "Motywuję zespół swoim entuzjazmem, by nie tracili wiary w sukces.", "scores": {"Neuroinspirator": 3, "Neuroempata": 1}}
        ]
    },
    {
        "question": "W jaki sposób komunikujesz się z zespołem?",
        "options": [
            {"text": "Przekazuję precyzyjne, dokładne informacje oparte na faktach.", "scores": {"Neuroanalityk": 3, "Neurobalanser": 1}},
            {"text": "Komunikuję się bezpośrednio i emocjonalnie, czasem impulsywnie.", "scores": {"Neuroreaktor": 3, "Neuroinspirator": 1}},
            {"text": "Łączę jasny przekaz merytoryczny z empatycznym podejściem.", "scores": {"Neurobalanser": 3, "Neuroempata": 1}},
            {"text": "Koncentruję się na emocjonalnych aspektach komunikacji i budowaniu relacji.", "scores": {"Neuroempata": 3, "Neurobalanser": 1}},
            {"text": "Dostosowuję styl komunikacji do sytuacji i osoby.", "scores": {"Neuroinnowator": 3, "Neurobalanser": 1}},
            {"text": "Inspiruję i motywuję przez charyzmatyczny, wizjonerski przekaz.", "scores": {"Neuroinspirator": 3, "Neuroinnowator": 1}}
        ]
    },
    {
        "question": "Co jest dla Ciebie największym wyzwaniem jako lidera?",
        "options": [
            {"text": "Podejmowanie szybkich decyzji bez nadmiernej analizy.", "scores": {"Neuroanalityk": 3, "Neurobalanser": 1}},
            {"text": "Kontrolowanie emocjonalnych reakcji w stresujących sytuacjach.", "scores": {"Neuroreaktor": 3, "Neuroempata": 1}},
            {"text": "Znalezienie idealnej równowagi między analizą a działaniem.", "scores": {"Neurobalanser": 3, "Neuroanalityk": 1}},
            {"text": "Zachowanie obiektywizmu i niezbytniego angażowania się emocjonalnie.", "scores": {"Neuroempata": 3, "Neuroreaktor": 1}},
            {"text": "Utrzymanie stabilności przy ciągłym wprowadzaniu zmian.", "scores": {"Neuroinnowator": 3, "Neurobalanser": 1}},
            {"text": "Niedominowanie nad zespołem swoją silną osobowością.", "scores": {"Neuroinspirator": 3, "Neuroinnowator": 1}}
        ]
    },
    {
        "question": "Jak podchodzisz do wprowadzania zmian w organizacji?",
        "options": [
            {"text": "Analizuję dokładnie wszystkie ryzyka i korzyści przed wprowadzeniem zmiany.", "scores": {"Neuroanalityk": 3, "Neurobalanser": 1}},
            {"text": "Działam szybko i dynamicznie, gdy widzę potrzebę zmiany.", "scores": {"Neuroreaktor": 3, "Neuroinnowator": 1}},
            {"text": "Równoważę analizę z intuicją, uwzględniając różne perspektywy.", "scores": {"Neurobalanser": 3, "Neuroanalityk": 1}},
            {"text": "Koncentruję się na tym, jak zmiana wpłynie na ludzi i ich emocje.", "scores": {"Neuroempata": 3, "Neurobalanser": 1}},
            {"text": "Entuzjastycznie wprowadzam innowacje i eksperymentuję z nowymi podejściami.", "scores": {"Neuroinnowator": 3, "Neuroreaktor": 1}},
            {"text": "Tworzę inspirującą wizję zmiany, która motywuje innych do działania.", "scores": {"Neuroinspirator": 3, "Neuroempata": 1}}
        ]
    },
    {
        "question": "Co motywuje Cię jako lidera?",
        "options": [
            {"text": "Dokładność i perfekcja w realizacji zadań.", "scores": {"Neuroanalityk": 3, "Neurobalanser": 1}},
            {"text": "Wyzwania i możliwość szybkiego działania.", "scores": {"Neuroreaktor": 3, "Neuroinnowator": 1}},
            {"text": "Osiąganie zrównoważonych i trwałych rezultatów.", "scores": {"Neurobalanser": 3, "Neuroanalityk": 1}},
            {"text": "Budowanie silnych, pozytywnych relacji w zespole.", "scores": {"Neuroempata": 3, "Neurobalanser": 1}},
            {"text": "Możliwość wprowadzania innowacji i zmian.", "scores": {"Neuroinnowator": 3, "Neuroinspirator": 1}},
            {"text": "Inspirowanie innych i tworzenie wizjonerskich projektów.", "scores": {"Neuroinspirator": 3, "Neuroempata": 1}}
        ]
    },
    {
        "question": "Jak zarządzasz konfliktem w zespole?",
        "options": [
            {"text": "Analizuję przyczyny, szukam optymalnego rozwiązania opartego na faktach.", "scores": {"Neuroanalityk": 3, "Neurobalanser": 1}},
            {"text": "Reaguję szybko i bezpośrednio, czasem emocjonalnie.", "scores": {"Neuroreaktor": 3, "Neuroinspirator": 1}},
            {"text": "Poszukuję kompromisu uwzględniającego różne perspektywy.", "scores": {"Neurobalanser": 3, "Neuroempata": 1}},
            {"text": "Koncentruję się na emocjach i potrzebach zaangażowanych osób.", "scores": {"Neuroempata": 3, "Neurobalanser": 1}},
            {"text": "Szukam kreatywnych, nietypowych rozwiązań sytuacji konfliktowej.", "scores": {"Neuroinnowator": 3, "Neuroreaktor": 1}},
            {"text": "Wykorzystuję charyzmę, by zjednoczyć strony konfliktu wokół wspólnej wizji.", "scores": {"Neuroinspirator": 3, "Neuroinnowator": 1}}
        ]
    },
    {
        "question": "Jak podchodzisz do ryzyka i niepewności?",
        "options": [
            {"text": "Unikam ryzyka, dokładnie analizując wszystkie możliwe scenariusze.", "scores": {"Neuroanalityk": 3, "Neurobalanser": 1}},
            {"text": "Podejmuję ryzyko impulsywnie, kierując się intuicją i emocjami.", "scores": {"Neuroreaktor": 3, "Neuroinnowator": 1}},
            {"text": "Podejmuję wykalkulowane ryzyko po rozważeniu różnych perspektywy", "scores": {"Neurobalanser": 3, "Neuroanalityk": 1}},
            {"text": "Koncentruję się na tym, jak ryzyko wpłynęło na ludzi i relacje.", "scores": {"Neuroempata": 3, "Neurobalanser": 1}},
            {"text": "Widzę w ryzyku szansę na innowację i rozwój.", "scores": {"Neuroinnowator": 3, "Neuroinspirator": 1}},
            {"text": "Inspiruję innych do odważnego podejmowania wyzwań mimo niepewności.", "scores": {"Neuroinspirator": 3, "Neuroreaktor": 1}}
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
    """Generate a radar chart for test results
    
    Args:
        scores: Dictionary of neuroleader types and their scores
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
    
    # Dodaj przezroczyste tło za etykietami dla lepszego czytelności
    ax.set_facecolor('white')
    if device_type == 'mobile':
        # Na telefonach zwiększ kontrast
        ax.set_facecolor('#f8f8f8')
    
    # Plot the radar chart with marker size adjusted for device
    ax.plot(angles_radians_closed, values_closed, 'o-', linewidth=line_width, markersize=marker_size)
    ax.fill(angles_radians_closed, values_closed, alpha=0.25)
    
    # Ensure we have a valid limit
    max_val = max(values) if max(values) > 0 else 1
    
    # Ustaw skalę osi Y
    grid_values = [2, 4, 6, 8, 10, 12, 14] if max_val <= 14 else np.arange(0, max_val+1, max_val/7)
    ax.set_yticks(grid_values)
    plt.setp(ax.get_yticklabels(), fontsize=font_size-1)
    
    # Ustaw wartości osi X (nazwy typów neuroleaderów)
    ax.set_xticks(angles_radians)
    
    # Dodaj etykiety typów na osiach - kluczowy element
    if device_type == 'mobile':
        # Na telefonach skróć nazwy typów
        shortened_labels = [label.split()[0] for label in labels]  # Użyj tylko pierwszego słowa
        ax.set_xticklabels(shortened_labels, fontsize=font_size-1)
        plt.setp(ax.get_xticklabels(), rotation=67.5)  # Obróć etykiety dla lepszego dopasowania
    else:
        ax.set_xticklabels(labels, fontsize=font_size)
    
    # Plot the radar chart with marker size adjusted for device
    dominant_type = calculate_test_results(scores)
    dominant_color = NEUROLEADER_TYPES[dominant_type]["color"]
    
    ax.plot(angles_radians_closed, values_closed, 'o-', 
            linewidth=line_width, markersize=marker_size,
            color=dominant_color)  # Użyj koloru dominującego typu
    ax.fill(angles_radians_closed, values_closed, alpha=0.25, color=dominant_color)
    
    # Ensure we have a valid limit
    y_max = max_val * 1.2  # Add some padding at the top
    ax.set_ylim(0, y_max)
    
    # Set title with responsive size
    ax.set_title("Twój profil neuroleaderski", size=title_size, pad=20)
    # ax.set_xticklabels(labels, fontsize=font_size)
    # Dostosuj siatkę i oś
    ax.grid(True, alpha=grid_alpha)
    
    # Dodaj etykiety z wartościami
    # Dostosuj odległość etykiet od wykresu
    label_pad = max_val * (0.05 if device_type == 'mobile' else 0.1)

    # Dodaj etykiety z wartościami
    for i, (angle, value) in enumerate(zip(angles_radians, values)):
        color = NEUROLEADER_TYPES[labels[i]]["color"]
        
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
        
        # Dodane: Zapisz też wyniki w głównej strukturze danych użytkownika,
        # aby były dostępne w zakładce Profil/Typ Neurolidera
        users_data[username]['neuroleader_type'] = dominant_type
        users_data[username]['neuroleader_scores'] = scores
        
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
    
    # Header - Ten nagłówek wyświetla się raz na samej górze
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
    
    # Bezpośrednio wyświetlamy zawartość
    if st.session_state.show_test_info:
        show_test_info(display_header=False)  # Nie wyświetlaj nagłówka ponownie
    elif st.session_state.neuroleader_test_completed:
        show_test_results()
    else:
        show_test_questions()

def show_test_info(display_header=True):
    """
    Display information about the neuroleader test
    
    Args:
        display_header: Whether to display the header (default: True)
    """
    # Wyświetl nagłówek tylko jeśli display_header=True
    if display_header:
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
    """Display the test questions"""
    current_question = st.session_state.neuroleader_test_current_question
    
    if current_question < len(NEUROLEADER_TEST_QUESTIONS):
        question_data = NEUROLEADER_TEST_QUESTIONS[current_question]
        
        with section_container():
            # Header and progress
            st.subheader(f"Pytanie {current_question + 1} z {len(NEUROLEADER_TEST_QUESTIONS)}")
            progress = (current_question / len(NEUROLEADER_TEST_QUESTIONS)) * 100
            st.progress(progress / 100)
            st.markdown(f"**{progress:.0f}% ukończone**")
            
            # Question
            st.markdown(f"### {question_data['question']}")
            
            # Display options
            for i, option in enumerate(question_data['options']):
                button_key = f"q{current_question}_opt{i}"
                
                if st.button(option['text'], key=button_key, use_container_width=True):
                    # Store the selected option and scores
                    st.session_state.neuroleader_test_answers[current_question] = (i, option['text'])
                    
                    # Update scores
                    for neuroleader_type, score in option['scores'].items():
                        if neuroleader_type in st.session_state.neuroleader_test_scores:
                            st.session_state.neuroleader_test_scores[neuroleader_type] += score
                    
                    # Move to next question or complete the test
                    st.session_state.neuroleader_test_current_question += 1
                    if st.session_state.neuroleader_test_current_question >= len(NEUROLEADER_TEST_QUESTIONS):
                        st.session_state.neuroleader_test_completed = True
                    
                    st.rerun()

def calculate_scores():
    """
    Calculate and normalize the scores from the test answers.
    This function is not needed if we're directly updating st.session_state.neuroleader_test_scores
    during question answering.
    """
    # Wyniki już są aktualizowane przy odpowiadaniu na pytania, więc możemy tylko znormalizować
    scores = st.session_state.neuroleader_test_scores
    
    # Znajdź wartość maksymalną do normalizacji (jeśli potrzebne)
    max_score = max(scores.values()) if any(scores.values()) else 1
    
    # Normalizacja do 0-100
    normalized_scores = {}
    for neuroleader_type, score in scores.items():
        # Zapewnij minimalny wynik 10 punktów dla każdego typu
        normalized_scores[neuroleader_type] = 10 + int((score / max_score) * 90) if max_score > 0 else 10
    
    # Update session state
    st.session_state.neuroleader_test_scores = normalized_scores
    
    return normalized_scores

def show_test_results():
    """Display the test results"""
    scores = st.session_state.neuroleader_test_scores
    dominant_type = calculate_test_results(scores)
    
    # Zapisz wyniki w danych użytkownika
    handle_test_completion(scores)
    
    # Header for results
    zen_header("Wyniki Testu Neuroliderera", f"Twój dominujący typ: {dominant_type}")
    
    # SEKCJA 1: Wykres i szczegółowe wyniki w dwóch kolumnach
    st.markdown("## Podsumowanie wyników")
    
    # Tworzenie siatki dla wykresu i tabeli wyników
    chart_cols = responsive_grid(columns_desktop=2, columns_tablet=2, columns_mobile=1)
    
    # Lewa kolumna - Wykres radarowy
    with chart_cols[0]:
        # Show radar chart
        fig = plot_radar_chart(scores)
        st.pyplot(fig)
    
    # Prawa kolumna - Tabela z wynikami
    with chart_cols[1]:
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
    
    # SEKCJA 2: Opis typu neuroliderera w jednej kolumnie poniżej
    st.markdown("---")
    
    # Opis typu w jednej kolumnie na całą szerokość
    with section_container(f"Twój typ neuroliderera: {dominant_type}"):
        # Get type details
        if dominant_type in neuroleader_details:
            type_info = neuroleader_details[dominant_type]
            
            # Sprawdź, czy type_info jest słownikiem
            if isinstance(type_info, dict):
                # Main description
                st.markdown(f"### {type_info.get('name', dominant_type)}")
                st.markdown(type_info.get('description', 'Brak opisu'))
                
                # Dwie kolumny dla mocnych stron i wyzwań
                strengths_challenges = st.columns(2)
                
                # Mocne strony w lewej kolumnie
                with strengths_challenges[0]:
                    st.markdown("### Mocne strony:")
                    for strength in type_info.get('strengths', []):
                        st.markdown(f"- {strength}")
                
                # Wyzwania w prawej kolumnie
                with strengths_challenges[1]:
                    st.markdown("### Wyzwania:")
                    for challenge in type_info.get('challenges', []):
                        st.markdown(f"- {challenge}")
                
                # Wskazówki na całą szerokość
                st.markdown("### Jak rozwijać swój potencjał:")
                st.info(type_info.get('development_tips', 'Brak wskazówek'))
            else:
                # Jeśli type_info jest stringiem lub innym typem, wyświetl go bezpośrednio
                st.markdown(f"### {dominant_type}")
                st.markdown(str(type_info))
        else:
            st.error(f"Nie znaleziono informacji o typie {dominant_type}")
    
    # Action buttons
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if zen_button("Rozpocznij test od nowa", key="restart_test_button"):
            reset_test()
            st.rerun()
    
    with col2:
        if zen_button("Wróć do dashboardu", key="back_to_dashboard_button"):
            st.session_state.page = "dashboard"
            st.rerun()

if __name__ == "__main__":
    # Test the module
    show_neuroleader_test()
