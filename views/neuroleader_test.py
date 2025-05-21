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

# Pytania do testu typów neuroliderów
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
            {"text": "Podejmuję wykalkulowane ryzyko po rozważeniu różnych perspektyw.", "scores": {"Neurobalanser": 3, "Neuroanalityk": 1}},
            {"text": "Koncentruję się na tym, jak ryzyko wpłynie na ludzi i relacje.", "scores": {"Neuroempata": 3, "Neurobalanser": 1}},
            {"text": "Widzę w ryzyku szansę na innowację i rozwój.", "scores": {"Neuroinnowator": 3, "Neuroinspirator": 1}},
            {"text": "Inspiruję innych do odważnego podejmowania wyzwań mimo niepewności.", "scores": {"Neuroinspirator": 3, "Neuroreaktor": 1}}
        ]
    }
]

def calculate_test_results(scores):
    """Calculate the dominant neuroleader type based on test scores"""
    return max(scores.items(), key=lambda x: x[1])[0]

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
    ax.set_title("Twój profil neuroleaderski", size=title_size, pad=20)
    
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

def show_neuroleader_test():
    # Zastosuj style Material 3
    apply_material3_theme()
    
    # Zastosuj responsywne style
    apply_responsive_styles()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    zen_header("Test Typu Neurolidera")
    
    # Informacja o teście
    if 'show_test_info' not in st.session_state:
        st.session_state.show_test_info = True
    
    if st.session_state.show_test_info:
        st.markdown("""
        ### 👉 Jak działa ten test?

        Ten test pomoże Ci sprawdzić, **jakim typem neuroliderera jesteś**.

        - Każde pytanie ma **6 odpowiedzi** – każda reprezentuje inny styl przywództwa neurobiologicznego.
        - **Wybierz tę odpowiedź, która najlepiej opisuje Twoje zachowanie lub sposób myślenia.**
        - Po zakończeniu zobaczysz graficzny wynik w postaci wykresu radarowego oraz szczegółowy opis Twojego dominującego typu neuroliderera.        
        
        🧠 Gotowy? 
        """)
        if zen_button("Rozpocznij test"):
            st.session_state.show_test_info = False
            if 'test_step' not in st.session_state:
                st.session_state.test_step = 0
                st.session_state.test_scores = {neuroleader_type: 0 for neuroleader_type in NEUROLEADER_TYPES}
            st.rerun()
        
        # Opcja przeglądania typów neuroliderów
        st.markdown("---")
        st.markdown("### 📚 Chcesz dowiedzieć się więcej o typach neuroliderów?")
        selected_type = st.selectbox("Wybierz typ neuroliderera:", list(NEUROLEADER_TYPES.keys()))
        
        if selected_type:
            st.markdown(f"### {selected_type}")
            
            # Użyj responsywnego układu w zależności od typu urządzenia
            if device_type == 'mobile':
                # Na telefonach wyświetl sekcje jedna pod drugą
                content_section("Mocne strony:", 
                               "\n".join([f"- ✅ {strength}" for strength in NEUROLEADER_TYPES[selected_type]["strengths"]]), 
                               icon="💪", 
                               collapsed=False)
                
                content_section("Wyzwania:", 
                               "\n".join([f"- ⚠️ {challenge}" for challenge in NEUROLEADER_TYPES[selected_type]["challenges"]]), 
                               icon="🚧", 
                               collapsed=False)
            else:
                # Na tabletach i desktopach użyj dwóch kolumn
                col1, col2 = st.columns(2)
                with col1:
                    content_section("Mocne strony:", 
                                   "\n".join([f"- ✅ {strength}" for strength in NEUROLEADER_TYPES[selected_type]["strengths"]]), 
                                   icon="💪", 
                                   collapsed=False)
                
                with col2:
                    content_section("Wyzwania:", 
                                   "\n".join([f"- ⚠️ {challenge}" for challenge in NEUROLEADER_TYPES[selected_type]["challenges"]]), 
                                   icon="🚧", 
                                   collapsed=False)
            
            tip_block(NEUROLEADER_TYPES[selected_type]["strategy"], "Rekomendowana strategia")
            
            # Dodajemy szczegółowy opis typu neuroliderera
            if st.checkbox("Pokaż szczegółowy opis typu"):
                if selected_type in neuroleader_details:
                    st.markdown(neuroleader_details[selected_type])
                else:
                    st.warning("Szczegółowy opis dla tego typu neuroliderera nie jest jeszcze dostępny.")
    
    # Tryb testu
    elif 'test_step' not in st.session_state:
        st.session_state.test_step = 0
        st.session_state.test_scores = {neuroleader_type: 0 for neuroleader_type in NEUROLEADER_TYPES}
        st.rerun()
    
    elif st.session_state.test_step < len(NEUROLEADER_TEST_QUESTIONS):
        # Display current question
        question = NEUROLEADER_TEST_QUESTIONS[st.session_state.test_step]
        
        st.markdown("<div class='st-bx'>", unsafe_allow_html=True)
        st.subheader(f"Pytanie {st.session_state.test_step + 1} z {len(NEUROLEADER_TEST_QUESTIONS)}")
        st.markdown(f"### {question['question']}")
        
        # Render options in two columns
        options = question['options']
        
        # Użyj responsywnego układu w zależności od typu urządzenia
        if device_type == 'mobile':
            # Na telefonach wyświetl opcje jedna pod drugą
            for i in range(len(options)):
                if zen_button(f"{options[i]['text']}", key=f"q{st.session_state.test_step}_opt{i}", use_container_width=True):
                    # Add scores for the answer
                    for neuroleader_type, score in options[i]['scores'].items():
                        st.session_state.test_scores[neuroleader_type] += score
                    
                    st.session_state.test_step += 1
                    st.rerun()
        else:
            # Na tabletach i desktopach użyj dwóch kolumn
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
        st.markdown("</div>", unsafe_allow_html=True)
    
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
        
        st.markdown("<div class='st-bx'>", unsafe_allow_html=True)
        st.subheader("Wyniki testu")
        
        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 30px;'>
            <h2>Twój dominujący typ Neuroliderera to:</h2>
            <h1 style='color: {NEUROLEADER_TYPES[dominant_type]["color"]};'>{dominant_type}</h1>
            <p>{NEUROLEADER_TYPES[dominant_type]["description"]}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Radar chart
        radar_fig = plot_radar_chart(st.session_state.test_scores, device_type=device_type)
        
        # Add mobile-specific styles for the chart container
        if device_type == 'mobile':
            st.markdown("""
            <style>
            .radar-chart-container {
                margin: 0 -20px; /* Negative margin to use full width on mobile */
                padding-bottom: 15px;
            }
            </style>
            <div class="radar-chart-container">
            """, unsafe_allow_html=True)
            
        st.pyplot(radar_fig)
        
        if device_type == 'mobile':
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Display strengths and challenges based on device type
        if device_type == 'mobile':
            # Na telefonach wyświetl sekcje jedna pod drugą
            content_section(
                "Twoje mocne strony:", 
                "\n".join([f"- ✅ {strength}" for strength in NEUROLEADER_TYPES[dominant_type]["strengths"]]),
                icon="💪",
                collapsed=False
            )
            
            content_section(
                "Twoje wyzwania:", 
                "\n".join([f"- ⚠️ {challenge}" for challenge in NEUROLEADER_TYPES[dominant_type]["challenges"]]),
                icon="🚧",
                collapsed=False
            )
        else:
            # Na tabletach i desktopach użyj dwóch kolumn
            col1, col2 = st.columns(2)
            with col1:
                content_section(
                    "Twoje mocne strony:", 
                    "\n".join([f"- ✅ {strength}" for strength in NEUROLEADER_TYPES[dominant_type]["strengths"]]),
                    icon="💪",
                    collapsed=False
                )
            with col2:
                content_section(
                    "Twoje wyzwania:", 
                    "\n".join([f"- ⚠️ {challenge}" for challenge in NEUROLEADER_TYPES[dominant_type]["challenges"]]),
                    icon="🚧",
                    collapsed=False
                )
        
        tip_block(NEUROLEADER_TYPES[dominant_type]["strategy"], title="Rekomendowana strategia", icon="🎯")
        
        # Dodanie szczegółowych informacji o typie neuroliderera
        content_section(
            "Szczegółowy opis twojego typu neuroliderera", 
            neuroleader_details.get(dominant_type, "Szczegółowy opis dla tego typu neuroliderera nie jest jeszcze dostępny."),
            icon="🔍",
            collapsed=True
        )
        
        # Additional options
        if zen_button("Wykonaj test ponownie"):
            st.session_state.test_step = 0
            st.session_state.test_scores = {neuroleader_type: 0 for neuroleader_type in NEUROLEADER_TYPES}
            st.session_state.show_test_info = True
            st.rerun()
            
        if zen_button("Przejdź do dashboardu"):
            st.session_state.test_step = 0
            st.session_state.page = 'dashboard'
            st.rerun()
