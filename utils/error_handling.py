import logging
import traceback
import functools
from datetime import datetime
import streamlit as st
from utils.notifications import show_notification

# Konfiguracja logowania
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('zen_degen')

class AppError(Exception):
    """Base exception class for application errors"""
    def __init__(self, message, error_type="error"):
        self.message = message
        self.error_type = error_type
        super().__init__(self.message)

def handle_error(func):
    """Decorator for handling errors in functions"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AppError as e:
            # Pokaż użytkownikowi przyjazny komunikat
            show_notification(e.message, e.error_type)
            # Zaloguj błąd
            logger.error(f"AppError in {func.__name__}: {e.message}")
        except Exception as e:
            # Pokaż użytkownikowi ogólny komunikat
            show_notification(
                "Wystąpił nieoczekiwany błąd. Spróbuj ponownie później.",
                "error"
            )
            # Zaloguj szczegółowy błąd
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
        return None
    return wrapper

def log_action(action_type):
    """Decorator for logging user actions"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            username = st.session_state.get('username', 'anonymous')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            logger.info(
                f"Action: {action_type} | User: {username} | "
                f"Function: {func.__name__} | Time: {timestamp}"
            )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def validate_user_input(**validators):
    """
    Decorator for validating user input
    Example usage:
    @validate_user_input(
        username=lambda x: len(x) >= 3,
        password=lambda x: len(x) >= 6
    )
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for field, validator in validators.items():
                if field in kwargs:
                    value = kwargs[field]
                    if not validator(value):
                        raise AppError(
                            f"Nieprawidłowa wartość dla pola {field}",
                            "warning"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator

class ErrorBoundary:
    """Context manager for handling errors in specific sections of code"""
    def __init__(self, section_name, show_error=True):
        self.section_name = section_name
        self.show_error = show_error

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            if self.show_error:
                show_notification(
                    f"Błąd w sekcji {self.section_name}. Spróbuj ponownie.",
                    "error"
                )
            logger.error(
                f"Error in section {self.section_name}: "
                f"{exc_type.__name__}: {str(exc_value)}"
            )
            return True  # Obsłuż błąd
        return False