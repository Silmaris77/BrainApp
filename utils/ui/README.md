# System UI Neuroliderzy App

## Przegląd

Ten system UI został zaprojektowany jako część aplikacji Neuroliderzy (dawniej ZenDegenAcademy) z myślą o zgodności z Content Security Policy (CSP) oraz łatwiejszej modyfikacji i rozszerzaniu interfejsu użytkownika.

## Struktura katalogów

```
utils/
  ├── ui/
  │   ├── __init__.py          # Główny plik inicjalizacyjny
  │   ├── bridge.py            # Komponenty kompatybilności wstecznej
  │   ├── components/          # Komponenty UI
  │   │   ├── cards.py         # Karty (stat_card, skill_card, itd.)
  │   │   ├── interactive.py   # Komponenty interaktywne (przyciski, powiadomienia)
  │   │   └── text.py          # Komponenty tekstowe (nagłówki, cytaty, wskazówki)
  │   ├── layouts/             # Układy i struktury layoutu
  │   │   └── grid.py          # Układy siatkowe i responsywne
  │   └── theme_manager.py     # Zarządzanie motywami
  └── components.py            # Stare komponenty (do stopniowej migracji)
  
static/
  └── css/
      └── themes/              # Pliki CSS motywów
          ├── card_layout.css  # Motyw oparty na kartach
          └── material3_layout.css  # Motyw zgodny z Material Design 3
          
docs/
  └── migration_guide.md       # Przewodnik migracji ze starego do nowego systemu UI
  
views/
  ├── ui_demo.py               # Demonstracja nowego systemu UI
  ├── ui_comparison.py         # Porównanie starych i nowych komponentów
  └── dashboard_example.py     # Przykład implementacji nowego systemu UI
```

## Główne cechy

1. **Eliminacja inline JavaScript** - wszystkie komponenty są zgodne z Content Security Policy (CSP)
2. **System motywów** - łatwa zmiana wyglądu aplikacji bez modyfikacji kodu
3. **Responsive design** - automatyczne dostosowanie do różnych urządzeń
4. **Kompatybilność wsteczna** - tryb bridge umożliwiający stopniową migrację
5. **Modułowa struktura** - łatwe rozszerzanie systemu o nowe komponenty

## Jak zacząć

### Inicjalizacja systemu UI

```python
from utils.ui import initialize_ui

# Na początku każdego widoku
initialize_ui()
```

### Używanie komponentów

```python
from utils.ui.components.cards import stat_card, skill_card
from utils.ui.components.text import zen_header
from utils.ui.layouts.grid import render_dashboard_header, responsive_grid

# Nagłówek strony
render_dashboard_header("Dashboard Neuroliderera", "Witaj w aplikacji!")

# Responsywna siatka
columns = responsive_grid(columns_desktop=3, columns_tablet=2, columns_mobile=1)

with columns[0]:
    stat_card("🧠", "24", "Ukończone lekcje")
```

### Wybór motywu

```python
from utils.ui import theme_selector

# Dodaj do sidebara
with st.sidebar:
    theme_selector()
```

## Migracja ze starego systemu

System zawiera funkcje bridge, które ułatwiają stopniową migrację ze starego systemu UI do nowego:

```python
# Stary import
from utils.components import degen_card

# Zastąp:
from utils.ui.bridge import bridge_degen_card as degen_card
```

Szczegółowy przewodnik migracji znajduje się w pliku `docs/migration_guide.md`.

## Demonstracja

Aby zobaczyć wszystkie dostępne komponenty, uruchom:

```
streamlit run views/ui_demo.py
```

Aby porównać stare i nowe komponenty obok siebie:

```
streamlit run views/ui_comparison.py
```

## Przykład implementacji

Przykład implementacji nowego systemu UI w prawdziwym widoku:

```
streamlit run views/dashboard_example.py
```
