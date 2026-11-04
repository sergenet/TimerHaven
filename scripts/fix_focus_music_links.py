import os
import re

directory = r'C:\TimerHavenWebsite'

files_to_check = [
    'focus-music.html',
    'focus-music-en.html',
    'focus-music-es.html',
    'focus-music-fr.html',
    'focus-music-de.html',
    'focus-music-ru.html',
    'focus-music-ar.html',
    'focus-music-el.html'
]

count = 0
for filename in files_to_check:
    filepath = os.path.join(directory, filename)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace focus-music/focus-music.html with focus-music/focus-music-index.html
    new_content = re.sub(r'(focus-music)/focus-music\.html', r'\1/focus-music-index.html', content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"Fixed links in {filename}")

print(f"Fixed {count} files.")
