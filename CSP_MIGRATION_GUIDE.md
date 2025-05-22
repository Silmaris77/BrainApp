# Migracja aplikacji Neuroliderzy do zgodności z CSP

## Problem

Aplikacja Neuroliderzy zawiera liczne przypadki użycia inline JavaScript, co powoduje problemy zgodności z Content Security Policy (CSP). Polityka CSP blokuje wykonywanie skryptów inline, co prowadzi do nieprawidłowego działania aplikacji w przeglądarkach z włączonym CSP.

Główne problemy:
- Przyciski HTML z atrybutami `onclick="document.getElementById(...).click()"`
- Używanie ukrytych przycisków Streamlit aktywowanych przez JavaScript
- Inne przypadki inline JavaScript w kodzie HTML generowanym przez aplikację

## Rozwiązanie

Stworzyliśmy nowy system UI zgodny z CSP, który eliminuje potrzebę stosowania inline JavaScript. Nowy system:

1. Bezpośrednio używa komponentów Streamlit zamiast HTML+JavaScript
2. Wykorzystuje stan sesji Streamlit do kontrolowania przepływu aplikacji
3. Oferuje responsywny layout dostosowany do różnych urządzeń
4. Zapewnia spójny wygląd i zachowanie w całej aplikacji

## Zmigrowane moduły

| Stary moduł (z inline JS) | Nowy moduł (zgodny z CSP) |
|--------------------------|---------------------------|
| `admin_card_layout.py`   | `admin_ui.py`             |
| `dashboard_card_layout.py` | `dashboard_ui.py`       |
| `degen_test_card_layout.py` | `degen_test_ui.py`     |
| `lesson_card_layout.py`  | `lesson_ui.py`            |
| `neuroleader_explorer_card_layout.py` | `neuroleader_explorer_ui.py` |
| `neuroleader_test_card_layout.py` | `neuroleader_test_ui.py` |
| `profile_card_layout.py` | `profile_ui.py`           |
| `shop_card_layout.py`    | `shop_ui.py`              |
| `skills_card_layout.py`  | `skills_ui.py`            |

## Jak przetestować nowe moduły

```
python test_csp_modules.py
```

## Automatyczna migracja widoków

Uruchom skrypt automatyzujący migrację plików z card_layout na nowy system UI:

```
python migrate_views.py
```

Ten skrypt:
1. Tworzy kopię zapasową głównych plików
2. Generuje szablony plików _ui.py dla wszystkich widoków używających card_layout
3. Aktualizuje importy w main_ui.py
4. Generuje raport z migracji

## Uwagi dotyczące importów

Podczas migracji mogą pojawić się problemy z importami spowodowane różnicami w nazwach funkcji. Na przykład:

- Moduł `lesson_ui.py` próbuje importować `load_lessons_data`, ale w pliku `data.lessons.py` funkcja nazywa się `load_lessons`.

W takim przypadku można zastosować alias importu:

```python
# Zamiast
from data.lessons import load_lessons_data

# Użyj alias
from data.lessons import load_lessons as load_lessons_data
```

To podejście pozwala na kompatybilność bez konieczności modyfikowania istniejących modułów.

## Jak przeprowadzić migrację innych modułów

### 1. Zidentyfikuj problematyczny kod

Wyszukaj wszystkie wystąpienia:
- `onclick="document`
- `onclick="javascript`
- Inne przypadki generowania HTML z atrybutami `onclick`

### 2. Utwórz nowy plik UI

```python
import streamlit as st
from utils.ui import initialize_ui
from utils.ui.components.interactive import zen_button, notification
from utils.ui.components.text import content_section, zen_header
from utils.ui.layouts.grid import responsive_grid, render_dashboard_header

def show_my_module_ui():
    """
    Główna funkcja wyświetlająca UI modułu
    """
    # Inicjalizacja UI
    initialize_ui()
    
    # Nagłówek
    render_dashboard_header("Tytuł modułu", "Podtytuł")
    
    # Zawartość
    # ...
```

### 3. Zamień inline JavaScript na komponenty Streamlit

#### Stary kod z inline JavaScript:

```python
# HTML z inline JavaScript
st.markdown('''
<button class='material-button' 
    onclick="document.getElementById('btn-action').click()">
    Kliknij mnie
</button>
''', unsafe_allow_html=True)

# Ukryty przycisk
if st.button("Kliknij mnie", key="btn-action",
             label_visibility="collapsed"):
    # Logika
    pass
```

#### Nowy kod zgodny z CSP:

```python
# Import komponentów UI
from utils.ui.components.interactive import zen_button

# Bezpośredni przycisk Streamlit
if zen_button("Kliknij mnie", key="btn-action"):
    # Logika (ta sama co wcześniej)
    pass
```

### 4. Aktualizuj importy w głównej aplikacji

```python
# Stary import
# from views.module_card_layout import show_module_page

# Nowy import
from views.module_ui import show_module_ui
```

## Dostępne komponenty UI

### Komponenty interaktywne

- `zen_button` - Przycisk zgodny z CSP
- `notification` - Powiadomienia użytkownika
- `theme_selector` - Wybór motywu interfejsu

### Komponenty layoutu

- `responsive_grid` - Responsywna siatka dostosowana do urządzenia
- `render_dashboard_header` - Nagłówek dashboardu
- `render_stats_section` - Sekcja statystyk

### Komponenty tekstowe i karty

- `content_section` - Sekcja zawartości
- `zen_header` - Stylizowany nagłówek
- `stat_card` - Karta statystyk

## Dalsze kroki

1. Przetestuj nowe moduły w różnych przeglądarkach i urządzeniach
2. Zmigruj pozostałe moduły z problematycznym kodem
3. Zaktualizuj importy w głównej aplikacji
4. Przeprowadź testy wydajności i kompatybilności

## Informacje o autorach

Migracja została przeprowadzona przez zespół Neuroliderzy w maju 2025.
