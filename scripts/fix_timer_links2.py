import os
import re

directory = r'C:\TimerHavenWebsite'

files_to_check = [f for f in os.listdir(directory) if f.startswith('timer-') and f.endswith('.html')]

count = 0
for filename in files_to_check:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Find the language code
    match = re.search(r'timer-([a-z]{2})\.html', filename)
    if match:
        lang = match.group(1)
        
        # Replace href="/timer-{lang}.html" with href="{lang}/task-timer/task-timer-index.html"
        old_href = f'href="/timer-{lang}.html"'
        new_href = f'href="{lang}/task-timer/task-timer-index.html"'
        
        content = content.replace(old_href, new_href)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Fixed link in {filename}")

print(f"Modified {count} files.")
