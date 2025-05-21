# filepath: c:\Users\Anna\Dropbox\Maverick\DegApp\degenopment\data\test_questions.py
DEGEN_TYPES = {
    "Zen Degen": {
        "description": "Balansujący emocje i strategie, inwestujesz ze spokojem i uważnością.",
        "strengths": ["Zrównoważone podejście", "Kontrola emocji", "Długoterminowa wizja"],
        "challenges": ["Czasem zbyt ostrożny", "Może przegapiać okazje wymagające szybkiej decyzji"],
        "strategy": "Połącz medytację z analizą techniczną. Twórz zrównoważone portfolio z elementami wysokiego ryzyka.",
        "color": "#3498db"
    },
    "YOLO Degen": {
        "description": "Stawiasz wszystko na jedną kartę, podejmując decyzje bez zastanowienia, traktujesz inwestowanie jak grę.",
        "strengths": ["Szybkie działanie", "Odwaga i spontaniczność", "Wykorzystywanie okazji"],
        "challenges": ["Nadmierna impulsywność", "Ignorowanie ryzyka", "Brak długoterminowego planu"],
        "strategy": "Ustal konkretne limity ryzyka. Przeznacz maksymalnie 10% portfolio na impulsywne decyzje.",
        "color": "#e74c3c"
    },
    "Emo Degen": {
        "description": "Działasz pod wpływem emocji takich jak strach, euforia czy panika, Twoje decyzje są często impulsywne.",
        "strengths": ["Wrażliwość na nastroje rynku", "Intuicja", "Zaangażowanie emocjonalne"],
        "challenges": ["Panika przy spadkach", "Kupowanie na szczytach", "Brak kontroli nad emocjami"],
        "strategy": "Prowadź dziennik emocji. Wprowadź zasadę 24h oczekiwania przed ważną decyzją.",
        "color": "#f39c12"
    },
    "Strategist Degen": {
        "description": "Działasz według planu i strategii, analizując wszystkie kroki przed podjęciem decyzji.",
        "strengths": ["Zorganizowanie", "Konsekwencja", "Długoterminowa wizja"],
        "challenges": ["Mniejsza elastyczność", "Trudność w adaptacji do nagłych zmian", "Czasem zbyt ostrożny"],
        "strategy": "Regularnie weryfikuj swoje założenia. Zarezerwuj część portfolio na testy nowych strategii.",
        "color": "#27ae60"
    },
    "Mad Scientist Degen": {
        "description": "Testujesz innowacyjne podejścia i modele, eksperymentując z nowymi teoriami inwestycyjnymi.",
        "strengths": ["Kreatywność", "Innowacyjność", "Analityczne myślenie"],
        "challenges": ["Paraliż analityczny", "Nadmierne teoretyzowanie", "Trudności w realizacji"],
        "strategy": "Ustal czas na analizę i moment decyzji. Testuj swoje hipotezy na małej części portfolio.",
        "color": "#9b59b6"
    },
    "Spreadsheet Degen": {
        "description": "Kochasz dane i liczby, wszystko analizujesz w arkuszach kalkulacyjnych przed podjęciem decyzji.",
        "strengths": ["Dokładność", "Metodyczność", "Działanie oparte na danych"],
        "challenges": ["Przeciążenie danymi", "Ignorowanie intuicji", "Trudność w szybkim reagowaniu"],
        "strategy": "Uprość swoje modele. Zrównoważ analizę z intuicją i doświadczeniem rynkowym.",
        "color": "#2980b9"
    },
    "Meta Degen": {
        "description": "Analizujesz szerszy kontekst, trendy globalne i powiązania między różnymi rynkami.",
        "strengths": ["Szerokie spojrzenie", "Rozumienie globalnych zależności", "Długoterminowa wizja"],
        "challenges": ["Pomijanie szczegółów", "Trudność w wyczuciu krótkiego terminu", "Abstrakcyjne podejście"],
        "strategy": "Połącz analizę makro z mikro. Regularnie weryfikuj swoje założenia w zderzeniu z realnymi danymi.",
        "color": "#16a085"
    },
    "Hype Degen": {
        "description": "Śledzisz trendy i popularne tematy, inwestujesz w to, co obecnie jest na topie w mediach społecznościowych.",
        "strengths": ["Znajdowanie nowych trendów", "Szybkość działania", "Wyczucie nastrojów społecznych"],
        "challenges": ["Podążanie za tłumem", "Brak własnej analizy", "Inwestowanie na szczytach popularności"],
        "strategy": "Weryfikuj trendy własnymi badaniami. Ustal limit inwestycji w popularne tematy.",
        "color": "#e67e22"
    }
}

TEST_QUESTIONS = [
    {
        "question": "Jak reagujesz, gdy cena aktywa gwałtownie wzrasta?",
        "options": [
            {"text": "Natychmiast kupuję, nie analizując zbyt dużo.", "scores": {"YOLO Degen": 3, "Hype Degen": 1}},
            {"text": "Zastanawiam się, czy to zgodne z moją strategią.", "scores": {"Strategist Degen": 3}},
            {"text": "Czuję euforię i szybko kupuję.", "scores": {"Emo Degen": 3, "YOLO Degen": 1}},
            {"text": "Czekam na spokojniejszy moment na rynku.", "scores": {"Zen Degen": 3}},
            {"text": "Analizuję dane, by przewidzieć kolejny ruch.", "scores": {"Mad Scientist Degen": 3, "Spreadsheet Degen": 1}},
            {"text": "Sprawdzam dane historyczne i ryzyko.", "scores": {"Spreadsheet Degen": 3, "Strategist Degen": 1}},
            {"text": "Analizuję kontekst i większy trend.", "scores": {"Meta Degen": 3}},
            {"text": "Kupuję, bo widzę, że wszyscy o tym mówią.", "scores": {"Hype Degen": 3, "YOLO Degen": 1}}
        ]
    },
    {
        "question": "Co robisz, gdy rynek zaczyna się zmieniać w sposób nieprzewidywalny?",
        "options": [
            {"text": "Działam natychmiast  instynkt to podstawa.", "scores": {"YOLO Degen": 3, "Emo Degen": 1}},
            {"text": "Analizuję dane, zanim coś zrobię.", "scores": {"Strategist Degen": 3, "Spreadsheet Degen": 1}},
            {"text": "Wpadam w panikę, sprzedaję wszystko.", "scores": {"Emo Degen": 3}},
            {"text": "Zachowuję spokój, nic nie zmieniam.", "scores": {"Zen Degen": 3}},
            {"text": "Tworzę własny model predykcyjny.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Odświeżam arkusze z analizami.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Szukam głębszego sensu zmian.", "scores": {"Meta Degen": 3}},
            {"text": "Reaguję tak, jak społeczność Twittera.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak często zmieniasz swoje decyzje inwestycyjne?",
        "options": [
            {"text": "Ciągle  każda okazja to nowy ruch.", "scores": {"YOLO Degen": 3, "Hype Degen": 1}},
            {"text": "Tylko gdy plan tego wymaga.", "scores": {"Strategist Degen": 3}},
            {"text": "Za każdym razem, gdy się zestresuję.", "scores": {"Emo Degen": 3}},
            {"text": "Prawie nigdy  spokój to podstawa.", "scores": {"Zen Degen": 3}},
            {"text": "Kiedy dane dają zielone światło.", "scores": {"Mad Scientist Degen": 3, "Spreadsheet Degen": 1}},
            {"text": "Gdy model pokazuje, że to uzasadnione.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "W rytmie zmian rynkowych i geopolitycznych.", "scores": {"Meta Degen": 3}},
            {"text": "Gdy coś trenduje  wchodzę!", "scores": {"Hype Degen": 3, "YOLO Degen": 1}}
        ]
    },
    {
        "question": "Jak wygląda Twoje poranne podejście do inwestowania?",
        "options": [
            {"text": "Włączam aplikację i kupuję na ślepo.", "scores": {"YOLO Degen": 3}},
            {"text": "Sprawdzam moją strategię i wykonuję plan.", "scores": {"Strategist Degen": 3}},
            {"text": "Sprawdzam nastroje i kieruję się emocjami.", "scores": {"Emo Degen": 3}},
            {"text": "Medytuję, zanim podejmę decyzję.", "scores": {"Zen Degen": 3}},
            {"text": "Odpalam skrypty z analizami.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Aktualizuję swój Excel z danymi.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Przeglądam światowe wydarzenia.", "scores": {"Meta Degen": 3}},
            {"text": "Sprawdzam TikToka i Twittera.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak się czujesz, gdy Twoja inwestycja traci na wartości?",
        "options": [
            {"text": "Trudno, YOLO  lecę dalej.", "scores": {"YOLO Degen": 3}},
            {"text": "To część planu, mam to pod kontrolą.", "scores": {"Strategist Degen": 3}},
            {"text": "Jestem załamany, nie mogę spać.", "scores": {"Emo Degen": 3}},
            {"text": "Akceptuję to. Taki jest rynek.", "scores": {"Zen Degen": 3}},
            {"text": "Analizuję, dlaczego tak się stało.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Aktualizuję plik i zmieniam parametry.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Sprawdzam, czy to nie wynik globalnych trendów.", "scores": {"Meta Degen": 3}},
            {"text": "Obwiniam influencerów z internetu.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak wybierasz projekt lub spółkę do inwestycji?",
        "options": [
            {"text": "Klikam w to, co akurat wygląda fajnie.", "scores": {"YOLO Degen": 3}},
            {"text": "Szukam zgodności z moją strategią.", "scores": {"Strategist Degen": 3}},
            {"text": "Wybieram to, co wzbudza emocje.", "scores": {"Emo Degen": 3}},
            {"text": "Wybieram intuicyjnie, po przemyśleniu.", "scores": {"Zen Degen": 3}},
            {"text": "Patrzę na technologię i innowacyjność.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Analizuję wskaźniki i liczby.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Czytam białą księgę i analizuję ekosystem.", "scores": {"Meta Degen": 3}},
            {"text": "To, co trenduje na socialach.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak planujesz swoje portfolio?",
        "options": [
            {"text": "Nie planuję  pełen spontan.", "scores": {"YOLO Degen": 3}},
            {"text": "Mam rozpisany plan i cel.", "scores": {"Strategist Degen": 3}},
            {"text": "Dodaję i usuwam po impulsie.", "scores": {"Emo Degen": 3}},
            {"text": "Portfolio to droga  zmienia się naturalnie.", "scores": {"Zen Degen": 3}},
            {"text": "Symuluję wiele scenariuszy.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Optymalizuję strukturę w arkuszu kalkulacyjnym.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Układam pod mega trendy i narracje.", "scores": {"Meta Degen": 3}},
            {"text": "Kupuję to, co polecają inni.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Co robisz w dniu dużej korekty rynkowej?",
        "options": [
            {"text": "Wchodzę all-in w dołku.", "scores": {"YOLO Degen": 3}},
            {"text": "Trzymam się planu.", "scores": {"Strategist Degen": 3}},
            {"text": "Wpadam w panikę i wyprzedaję.", "scores": {"Emo Degen": 3}},
            {"text": "Obserwuję i nie działam pochopnie.", "scores": {"Zen Degen": 3}},
            {"text": "Weryfikuję modele i dane.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Uaktualniam wyceny i alokację.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Szacuję konsekwencje makroekonomiczne.", "scores": {"Meta Degen": 3}},
            {"text": "Patrzę co robią znani YouTuberzy.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jaki jest Twój ulubiony sposób zdobywania wiedzy o inwestowaniu?",
        "options": [
            {"text": "Z memów i shortów.", "scores": {"YOLO Degen": 3}},
            {"text": "Z książek i analiz.", "scores": {"Strategist Degen": 3}},
            {"text": "Z podcastów o sukcesach i porażkach.", "scores": {"Emo Degen": 3}},
            {"text": "Z doświadczenia i uważności.", "scores": {"Zen Degen": 3}},
            {"text": "Z badań naukowych.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Z raportów i arkuszy.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Z rozmów i debat o przyszłości.", "scores": {"Meta Degen": 3}},
            {"text": "Z komentarzy pod filmami influencerów.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak oceniasz sukces swojej inwestycji?",
        "options": [
            {"text": "Czy zrobiłem szybki zysk?", "scores": {"YOLO Degen": 3}},
            {"text": "Czy osiągnąłem cel zgodnie z planem?", "scores": {"Strategist Degen": 3}},
            {"text": "Czy poczułem się z tym dobrze?", "scores": {"Emo Degen": 3}},
            {"text": "Czy nie cierpiałem w procesie?", "scores": {"Zen Degen": 3}},
            {"text": "Czy moja hipoteza się potwierdziła?", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Czy ROI było zgodne z kalkulacją?", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Czy wpisało się to w większy trend?", "scores": {"Meta Degen": 3}},
            {"text": "Czy znajomi byli pod wrażeniem?", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak podejmujesz decyzję o sprzedaży aktywów?",
        "options": [
            {"text": "Sprzedaję wszystko nagle, gdy tylko czuję się zagrożony.", "scores": {"Emo Degen": 3}},
            {"text": "Sprzedaję tylko wtedy, gdy osiągnę planowany cel.", "scores": {"Strategist Degen": 3}},
            {"text": "Sprzedaję od razu po dużym wzroście  lepiej nie ryzykować.", "scores": {"YOLO Degen": 3}},
            {"text": "Sprzedaję spokojnie i bez emocji, zgodnie z filozofią spokoju.", "scores": {"Zen Degen": 3}},
            {"text": "Tworzę modele ryzyka i podejmuję decyzję na podstawie wyników.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Najpierw aktualizuję dane, potem analizuję.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Próbuję przewidzieć przyszłość rynku i na tej podstawie decyduję.", "scores": {"Meta Degen": 3}},
            {"text": "Sprzedaję, gdy widzę, że wszyscy to robią.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Co motywuje Cię najbardziej do inwestowania?",
        "options": [
            {"text": "Możliwość zysku tu i teraz.", "scores": {"YOLO Degen": 3}},
            {"text": "Realizacja długoterminowej strategii.", "scores": {"Strategist Degen": 3}},
            {"text": "Emocje  ekscytacja, adrenalina.", "scores": {"Emo Degen": 3}},
            {"text": "Praktyka spokoju i cierpliwości.", "scores": {"Zen Degen": 3}},
            {"text": "Chęć przetestowania własnych hipotez.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Obliczenia pokazujące potencjalny zwrot.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Wiara w przełomowe technologie.", "scores": {"Meta Degen": 3}},
            {"text": "Trendy, memy, hype i to, co popularne.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Co robisz po udanej inwestycji?",
        "options": [
            {"text": "Czuję euforię i szukam kolejnej szansy!", "scores": {"Emo Degen": 3}},
            {"text": "Analizuję, czy było to zgodne z planem.", "scores": {"Strategist Degen": 3}},
            {"text": "Wypłacam zyski i idę dalej  YOLO.", "scores": {"YOLO Degen": 3}},
            {"text": "Praktykuję wdzięczność i pozostaję spokojny.", "scores": {"Zen Degen": 3}},
            {"text": "Zapisuję dane i aktualizuję model.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Zastanawiam się, jak to powtórzyć na poziomie systemowym.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Snuję wizje przyszłości i szukam czegoś jeszcze bardziej innowacyjnego.", "scores": {"Meta Degen": 3}},
            {"text": "Chwalę się znajomym  niech wiedzą!", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Co robisz, gdy masz zainwestować większą sumę?",
        "options": [
            {"text": "Wchodzę od razu, bez zastanowienia.", "scores": {"YOLO Degen": 3}},
            {"text": "Sprawdzam, czy to pasuje do mojego planu i alokacji.", "scores": {"Strategist Degen": 3}},
            {"text": "Waham się, analizuję i w końcu nic nie robię.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Medytuję, a potem podejmuję decyzję w zgodzie ze sobą.", "scores": {"Zen Degen": 3}},
            {"text": "Ekscytuję się, ale potem się boję i działam impulsywnie.", "scores": {"Emo Degen": 3}},
            {"text": "Tworzę pełną analizę w Excelu, zanim zrobię cokolwiek.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Zastanawiam się, jak ta inwestycja wpisuje się w przyszłość.", "scores": {"Meta Degen": 3}},
            {"text": "Wpisuję nazwę aktywa w Google Trends i Twittera.", "scores": {"Hype Degen": 3}}
        ]
    }
]
