import os
import re

directory = r'C:\TimerHavenWebsite'

files_to_check = [f for f in os.listdir(directory) if f.startswith('pomodoro-') and f.endswith('.html')]

count = 0
for filename in files_to_check:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # The issue: the href currently points to "/pomodoro-en.html" (or similar).
    # It should point to "en/pomodoro-timer/pomodoro-index.html"
    
    # We will extract the lang code from the filename, e.g., "pomodoro-en.html" -> "en"
    match = re.search(r'pomodoro-([a-z]{2})\.html', filename)
    if match:
        lang = match.group(1)
        # Find the read guide button and replace its href
        # e.g., <a id="read-guide-btn" class="read-guide" href="/pomodoro-en.html" role="button" target="_self" rel="noopener">Read full guide</a>
        pattern = r'<a id="read-guide-btn" class="read-guide" href="[^"]+" role="button"'
        replacement = f'<a id="read-guide-btn" class="read-guide" href="{lang}/pomodoro-timer/pomodoro-index.html" role="button"'
        content = re.sub(pattern, replacement, content)
        
        # There's another "Read full guide" link right above it in mobile-summary:
        # <div class="mobile-summary">Pomodoro quick start — <a href="/pomodoro-en.html">Read full guide</a></div>
        pattern2 = r'<div class="mobile-summary">[^<]*<a href="[^"]+">'
        replacement2 = f'<div class="mobile-summary">Pomodoro quick start — <a href="{lang}/pomodoro-timer/pomodoro-index.html">'
        content = re.sub(pattern2, replacement2, content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Fixed read guide link in {filename}")

print(f"Modified {count} files.")
