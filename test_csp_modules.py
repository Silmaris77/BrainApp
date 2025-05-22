import streamlit as st
import sys
import os

# Dodaj ścieżkę główną projektu do sys.path
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

def test_lesson_ui():
    """
    Test dla nowego modułu lesson_ui.py
    """
    try:
        from views.lesson_ui import show_lesson_content, show_lesson_summary
        print("✅ Import lesson_ui.py udany")
        
        # Sprawdź czy funkcje mają odpowiednie sygnatury
        show_lesson_content("test_lesson")
        show_lesson_summary("test_lesson", 100, 50)
        print("✅ Funkcje z lesson_ui.py działają poprawnie")
        
        return True
    except Exception as e:
        print(f"❌ Błąd w module lesson_ui.py: {str(e)}")
        print(f"Szczegóły: {e.__class__.__name__}")
        import traceback
        traceback.print_exc()
        return False

def test_skills_ui():
    """
    Test dla nowego modułu skills_ui.py
    """
    try:
        from views.skills_ui import show_skill_tree
        print("✅ Import skills_ui.py udany")
        
        # Sprawdź czy funkcja ma odpowiednią sygnaturę
        show_skill_tree()
        print("✅ Funkcje z skills_ui.py działają poprawnie")
        
        return True
    except Exception as e:
        print(f"❌ Błąd w module skills_ui.py: {str(e)}")
        print(f"Szczegóły: {e.__class__.__name__}")
        import traceback
        traceback.print_exc()
        return False

def test_shop_ui():
    """
    Test dla nowego modułu shop_ui.py
    """
    try:
        from views.shop_ui import show_shop_ui
        print("✅ Import shop_ui.py udany")
        
        # Sprawdź czy funkcja ma odpowiednią sygnaturę
        show_shop_ui()
        print("✅ Funkcje z shop_ui.py działają poprawnie")
        
        return True
    except Exception as e:
        print(f"❌ Błąd w module shop_ui.py: {str(e)}")
        print(f"Szczegóły: {e.__class__.__name__}")
        import traceback
        traceback.print_exc()
        return False

def test_admin_ui():
    """
    Test dla istniejącego modułu admin_ui.py
    """
    try:
        from views.admin_ui import show_admin_dashboard
        print("✅ Import admin_ui.py udany")
        
        # Sprawdź czy funkcja ma odpowiednią sygnaturę
        show_admin_dashboard()
        print("✅ Funkcje z admin_ui.py działają poprawnie")
        
        return True
    except Exception as e:
        print(f"❌ Błąd w module admin_ui.py: {str(e)}")
        print(f"Szczegóły: {e.__class__.__name__}")
        import traceback
        traceback.print_exc()
        return False

def test_dashboard_ui():
    """
    Test dla nowego modułu dashboard_ui.py
    """
    try:
        from views.dashboard_ui import show_dashboard
        print("✅ Import dashboard_ui.py udany")
        
        # Sprawdź czy funkcja ma odpowiednią sygnaturę
        show_dashboard()
        print("✅ Funkcje z dashboard_ui.py działają poprawnie")
        
        return True
    except Exception as e:
        print(f"❌ Błąd w module dashboard_ui.py: {str(e)}")
        print(f"Szczegóły: {e.__class__.__name__}")
        import traceback
        traceback.print_exc()
        return False

def test_profile_ui():
    """
    Test dla nowego modułu profile_ui.py
    """
    try:
        from views.profile_ui import show_profile
        print("✅ Import profile_ui.py udany")
        
        # Sprawdź czy funkcja ma odpowiednią sygnaturę
        show_profile()
        print("✅ Funkcje z profile_ui.py działają poprawnie")
        
        return True
    except Exception as e:
        print(f"❌ Błąd w module profile_ui.py: {str(e)}")
        print(f"Szczegóły: {e.__class__.__name__}")
        import traceback
        traceback.print_exc()
        return False

def test_degen_test_ui():
    """
    Test dla nowego modułu degen_test_ui.py
    """
    try:
        from views.degen_test_ui import show_degen_test
        print("✅ Import degen_test_ui.py udany")
        
        # Sprawdź czy funkcja ma odpowiednią sygnaturę
        show_degen_test()
        print("✅ Funkcje z degen_test_ui.py działają poprawnie")
        
        return True
    except Exception as e:
        print(f"❌ Błąd w module degen_test_ui.py: {str(e)}")
        print(f"Szczegóły: {e.__class__.__name__}")
        import traceback
        traceback.print_exc()
        return False

def test_neuroleader_test_ui():
    """
    Test dla nowego modułu neuroleader_test_ui.py
    """
    try:
        from views.neuroleader_test_ui import show_neuroleader_test
        print("✅ Import neuroleader_test_ui.py udany")
        
        # Sprawdź czy funkcja ma odpowiednią sygnaturę
        show_neuroleader_test()
        print("✅ Funkcje z neuroleader_test_ui.py działają poprawnie")
        
        return True
    except Exception as e:
        print(f"❌ Błąd w module neuroleader_test_ui.py: {str(e)}")
        print(f"Szczegóły: {e.__class__.__name__}")
        import traceback
        traceback.print_exc()
        return False

def test_neuroleader_explorer_ui():
    """
    Test dla nowego modułu neuroleader_explorer_ui.py
    """
    try:
        from views.neuroleader_explorer_ui import show_neuroleader_explorer
        print("✅ Import neuroleader_explorer_ui.py udany")
        
        # Sprawdź czy funkcja ma odpowiednią sygnaturę
        show_neuroleader_explorer()
        print("✅ Funkcje z neuroleader_explorer_ui.py działają poprawnie")
        
        return True
    except Exception as e:
        print(f"❌ Błąd w module neuroleader_explorer_ui.py: {str(e)}")
        print(f"Szczegóły: {e.__class__.__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("===== Test nowych modułów UI zgodnych z CSP =====")
    print("\n1. Testowanie modułu lesson_ui.py...")
    lesson_success = test_lesson_ui()
    
    print("\n2. Testowanie modułu shop_ui.py...")
    shop_success = test_shop_ui()
    
    print("\n3. Testowanie modułu admin_ui.py...")
    admin_success = test_admin_ui()
    
    print("\n4. Testowanie modułu skills_ui.py...")
    skills_success = test_skills_ui()
    
    print("\n5. Testowanie modułu dashboard_ui.py...")
    dashboard_success = test_dashboard_ui()
    
    print("\n6. Testowanie modułu profile_ui.py...")
    profile_success = test_profile_ui()
    
    print("\n7. Testowanie modułu degen_test_ui.py...")
    degen_test_success = test_degen_test_ui()
    print("\n8. Testowanie modułu neuroleader_test_ui.py...")
    neuroleader_test_success = test_neuroleader_test_ui()
    
    print("\n9. Testowanie modułu neuroleader_explorer_ui.py...")
    neuroleader_explorer_success = test_neuroleader_explorer_ui()
    
    print("\n9. Testowanie modułu neuroleader_explorer_ui.py...")
    neuroleader_explorer_success = test_neuroleader_explorer_ui()
      # Podsumowanie
    print("\n===== Podsumowanie testów =====")
    all_success = lesson_success and shop_success and admin_success and skills_success and dashboard_success and profile_success and degen_test_success and neuroleader_test_success and neuroleader_explorer_success and neuroleader_explorer_success
    
    if all_success:
        print("✅ Wszystkie moduły zostały pomyślnie przetestowane!")
        print("Możesz teraz bezpiecznie zastąpić stare wersje plików nowymi wersjami zgodnym z CSP.")
    else:
        print("❌ Niektóre testy nie powiodły się. Sprawdź błędy powyżej.")
        
    if lesson_success:
        print("✅ lesson_ui.py - OK")
    else:
        print("❌ lesson_ui.py - BŁĄD")
    
    if shop_success:
        print("✅ shop_ui.py - OK")
    else:
        print("❌ shop_ui.py - BŁĄD")
    
    if admin_success:
        print("✅ admin_ui.py - OK")
    else:
        print("❌ admin_ui.py - BŁĄD")
        
    if skills_success:
        print("✅ skills_ui.py - OK")
    else:
        print("❌ skills_ui.py - BŁĄD")
        
    if dashboard_success:
        print("✅ dashboard_ui.py - OK")
    else:
        print("❌ dashboard_ui.py - BŁĄD")
        
    if profile_success:
        print("✅ profile_ui.py - OK")
    else:
        print("❌ profile_ui.py - BŁĄD")
        
    if degen_test_success:
        print("✅ degen_test_ui.py - OK")
    else:
        print("❌ degen_test_ui.py - BŁĄD")
    if neuroleader_test_success:
        print("✅ neuroleader_test_ui.py - OK")
    else:
        print("❌ neuroleader_test_ui.py - BŁĄD")
        
    if neuroleader_explorer_success:
        print("✅ neuroleader_explorer_ui.py - OK")
    else:
        print("❌ neuroleader_explorer_ui.py - BŁĄD")
        
    if neuroleader_explorer_success:
        print("✅ neuroleader_explorer_ui.py - OK")
    else:
        print("❌ neuroleader_explorer_ui.py - BŁĄD")
