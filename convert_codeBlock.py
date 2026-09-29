import re
import sys

def fix_code_blocks(filename):
    """
    Konwertuje indentowane bloki kodu na markdown code blocks.
    - Zmniejsza indentację o 4 spacje
    - Przenosi { na nową linię z TAKA SAMĄ indentacją
    - Dodaje ```c++ i ```
    """
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    output_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Sprawdzaj czy linia jest indentowana 4+ spacjami (kod bez ``` markerów)
        if line.startswith('    ') and not line.strip().startswith('```'):
            # Znaleziono blok kodu - zbierz wszystkie indentowane linie
            code_block = []
            
            while i < len(lines):
                current = lines[i]
                
                # Jeśli linia jest pusta, ale następna jest indentowana - dodaj ją
                if not current.strip():
                    if i + 1 < len(lines) and lines[i + 1].startswith('    '):
                        code_block.append(current)
                        i += 1
                        continue
                    else:
                        break
                
                # Jeśli linia jest indentowana 4+ spacjami - dodaj do bloku
                if current.startswith('    '):
                    code_block.append(current)
                    i += 1
                else:
                    break
            
            # Konwertuj blok kodu
            if code_block:
                output_lines.append('```c++\n')
                
                for code_line in code_block:
                    # Usuń 4 spacje indentacji (ale zostaw resztę)
                    if code_line.startswith('    '):
                        code_line = code_line[4:]
                    
                    # Przenieś { na nową linię z TAKA SAMĄ indentacją
                    # Znajdź indentację przed {
                    match = re.match(r'^(\s*)(.+?)\s*{\s*(//.*)?$', code_line)
                    if match:
                        indent = match.group(1)
                        code_part = match.group(2).rstrip()
                        comment = match.group(3) if match.group(3) else ''
                        code_line = f"{indent}{code_part}\n{indent}{{\n"
                        if comment:
                            code_line = f"{indent}{code_part}  {comment}\n{indent}{{\n"
                    
                    output_lines.append(code_line)
                
                output_lines.append('```\n')
        else:
            # Zwykła linia - przepisz bez zmian
            output_lines.append(line)
            i += 1
    
    # Zapisz plik
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    
    print(f"✓ Plik '{filename}' został przetworzony!")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Użycie: python fix_markdown.py <plik.md>")
        sys.exit(1)
    
    filename = sys.argv[1]
    fix_code_blocks(filename)