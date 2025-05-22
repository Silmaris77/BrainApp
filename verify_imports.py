import sys
import os

# Dodaj ścieżkę główną projektu do sys.path
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

try:
    from views.lesson_ui import show_lesson_content, show_lesson_summary
    print("✅ Import lesson_ui.py udany")
    
    # Importy innych modułów
    from views.shop_ui import show_shop_ui
    print("✅ Import shop_ui.py udany")
    
    from views.admin_ui import show_admin_dashboard
    print("✅ Import admin_ui.py udany")
    
    print("\nWszystkie importy działają poprawnie! Problem został naprawiony.")
    
except Exception as e:
    print(f"❌ Błąd podczas importu: {str(e)}")
    import traceback
    traceback.print_exc()
