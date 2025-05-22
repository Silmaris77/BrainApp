import os
import re

def fix_card_layout_files():
    """Remove Material3 theme application from card layout files"""
    # Get the directory of all view files
    views_dir = os.path.join(os.path.dirname(__file__), 'views')
    
    # Pattern to find card layout files
    card_layout_pattern = r'.*_card_layout\.py$'
    
    fixed_files = []
    
    # Find all card layout files
    for filename in os.listdir(views_dir):
        if re.match(card_layout_pattern, filename):
            file_path = os.path.join(views_dir, filename)
            
            # Read the file content
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            # Go through each line looking for the apply_material3_theme() call
            new_lines = []
            found_material3 = False
            
            for line in lines:
                if re.search(r'apply_material3_theme\(\)', line):
                    found_material3 = True
                    # Skip this line to remove the function call
                    continue
                new_lines.append(line)
            
            if found_material3:
                # Write back to the file if changes were made
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.writelines(new_lines)
                
                fixed_files.append(filename)
                print(f"Removed Material3 theme from {filename}")
    
    return fixed_files

if __name__ == "__main__":
    fixed_files = fix_card_layout_files()
    print(f"\nFixed {len(fixed_files)} files:")
    for file in fixed_files:
        print(f" - {file}")
