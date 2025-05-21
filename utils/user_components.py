import streamlit as st
from utils.components import stat_card, xp_level_display

def user_stats_panel(username, avatar, degen_type, level, xp, completed_lessons=None, next_level_xp=None):
    """
    Tworzy panel z podstawowymi statystykami użytkownika.
    
    Parametry:
    - username: Nazwa użytkownika
    - avatar: Emoji awatara użytkownika
    - degen_type: Typ Degena użytkownika
    - level: Aktualny poziom użytkownika
    - xp: Aktualna ilość punktów XP
    - completed_lessons: Lista ukończonych lekcji (opcjonalna)
    - next_level_xp: Wymagane XP do następnego poziomu (opcjonalne)
    """
    
    # Bardziej profesjonalny panel profilu użytkownika
    st.markdown(f"""
    <div class="m3-profile-card">
        <div class="profile-header">
            <div class="avatar-container">
                <div class="avatar">{avatar}</div>
                <div class="level-badge">{level}</div>
            </div>
            <div class="user-info">
                <h2>{username}</h2>
                <div class="degen-type">{degen_type}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Dodajemy style CSS dla karty profilu
    st.markdown("""
    <style>
    .m3-profile-card {
        background: linear-gradient(to right, #3a7bd5, #3a6073);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        color: white;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    
    .m3-profile-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
        pointer-events: none;
    }
    
    .profile-header {
        display: flex;
        align-items: center;
    }
    
    .avatar-container {
        position: relative;
        margin-right: 20px;
    }
    
    .avatar {
        font-size: 4rem;
        width: 80px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(255,255,255,0.2);
        border-radius: 50%;
        border: 3px solid rgba(255,255,255,0.5);
    }
    
    .level-badge {
        position: absolute;
        bottom: -5px;
        right: -5px;
        background: #ff9f43;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 0.9rem;
        border: 2px solid white;
        box-shadow: 0 3px 6px rgba(0,0,0,0.16);
    }
    
    .user-info {
        flex-grow: 1;
    }
    
    .user-info h2 {
        margin: 0;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    .degen-type {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Statystyki w trzech kolumnach w osobnej karcie
    st.markdown("""
    <div class="m3-stats-card">
        <h3 class="stats-header">Twoje statystyki</h3>
        <div class="stats-divider"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Dodajemy style dla karty statystyk
    st.markdown("""
    <style>
    .m3-stats-card {
        background: white;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }
    
    .stats-header {
        margin: 0 0 10px 0;
        font-size: 1.1rem;
        color: #333;
    }
    
    .stats-divider {
        height: 1px;
        background: #eee;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
      # Statystyki w trzech kolumnach
    stats_cols = st.columns(3)
    
    with stats_cols[0]:
        stat_card("Poziom", level, icon="🏆", custom_class="m3-stat-card")
    
    with stats_cols[1]:
        stat_card("XP", xp, icon="💎", custom_class="m3-stat-card")
    
    with stats_cols[2]:
        if completed_lessons is not None:
            completed_count = len(completed_lessons) if isinstance(completed_lessons, list) else completed_lessons
            stat_card("Ukończone lekcje", completed_count, icon="📚", custom_class="m3-stat-card")
    
    # Dodajemy style dla kart statystyk
    st.markdown("""
    <style>
    .m3-stat-card {
        background: white;
        border-radius: 10px;
        padding: 16px;
        transition: all 0.3s ease;
        height: 100%;
        border-left: 4px solid var(--primary-color);
    }
    
    .m3-stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
    }
    
    .stat-icon {
        font-size: 28px;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    
    .stat-value {
        font-size: 24px;
        font-weight: 700;
        color: #333;
        margin: 5px 0;
    }
    
    .stat-label {
        color: #777;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Pasek postępu XP do następnego poziomu
    if next_level_xp is not None:
        st.markdown("""
        <div class="m3-progress-card">
            <h3 class="progress-header">Postęp poziomu</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Dodajemy style dla karty postępu
        st.markdown("""
        <style>
        .m3-progress-card {
            background: white;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-top: 10px;
        }
        
        .progress-header {
            margin: 0 0 10px 0;
            font-size: 1.1rem;
            color: #333;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Używamy ulepszony xp_level_display
        xp_level_display(xp=xp, level=level, next_level_xp=next_level_xp)
