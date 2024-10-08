import re
import string

python_keywords = {
    # Seznam klíčových slov Pythonu
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue',
    'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import',
    'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield',
    # Seznam názvů objektů a funkcí z externích knihoven, které se nebudou nahrazovat
    '__init__', '__main__', '__name__',
    'bytes', 'abs', 'int', 'max',
    'read_digital', 'write_digital', 'read_analog', 'was_pressed',
    'init', 'read', 'write', 'freq',
    'NeoPixel', 'neopixel',
    'microbit', 'i2c', 'pin0', 'pin8', 'pin12', 'pin14', 'pin15', 'button_a', 'button_b', 'sleep',
    'utime', 'ticks_ms', 'ticks_us', 'ticks_diff',
    'machine', 'time_pulse_us',
}

# Funkce pro vytvoření náhradního jména
def generate_replacement_name(index):
    letters = string.ascii_uppercase
    name = ''
    while index >= 0:
        name = letters[index % 26] + name
        index = index // 26 - 1
    return '_' + name

# Funkce pro vytvoření slovníku pro nahrazování jmen
def create_replacement_dict(file_path):
    replacement_dict = {}
    with open(file_path, 'r') as file:
        content = file.read()
        # Najdi všechny názvy tříd, proměnných a metod
        names = re.findall(r'\b[A-Za-z_][A-Za-z0-9_]*\b', content)
        # Odstraň duplikáty a seřaď
        unique_names = sorted(set(names))
        # Vytvoř slovník s náhradními jmény
        for i, name in enumerate(unique_names):
            if name not in python_keywords and len(name) > 2:
                replacement_dict[name] = generate_replacement_name(i)
        return replacement_dict

# Funkce pro nahrazení slov podle slovníku
def replace_names(line, replacement_dict):
    words = re.findall(r'\b\w+\b', line)
    for word in words:
        if word in replacement_dict and word not in python_keywords:
            line = re.sub(r'\b' + re.escape(word) + r'\b', replacement_dict[word], line)
    return line

# Funkce pro nahrazení každých 4 mezer tabulátorem
def replace_spaces_with_tabs(line):
    return line.replace(' ' * 4, '\t')

# Funkce pro odstranění poznámek
def remove_comments(content):
    # Odstranění jednořádkových poznámek
    content = re.sub(r'#.*', '', content)
    # Odstranění vícerádkových poznámek
    content = re.sub(r'\'\'\'(.*?)\'\'\'', '', content, flags=re.DOTALL)
    content = re.sub(r'\"\"\"(.*?)\"\"\"', '', content, flags=re.DOTALL)
    return content

# Vytvoření slovníku pro nahrazování jmen
input_file_path = 'input_file.py'
with open(input_file_path, 'r') as file:
    content = file.read()

# Odstranění poznámek
content = remove_comments(content)

# Vytvoření slovníku pro nahrazování jmen
replacement_dict = create_replacement_dict(input_file_path)

# Otevření vstupního a výstupního souboru
with open('output_file.py', 'w') as outfile:
    for line in content.splitlines():
        new_line = replace_names(line, replacement_dict)
        new_line = replace_spaces_with_tabs(new_line)
        outfile.write(new_line + '\n')
