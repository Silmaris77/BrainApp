import streamlit as st

# Page configuration
PAGE_CONFIG = {
    "page_title": "DegApp",  # zakładam, że to są aktualne ustawienia
    "page_icon": "🧠",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "menu_items": {
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
}

# XP levels configuration
XP_LEVELS = {
    1: 0,
    2: 100,
    3: 250,
    4: 500,
    5: 1000,
    6: 2000,
    7: 3500,
    8: 5000,
    9: 7500,
    10: 10000
}

# CSS styles moved to static/css/style.css
# This variable is kept for backward compatibility
APP_STYLES = """
<style>
    /* CSS styles are now in static/css/style.css */
    /* This is kept for backward compatibility */
</style>
"""

# Daily missions configuration
DAILY_MISSIONS = [
    {"title": "Medytacja mindfulness", "description": "Wykonaj 10-minutową medytację uważności", "xp": 50, "badge": "🧘‍♂️"},
    {"title": "Analiza rynku", "description": "Przeanalizuj jeden projekt/token przez 30 minut", "xp": 70, "badge": "📊"},
    {"title": "Przegląd portfela", "description": "Dokonaj przeglądu swojego portfela i strategii", "xp": 60, "badge": "💼"},
    {"title": "Dziennik inwestora", "description": "Zapisz swoje decyzje i emocje z dzisiejszego dnia", "xp": 40, "badge": "📓"},
    {"title": "Nowa wiedza", "description": "Przeczytaj artykuł/raport o rynku lub psychologii inwestowania", "xp": 30, "badge": "🧠"}
]

# User avatar options
USER_AVATARS = {
    "default": "👤",
    "zen": "🧘‍♂️",
    "yolo": "🚀",
    "emo": "😭",
    "strategist": "🎯",
    "scientist": "🔬",
    "spreadsheet": "📊",
    "meta": "🔄",
    "hype": "📣"
}

# Theme options
THEMES = {
    "default": {
        "primary": "#2980B9",
        "secondary": "#6DD5FA",
        "accent": "#27ae60",
        "background": "#f7f7f7",
        "card": "#ffffff"
    },
    "dark": {
        "primary": "#3498db",
        "secondary": "#2c3e50",
        "accent": "#e74c3c",
        "background": "#1a1a1a",
        "card": "#2d2d2d"
    },
    "zen": {
        "primary": "#4CAF50",
        "secondary": "#8BC34A",
        "accent": "#009688",
        "background": "#f9f9f9",
        "card": "#ffffff"
    },
    "yolo": {
        "primary": "#FF5722",
        "secondary": "#FF9800",
        "accent": "#FFEB3B",
        "background": "#f5f5f5",
        "card": "#ffffff"
    },
    "emo": {
        "primary": "#9C27B0",
        "secondary": "#673AB7",
        "accent": "#E91E63",
        "background": "#f0f0f0",
        "card": "#ffffff"
    }
}

# Degen types
DEGEN_TYPES = {
    "Zen Degen": {
        "icon": "🧘", 
        "color": "#4CAF50", 
        "theme": "zen", 
        "description": "Dąży do równowagi i spokoju nawet w zmiennych warunkach rynkowych. Kontroluje emocje i podejmuje świadome decyzje.",
        "strengths": ["Spokój i kontrola nad emocjami", "Świadome podejmowanie decyzji", "Odporność na wahania rynku"],
        "challenges": ["Może być zbyt ostrożny", "Czasem trudno mu wykorzystać nagłe okazje", "Może przeoczyć niektóre trendy"],
        "strategy": "Długoterminowe strategie oparte na solidnej analizie fundamentalnej i zrównoważonym podejściu do ryzyka."
    },
    "YOLO Degen": {
        "icon": "🚀", 
        "color": "#FF5722", 
        "theme": "yolo", 
        "description": "Dynamiczny inwestor kierujący się intuicją i chęcią maksymalizacji zysków. Nie boi się podejmować ryzykownych decyzji.",
        "strengths": ["Szybkie podejmowanie decyzji", "Zdolność dostrzegania nowych okazji", "Odwaga i determinacja"],
        "challenges": ["Podatność na działanie pod wpływem emocji", "Ryzyko dużych strat", "Brak długoterminowej strategii"],
        "strategy": "Strategia bazująca na szybkich decyzjach i wykorzystywaniu krótkoterminowych trendów. Wymaga dyscypliny w zarządzaniu ryzykiem."
    },
    "Emo Degen": {
        "icon": "😭", 
        "color": "#9C27B0", 
        "theme": "emo", 
        "description": "Inwestor silnie reagujący emocjonalnie na zmiany rynkowe. Intensywnie przeżywa zarówno zyski jak i straty.",
        "strengths": ["Entuzjazm i zaangażowanie", "Umiejętność szybkiej adaptacji", "Intuicja społeczna"],
        "challenges": ["Decyzje pod wpływem strachu lub euforii", "Trudności z trzymaniem się planu", "Stres związany z inwestowaniem"],
        "strategy": "Strukturyzowane podejście z określonymi punktami wejścia i wyjścia, połączone z technikami zarządzania emocjami."
    },
    "Strategist Degen": {
        "icon": "🎯", 
        "color": "#3F51B5", 
        "theme": "default", 
        "description": "Planujący inwestor, który opracowuje dokładne strategie i trzyma się ich. Działa zgodnie z planem i ustalonymi celami.",
        "strengths": ["Metodyczne podejście", "Dyscyplina i konsekwencja", "Jasno określone cele"],
        "challenges": ["Brak elastyczności", "Może przeoczyć spontaniczne okazje", "Czasem zbyt przywiązany do teorii"],
        "strategy": "Precyzyjnie zdefiniowane strategie z jasnymi zasadami wejścia i wyjścia, regularnie weryfikowane i optymalizowane."
    },
    "Mad Scientist Degen": {
        "icon": "🔬", 
        "color": "#009688", 
        "theme": "default", 
        "description": "Eksperymentujący inwestor, który testuje nowe podejścia i teorie. Lubi badać niestandardowe rozwiązania i innowacje.",
        "strengths": ["Innowacyjność", "Analityczne myślenie", "Odkrywanie niewykorzystanych możliwości"],
        "challenges": ["Ryzyko nietestowanych strategii", "Skomplikowane podejście", "Nadmierne teoretyzowanie"],
        "strategy": "Eksperymentowanie z innowacyjnymi podejściami, przy jednoczesnym zarządzaniu ryzykiem poprzez alokację kapitału w sposób kontrolowany."
    },
    "Spreadsheet Degen": {
        "icon": "📊", 
        "color": "#795548", 
        "theme": "default", 
        "description": "Inwestor opierający decyzje na danych i analizach. Tworzy szczegółowe modele i kalkulacje przed każdą decyzją.",
        "strengths": ["Podejście bazujące na danych", "Dokładna analiza", "Ograniczenie wpływu emocji"],
        "challenges": ["Analiza paraliżująca", "Pomijanie czynników jakościowych", "Czasem przesadny perfekcjonizm"],
        "strategy": "Strategie oparte na modelach matematycznych, analizie danych i wskaźnikach technicznych, z regularną weryfikacją założeń."
    },
    "Meta Degen": {
        "icon": "🔄", 
        "color": "#607D8B", 
        "theme": "default", 
        "description": "Inwestor analizujący swoje własne procesy myślowe i decyzyjne. Ciągle doskonali swoje podejście i uczy się na błędach.",
        "strengths": ["Samoświadomość", "Ciągłe doskonalenie", "Adaptacyjność"],
        "challenges": ["Nadmierna autorefleksja", "Trudności z podjęciem decyzji", "Zbyt częste zmiany strategii"],
        "strategy": "Podejście adaptacyjne, łączące różne style inwestowania w zależności od okoliczności, z naciskiem na ciągłe uczenie się."
    },
    "Hype Degen": {
        "icon": "📣", 
        "color": "#FFC107", 
        "theme": "default", 
        "description": "Inwestor podążający za popularnymi trendami i projektami. Bardzo aktywny w mediach społecznościowych i śledzący opinie influencerów.",
        "strengths": ["Wczesne wykrywanie trendów", "Znajomość nastrojów społeczności", "Szybka reakcja na nowe projekty"],
        "challenges": ["Podatność na manipulacje", "FOMO (strach przed pominięciem)", "Brak własnej analizy"],
        "strategy": "Śledzenie trendów społecznościowych z jednoczesnym zachowaniem krytycznego myślenia i weryfikacją informacji z wielu źródeł."
    }
}

# Achievement badges
BADGES = {
    "starter": {"name": "Początkujący", "icon": "🌱", "description": "Rozpocznij swoją przygodę w Zen Degen Academy"},
    "tester": {"name": "Odkrywca", "icon": "🔍", "description": "Wykonaj test i odkryj swój typ degena"},
    "learner": {"name": "Uczeń", "icon": "📚", "description": "Ukończ pierwszą lekcję"},
    "consistent": {"name": "Konsekwentny", "icon": "📆", "description": "Zaloguj się 5 dni z rzędu"},
    "social": {"name": "Społecznik", "icon": "🤝", "description": "Podziel się swoim wynikiem testu"},
    "zen_master": {"name": "Mistrz Zen", "icon": "🧘‍♂️", "description": "Ukończ wszystkie lekcje z kategorii Mindfulness"},
    "market_pro": {"name": "Analityk Rynku", "icon": "📊", "description": "Ukończ wszystkie lekcje z kategorii Analiza Rynku"},
    "strategy_guru": {"name": "Guru Strategii", "icon": "🎯", "description": "Stwórz i zapisz własną strategię inwestycyjną"},
    
    # Nowe odznaki związane z aktywnością
    "streak_master": {"name": "Mistrz Serii", "icon": "🔥", "description": "Utrzymaj 10-dniową serię logowania"},
    "daily_hero": {"name": "Bohater Dnia", "icon": "⭐", "description": "Ukończ wszystkie misje dzienne w jeden dzień"},
    "weekend_warrior": {"name": "Wojownik Weekendu", "icon": "🏆", "description": "Ucz się regularnie przez 4 weekendy z rzędu"},
    
    # Odznaki związane z postępem nauki
    "knowledge_addict": {"name": "Głodny Wiedzy", "icon": "🤓", "description": "Spędź łącznie 10 godzin na nauce w aplikacji"},
    "quick_learner": {"name": "Szybki Uczeń", "icon": "⚡", "description": "Ukończ 3 lekcje w jeden dzień"},
    "night_owl": {"name": "Nocna Sowa", "icon": "🦉", "description": "Ukończ lekcję po godzinie 22:00"},
    "early_bird": {"name": "Ranny Ptaszek", "icon": "🐦", "description": "Ukończ lekcję przed godziną 8:00"},
    
    # Odznaki społecznościowe
    "mentor": {"name": "Mentor", "icon": "👨‍🏫", "description": "Pomóż innemu użytkownikowi ukończyć trudną lekcję"},
    "networker": {"name": "Networker", "icon": "🌐", "description": "Dołącz do 3 grup dyskusyjnych w aplikacji"},
    "influencer": {"name": "Influencer", "icon": "🎭", "description": "Uzyskaj 10 polubień dla swojego postu w społeczności"},
    
    # Odznaki za osiągnięcia
    "first_achievement": {"name": "Początek Drogi", "icon": "🏁", "description": "Zdobądź pierwsze osiągnięcie"},
    "collector": {"name": "Kolekcjoner", "icon": "🧩", "description": "Odblokuj 10 różnych odznak"},
    "perfectionist": {"name": "Perfekcjonista", "icon": "💯", "description": "Uzyskaj 100% w quizie z dowolnej lekcji"},
    
    # Odznaki degen typeów
    "degen_master": {"name": "Mistrz Degenów", "icon": "👑", "description": "Poznaj wszystkie typy degenów w eksploratorze"},
    "self_aware": {"name": "Samoświadomy", "icon": "🔮", "description": "Wykonaj ponownie test typu i potwierdź swój profil"},
    "identity_shift": {"name": "Przemiana", "icon": "🦋", "description": "Zmień swój główny typ degena poprzez rozwój nowych umiejętności"},
    
    # Odznaki ekonomiczne
    "saver": {"name": "Oszczędny", "icon": "💰", "description": "Zgromadź 1000 DegenCoins"},
    "big_spender": {"name": "Rozrzutny", "icon": "💸", "description": "Wydaj 2000 DegenCoins w sklepie"},
    "collector_premium": {"name": "Kolekcjoner Premium", "icon": "✨", "description": "Odblokuj wszystkie awatary dostępne w sklepie"},
    
    # Odznaki wyzwań
    "challenge_accepted": {"name": "Wyzwanie Przyjęte", "icon": "🎯", "description": "Ukończ pierwsze wyzwanie tygodniowe"},
    "challenge_master": {"name": "Mistrz Wyzwań", "icon": "🏅", "description": "Ukończ 5 wyzwań tygodniowych"},
    "seasonal_champion": {"name": "Mistrz Sezonu", "icon": "🏆", "description": "Ukończ wszystkie wyzwania sezonowe"}
}