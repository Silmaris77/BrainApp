import streamlit as st

def zen_header(title, subtitle=None):
    """
    Tworzy nagłówek dla strony.
    
    Parametry:
    - title: Tytuł strony
    - subtitle: Podtytuł (opcjonalny)
    """
    st.markdown(f"<h1 class='zen-header'>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p class='zen-subtitle'>{subtitle}</p>", unsafe_allow_html=True)

def quote_block(text, author=None):
    """
    Tworzy blok cytatu.
    
    Parametry:
    - text: Tekst cytatu
    - author: Autor cytatu (opcjonalnie)
    """
    author_html = f'<div style="text-align: right; font-style: italic;">— {author}</div>' if author else ""
    
    quote_html = f"""
    <div class="quote-block">
        <div class="quote-text">{text}</div>
        {author_html}
    </div>
    """
    
    st.markdown(quote_html, unsafe_allow_html=True)

def tip_block(text, type="tip", title=None, icon=None):
    """
    Tworzy blok ze wskazówką, ostrzeżeniem lub informacją.
    
    Parametry:
    - text: Tekst wskazówki
    - type: Typ bloku (tip, warning, info)
    - title: Opcjonalny tytuł bloku
    - icon: Niestandardowa ikona (zastępuje domyślną ikonę)
    """
    # Używamy klas zamiast inline stylów
    css_class = f"tip-block tip-{type}"
    
    default_icon = "💡" if type == "tip" else ("⚠️" if type == "warning" else "ℹ️")
    
    # Użyj niestandardowej ikony, jeśli podana, w przeciwnym razie użyj domyślnej
    display_icon = icon if icon else default_icon
    
    # Dodaj tytuł, jeśli jest podany
    title_html = f'<div class="tip-title">{title}</div>' if title else ""
    
    tip_html = f"""
    <div class="{css_class}">
        <div class="tip-content">
            <span class="tip-icon">{display_icon}</span>
            <div>
                {title_html}
                <div>{text}</div>
            </div>
        </div>
    </div>
    """
    
    st.markdown(tip_html, unsafe_allow_html=True)

def content_section(title, content, collapsed=True, icon=None, border_color=None):
    """
    Wyświetla sekcję z treścią, wykorzystująca CSS zamiast JavaScript
    
    Parametry:
    - title: Tytuł sekcji
    - content: Treść HTML do wyświetlenia w sekcji
    - collapsed: Czy sekcja ma być domyślnie zwinięta (obecnie tylko informacyjnie)
    - icon: Emoji lub ikona do wyświetlenia obok tytułu (opcjonalne)
    - border_color: Kolor obramowania sekcji w formacie HEX (opcjonalne)
    """
    collapsed_class = "collapsed" if collapsed else ""
    icon_html = f'<span class="icon">{icon}</span>' if icon else ""
    style = f'style="border-left-color: {border_color};"' if border_color else ""
    
    section_html = f"""
    <div class="content-section {collapsed_class}" {style}>
        <div class="section-header">
            {icon_html} {title}
        </div>
        <div class="section-content">
            {content}
        </div>
    </div>
    """
    
    st.markdown(section_html, unsafe_allow_html=True)

def section_container(title=None):
    """
    Tworzy sekcję z opcjonalnym tytułem jako kontekstowy menedżer.
    
    Parametry:
    - title: Tytuł sekcji (opcjonalnie)
    
    Użycie:
    with section_container("Tytuł"):
        st.write("Zawartość")
    """
    if title:
        st.markdown(f"## {title}")
    return st.container()
