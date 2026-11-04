import os
import re

directory = r'C:\TimerHavenWebsite'
files_to_check = [f for f in os.listdir(directory) if f.endswith('.html')]

count = 0
for filename in files_to_check:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Regex to match the coming soon banner
    pattern = r'<div style="background:\s*#185a9d;\s*color:\s*#fff;\s*text-align:\s*center;\s*font-size:\s*0\.8rem;\s*padding:\s*4px;\s*font-weight:\s*500;">.*?</div>\s*'
    content = re.sub(pattern, '', content, flags=re.DOTALL)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Removed ribbon from {filename}")

print(f"Modified {count} files.")
