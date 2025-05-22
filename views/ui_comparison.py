import streamlit as st
from utils.ui import initialize_ui, theme_selector
from utils.ui.bridge import bridge_degen_card, bridge_stat_card, bridge_content_section, bridge_tip_block

# Import starych komponentów
from utils.components import degen_card, stat_card, content_section, tip_block

def show_comparison():
    """Strona porównująca stare i nowe komponenty UI obok siebie."""
    # Inicjalizacja nowego UI
    initialize_ui()
    
    st.title("Porównanie komponentów UI")
    
    with st.sidebar:
        st.header("Ustawienia")
        theme_selector()
        st.markdown("---")
        st.write("Ten widok porównuje stare komponenty UI z nowymi, aby ułatwić migrację.")
    
    # Intro
    st.markdown("""
    Ta strona pokazuje porównanie starych i nowych komponentów UI. Celem jest pokazanie,
    jak nowe komponenty wyglądają obok starych, aby można było ocenić różnice wizualne
    i ułatwić migrację do nowego systemu UI.
    
    Nowe komponenty zostały zaimplementowane z myślą o zgodności z Content Security Policy (CSP)
    i nie używają inline JavaScript.
    """)
    
    # Porównanie kart
    st.header("Porównanie kart")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Stary degen_card")
        degen_card(
            title="Neurobiologia przywództwa", 
            description="Podstawy neuroprzywództwa i struktura mózgu lidera", 
            icon="🧠", 
            progress=75,
            status="in-progress"
        )
    
    with col2:
        st.subheader("Nowy z bridge_degen_card")
        bridge_degen_card(
            title="Neurobiologia przywództwa", 
            description="Podstawy neuroprzywództwa i struktura mózgu lidera", 
            icon="🧠", 
            progress=75,
            status="in-progress"
        )
    
    # Porównanie kart statystyk
    st.header("Porównanie kart statystyk")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Stary stat_card")
        stat_card(
            label="Ukończone lekcje", 
            value="24", 
            icon="📚",
            change="+3", 
            change_type="positive"
        )
    
    with col2:
        st.subheader("Nowy z bridge_stat_card")
        bridge_stat_card(
            label="Ukończone lekcje", 
            value="24", 
            icon="📚",
            change="+3", 
            change_type="positive"
        )
    
    # Porównanie bloków zawartości
    st.header("Porównanie sekcji zawartości")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Stary content_section")
        content_section(
            "Zaplanowane aktywności",
            """
            <ul>
                <li><strong>Nowy moduł:</strong> Neuroplastyczność</li>
                <li><strong>Wyzwanie:</strong> 30-dniowy challenge</li>
            </ul>
            """,
            collapsed=True,
            icon="📅"
        )
    
    with col2:
        st.subheader("Nowy z bridge_content_section")
        bridge_content_section(
            "Zaplanowane aktywności",
            """
            <ul>
                <li><strong>Nowy moduł:</strong> Neuroplastyczność</li>
                <li><strong>Wyzwanie:</strong> 30-dniowy challenge</li>
            </ul>
            """,
            collapsed=True,
            icon="📅"
        )
    
    # Porównanie wskazówek
    st.header("Porównanie bloków wskazówek")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Stary tip_block")
        tip_block(
            "Zdobywaj punkty XP, kończąc lekcje i misje.",
            type="tip",
            title="Jak zdobywać poziomy?",
            icon="💡"
        )
    
    with col2:
        st.subheader("Nowy z bridge_tip_block")
        bridge_tip_block(
            "Zdobywaj punkty XP, kończąc lekcje i misje.",
            type="tip",
            title="Jak zdobywać poziomy?",
            icon="💡"
        )
    
    # Objaśnienie migracji
    st.markdown("""
    ## Jak migrować komponenty?
    
    ### Opcja 1: Użyj funkcji mostkujących (bridge)
    
    ```python
    # Stary import
    from utils.components import degen_card
    
    # Zamień na:
    from utils.ui.bridge import bridge_degen_card as degen_card
    ```
    
    ### Opcja 2: Bezpośrednia migracja do nowych komponentów
    
    ```python
    # Stary kod
    from utils.components import degen_card
    degen_card(title="Tytuł", description="Opis", icon="🧠", progress=75)
    
    # Nowy kod
    from utils.ui.components.cards import skill_card
    skill_card(category="Tytuł", description="Opis", icon="🧠", 
               progress=75, status="in-progress", completed_count=8, total_count=10)
    ```
    """)

if __name__ == "__main__":
    show_comparison()
