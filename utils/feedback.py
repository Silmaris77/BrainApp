import json
import os
from datetime import datetime
import streamlit as st
from utils.notifications import show_notification
from utils.error_handling import logger

FEEDBACK_FILE = 'feedback.json'
ERROR_REPORTS_FILE = 'error_reports.json'

def save_feedback(username, feedback_type, content, rating=None):
    """Save user feedback to JSON file"""
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r') as f:
            feedback_data = json.load(f)
    else:
        feedback_data = []
    
    feedback_entry = {
        'id': len(feedback_data),
        'username': username,
        'type': feedback_type,
        'content': content,
        'rating': rating,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    feedback_data.append(feedback_entry)
    
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedback_data, f)
    
    show_notification("Dziękujemy za opinię!", "success")
    logger.info(f"Feedback received from {username}: {feedback_type}")

def report_error(username, error_type, description, steps_to_reproduce=None):
    """Save error report to JSON file"""
    if os.path.exists(ERROR_REPORTS_FILE):
        with open(ERROR_REPORTS_FILE, 'r') as f:
            error_data = json.load(f)
    else:
        error_data = []
    
    error_report = {
        'id': len(error_data),
        'username': username,
        'type': error_type,
        'description': description,
        'steps_to_reproduce': steps_to_reproduce,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 'new'
    }
    
    error_data.append(error_report)
    
    with open(ERROR_REPORTS_FILE, 'w') as f:
        json.dump(error_data, f)
    
    show_notification("Dziękujemy za zgłoszenie błędu!", "success")
    logger.info(f"Error report received from {username}: {error_type}")

def show_feedback_form():
    """Display feedback form in the sidebar"""
    with st.sidebar:
        with st.expander("📝 Podziel się opinią"):
            feedback_type = st.selectbox(
                "Typ opinii",
                ["Ogólna", "Lekcja", "Test", "Interfejs", "Sugestia"]
            )
            
            rating = st.slider(
                "Ocena (1-5)",
                min_value=1,
                max_value=5,
                value=5
            )
            
            content = st.text_area("Twoja opinia")
            
            if st.button("Wyślij opinię", use_container_width=True):
                if content:
                    save_feedback(
                        st.session_state.username,
                        feedback_type,
                        content,
                        rating
                    )
                else:
                    show_notification("Proszę wpisać treść opinii", "warning")

def show_error_report_form():
    """Display error report form"""
    with st.expander("❗ Zgłoś błąd"):
        error_type = st.selectbox(
            "Typ błędu",
            ["Błąd aplikacji", "Problem z interfejsem", "Błąd w lekcji", "Inny"]
        )
        
        description = st.text_area("Opis błędu")
        steps = st.text_area("Kroki do odtworzenia (opcjonalnie)")
        
        if st.button("Zgłoś błąd", use_container_width=True):
            if description:
                report_error(
                    st.session_state.username,
                    error_type,
                    description,
                    steps
                )
            else:
                show_notification("Proszę opisać błąd", "warning")
st.markdown("<style>div.stButton > button { margin-bottom: 5px; }</style>", unsafe_allow_html=True)