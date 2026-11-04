import os
import re

directory = r'C:\TimerHavenWebsite'

files_to_check = [f for f in os.listdir(directory) if f.startswith('unit-converter-') and f.endswith('.html')]

count = 0
for filename in files_to_check:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Replace the em-dash in the ternary operator
    # 'Number.isFinite(result) — Number(result).toFixed(precision)' -> 'Number.isFinite(result) ? Number(result).toFixed(precision)'
    content = content.replace('Number.isFinite(result) — Number(result).toFixed(precision)', 'Number.isFinite(result) ? Number(result).toFixed(precision)')

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Fixed JS syntax in {filename}")

print(f"Modified {count} files.")
