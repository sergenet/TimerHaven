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

    # Use regex to remove the entire block from <div class="tool-intro-in-card" to <!-- END: Guide excerpt -->\s*</div>
    pattern = r'<!-- Server-rendered in-card intro \(preserved\) -->\s*<div class="tool-intro-in-card" id="tool-help" data-preserve="true">.*?<!-- END: Guide excerpt -->\s*</div>'
    
    content = re.sub(pattern, '', content, flags=re.DOTALL)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Removed intro in {filename}")
    else:
        # Maybe the comment is different? Let's try matching just the div
        pattern2 = r'<div class="tool-intro-in-card"[^>]*>.*?<!-- END: Guide excerpt -->\s*</div>'
        content = re.sub(pattern2, '', content, flags=re.DOTALL)
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1
            print(f"Removed intro (pattern 2) in {filename}")

print(f"Modified {count} files.")
