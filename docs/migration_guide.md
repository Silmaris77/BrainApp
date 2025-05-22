# Przewodnik migracji do nowego systemu UI

Ten dokument zawiera wytyczne i instrukcje dotyczące migracji z oryginalnego systemu komponentów UI do nowego, bardziej elastycznego systemu zgodnego z Content Security Policy (CSP).

## Spis treści

1. [Przegląd](#przegląd)
2. [Korzyści z nowego systemu](#korzyści-z-nowego-systemu)
3. [Strategia migracji](#strategia-migracji)
4. [Tryb kompatybilności wstecznej (Bridge Mode)](#tryb-kompatybilności-wstecznej-bridge-mode)
5. [Mapowanie komponentów](#mapowanie-komponentów)
6. [Przykłady migracji](#przykłady-migracji)
7. [Obsługa motywów](#obsługa-motywów)
8. [Najlepsze praktyki](#najlepsze-praktyki)

## Przegląd

Nowy system UI zostały zaprojektowany, aby:

- Zapewnić zgodność z Content Security Policy (CSP) poprzez eliminację inline JavaScript
- Usprawnić zarządzanie stylami i motywami 
- Ułatwić rozbudowę i utrzymanie komponentów
- Poprawić separację logiki od prezentacji

Cały system znajduje się w katalogu `utils/ui`.

## Korzyści z nowego systemu

- **Zgodność z CSP**: Brak inline JavaScript zwiększa bezpieczeństwo aplikacji
- **Lepsza organizacja kodu**: Modułowa struktura i separation of concerns
- **Łatwiejsze zarządzanie motywami**: Centralne zarządzanie stylami CSS
- **Responsywność**: Komponenty automatycznie dostosowują się do różnych urządzeń
- **Rozszerzalność**: Łatwe dodawanie nowych komponentów i funkcji

## Strategia migracji

Zalecamy stopniowe podejście:

1. **Wdrożenie bridge mode**: Zaimplementuj tryb kompatybilności, aby natychmiast zyskać zgodność z CSP
2. **Migracja po stronie komponentów**: Stopniowo zastępuj stare komponenty nowymi
3. **Migracja po stronie widoków**: Aktualizuj widoki jeden po drugim
4. **Usunięcie starych komponentów**: Po zakończeniu migracji usuń stare komponenty

## Tryb kompatybilności wstecznej (Bridge Mode)

Tryb kompatybilności wstecznej pozwala na stopniowe przechodzenie na nowy system UI bez konieczności jednorazowej zmiany całego kodu.

### Inicjalizacja trybu kompatybilności

```python
from utils.ui.bridge import initialize_bridge

# Na początku aplikacji
initialize_bridge()
```

### Zamiana importów

```python
# Stary import
from utils.components import degen_card, stat_card

# Nowy import z mostkowaniem
from utils.ui.bridge import bridge_degen_card as degen_card
from utils.ui.bridge import bridge_stat_card as stat_card
```

## Mapowanie komponentów

| Stary komponent | Nowy komponent | Funkcja mostkująca |
|-----------------|----------------|-------------------|
| degen_card      | skill_card     | bridge_degen_card |
| stat_card       | stat_card      | bridge_stat_card  |
| mission_card    | mission_card   | bridge_mission_card |
| lesson_card     | lesson_card    | bridge_lesson_card |
| zen_button      | zen_button     | bridge_zen_button |
| notification    | notification   | bridge_notification |
| progress_bar    | progress_bar   | bridge_progress_bar |
| content_section | content_section | bridge_content_section |
| quote_block     | quote_block    | bridge_quote_block |
| tip_block       | tip_block      | bridge_tip_block |

## Przykłady migracji

### Przykład 1: Komponent karty

Stary kod:
```python
from utils.components import degen_card

degen_card(
    title="Neurobiologia przywództwa", 
    description="Podstawy neuroprzywództwa", 
    icon="🧠", 
    progress=75
)
```

Nowy kod (z bridge):
```python
from utils.ui.bridge import bridge_degen_card

bridge_degen_card(
    title="Neurobiologia przywództwa", 
    description="Podstawy neuroprzywództwa", 
    icon="🧠", 
    progress=75
)
```

Nowy kod (bezpośredni):
```python
from utils.ui.components.cards import skill_card

skill_card(
    category="Neurobiologia przywództwa",
    progress=75,
    status="in-progress",
    icon="🧠",
    description="Podstawy neuroprzywództwa",
    completed_count=8,
    total_count=10
)
```

### Przykład 2: Nagłówek strony

Stary kod:
```python
from utils.components import zen_header

zen_header("Dashboard Neuroliderów", "Witaj w aplikacji")
```

Nowy kod:
```python
from utils.ui.layouts.grid import render_dashboard_header

render_dashboard_header("Dashboard Neuroliderów", "Witaj w aplikacji")
```

## Obsługa motywów

Nowy system pozwala na łatwe przełączanie między motywami:

```python
from utils.ui import initialize_ui, theme_selector

# Inicjalizacja z domyślnym motywem
initialize_ui()

# Wyświetlenie selektora motywów (np. w sidebarze)
with st.sidebar:
    theme_selector()
```

Dostępne motywy:
- `card_layout` - klasyczny wygląd z kartami
- `material3_layout` - wygląd zgodny z Material Design 3

## Najlepsze praktyki

1. **Inicjalizacja**: Zawsze inicjalizuj UI na początku każdego widoku
2. **Responsywność**: Używaj funkcji responsywnej siatki zamiast stałej liczby kolumn
3. **Motywy**: Pozwól użytkownikowi wybrać preferowany motyw
4. **Stopniowa migracja**: Używaj bridge mode do stopniowej migracji
5. **Testowanie**: Zawsze testuj na różnych rozmiarach ekranu

## Demonstracja komponentów

Pełna demonstracja nowego systemu UI jest dostępna w pliku `views/ui_demo.py`. Możesz uruchomić tę stronę, aby zobaczyć wszystkie dostępne komponenty w akcji.
