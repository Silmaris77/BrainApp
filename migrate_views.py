import os
import re
import shutil
from datetime import datetime

def collect_card_layout_files():
    """
    Zbiera wszystkie pliki z card_layout.py do migracji
    """
    views_dir = os.path.join('views')
    card_layout_files = []
    
    for filename in os.listdir(views_dir):
        if filename.endswith('_card_layout.py'):
            base_name = filename.replace('_card_layout.py', '')
            ui_file = f"{base_name}_ui.py"
            ui_filepath = os.path.join(views_dir, ui_file)
            
            # Sprawdź, czy plik UI już istnieje
            ui_exists = os.path.exists(ui_filepath)
            
            card_layout_files.append({
                'original_file': filename,
                'ui_file': ui_file,
                'base_name': base_name,
                'ui_exists': ui_exists
            })
    
    return card_layout_files

def create_ui_templates():
    """
    Tworzy szablony plików UI na podstawie plików card_layout
    """
    card_files = collect_card_layout_files()
    views_dir = os.path.join('views')
    
    created_files = []
    skipped_files = []
    
    for file_info in card_files:
        original_path = os.path.join(views_dir, file_info['original_file'])
        ui_path = os.path.join(views_dir, file_info['ui_file'])
        
        if file_info['ui_exists']:
            skipped_files.append(file_info['ui_file'])
            continue
        
        # Wczytaj zawartość oryginalnego pliku
        with open(original_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Analizuj plik i wygeneruj szablon UI
        ui_content = generate_ui_content(content, file_info['base_name'])
        
        # Zapisz nowy plik UI
        with open(ui_path, 'w', encoding='utf-8') as f:
            f.write(ui_content)
            
        created_files.append(file_info['ui_file'])
    
    return created_files, skipped_files

def generate_ui_content(original_content, base_name):
    """
    Generuje zawartość pliku UI na podstawie oryginalnego pliku
    """
    # Znajdź importy
    import_pattern = r'import\s+.*?\n|from\s+.*?\s+import\s+.*?\n'
    imports = re.findall(import_pattern, original_content)
    
    # Znajdź główną funkcję
    main_function_pattern = r'def\s+(show_\w+)\s*\('
    main_function_match = re.search(main_function_pattern, original_content)
    main_function_name = main_function_match.group(1) if main_function_match else f"show_{base_name}"
    
    # Utwórz szablon pliku UI
    ui_template = f"""import streamlit as st
from utils.ui import initialize_ui
from utils.ui.components.interactive import zen_button, notification
from utils.ui.components.text import content_section, zen_header
from utils.ui.layouts.grid import responsive_grid, render_dashboard_header

# Oryginalne importy (dostosuj je do potrzeb)
# {''.join(imports)}

def {main_function_name}():
    \"\"\"
    Wyświetla {base_name.replace('_', ' ')} używając nowego systemu UI zgodnego z CSP
    \"\"\"
    # Inicjalizacja UI
    initialize_ui()
    
    # Nagłówek strony
    render_dashboard_header("{base_name.replace('_', ' ').title()}", "Opis funkcjonalności")
    
    # TODO: Zaimplementuj widok zgodny z CSP
    st.write("To jest nowy widok {base_name} zgodny z CSP.")
    st.write("Należy przenieść logikę z oryginalnego pliku {base_name}_card_layout.py")
    st.write("Zastąp inline JavaScript nowymi komponentami UI.")
    
    # Przykład użycia komponentów UI:
    cols = responsive_grid(columns_desktop=2, columns_tablet=1, columns_mobile=1)
    
    with cols[0]:
        st.markdown("### Lewa kolumna")
        if zen_button("Przykładowy przycisk", key="sample_button_1"):
            notification("Kliknięto przycisk!", "info")
    
    with cols[1]:
        st.markdown("### Prawa kolumna")
        st.write("Tutaj umieść więcej zawartości.")

"""
    
    return ui_template

def update_main_ui(created_files):
    """
    Aktualizuje plik main_ui.py o nowe importy
    """
    main_ui_path = os.path.join('main_ui.py')
    
    # Wczytaj plik main_ui.py
    with open(main_ui_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Podziel na sekcje
    imports_section = re.search(r'try:.*?# Importy nowych modułów zgodnych z CSP', content, re.DOTALL)
    if not imports_section:
        return False
    
    new_imports_section = content[imports_section.end():]
    new_imports_section_match = re.search(r'.*?except', new_imports_section, re.DOTALL)
    if new_imports_section_match:
        new_imports_section = new_imports_section[:new_imports_section_match.start()]
    
    # Dodaj nowe importy
    updated_imports = new_imports_section
    
    for file_info in created_files:
        base_name = file_info.replace('_ui.py', '')
        import_line = f"from views.{file_info[:-3]} import show_{base_name}\n"
        if import_line not in updated_imports:
            updated_imports += import_line
    
    # Zastąp sekcję importów
    new_content = content.replace(new_imports_section, updated_imports)
    
    # Zapisz zaktualizowany plik
    with open(main_ui_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def create_backup():
    """
    Tworzy kopię zapasową głównego pliku aplikacji
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Kopia main.py
    if os.path.exists('main.py'):
        shutil.copy2('main.py', f'main.py.bak_{timestamp}')
    
    # Kopia main_ui.py
    if os.path.exists('main_ui.py'):
        shutil.copy2('main_ui.py', f'main_ui.py.bak_{timestamp}')
    
    return timestamp

def main():
    """
    Główna funkcja migrująca widoki
    """
    print("=== Migracja widoków do zgodności z CSP ===")
    
    # Tworzenie kopii zapasowej
    timestamp = create_backup()
    print(f"✅ Utworzono kopie zapasowe z timestampem {timestamp}")
    
    # Migrowanie widoków
    created_files, skipped_files = create_ui_templates()
    
    print("\n=== Podsumowanie migracji ===")
    print(f"✅ Utworzono {len(created_files)} nowych plików UI:")
    for file in created_files:
        print(f"  - {file}")
    
    print(f"\n⏭️ Pominięto {len(skipped_files)} istniejących plików UI:")
    for file in skipped_files:
        print(f"  - {file}")
    
    if created_files:
        update_main_ui([f for f in created_files if f != 'skills_ui.py'])
        print("\n✅ Zaktualizowano importy w main_ui.py")
    
    print("\n=== Następne kroki ===")
    print("1. Edytuj wygenerowane pliki _ui.py i dostosuj je do swoich potrzeb")
    print("2. Uruchom aplikację z nowym UI: streamlit run main_ui.py")
    print("3. Upewnij się, że wszystkie funkcje działają poprawnie")

if __name__ == "__main__":
    main()
