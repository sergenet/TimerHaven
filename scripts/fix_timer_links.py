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

    # 1. Remove the <div class="tool-intro" id="tool-help" data-preserve="true">...</div>
    # Using regex to match from <div class="tool-intro" id="tool-help" data-preserve="true"> to the closing </div> before <a id="read-guide-btn"
    pattern = r'<div class="tool-intro"[^>]*id="tool-help"[^>]*data-preserve="true"[^>]*>.*?</div>\s*(?=<a id="read-guide-btn")'
    content = re.sub(pattern, '', content, flags=re.DOTALL)

    # 2. Fix the links to point to <lang>/task-timer/task-timer-index.html
    match = re.search(r'timer-([a-z]{2})\.html', filename)
    if match:
        lang = match.group(1)
        
        # Replace the read-guide-btn link
        pattern_btn = r'<a id="read-guide-btn"([^>]*)href="[^"]+"([^>]*)>'
        replacement_btn = f'<a id="read-guide-btn"\\1href="{lang}/task-timer/task-timer-index.html"\\2>'
        content = re.sub(pattern_btn, replacement_btn, content)
        
        # Replace the mobile-summary link
        pattern_mob = r'<div class="mobile-summary">[^<]*<a href="[^"]+">'
        replacement_mob = f'<div class="mobile-summary">Quick timer — <a href="{lang}/task-timer/task-timer-index.html">'
        content = re.sub(pattern_mob, replacement_mob, content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Fixed timer logic in {filename}")

print(f"Modified {count} files.")
