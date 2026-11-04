import os
import re

directory = r'C:\TimerHavenWebsite'

files_to_check = [f for f in os.listdir(directory) if f.startswith('meeting-planner-') and f.endswith('.html')]

count = 0
for filename in files_to_check:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Remove sel.style.position = 'absolute';
    content = re.sub(r"sel\.style\.position = 'absolute';", "", content)
    # Remove sel.style.position = '';
    content = re.sub(r"sel\.style\.position = '';", "", content)
    # Remove sel.style.zIndex = '999';
    content = re.sub(r"sel\.style\.zIndex = '999';", "", content)

    # Remove orgSel.style.position = 'absolute';
    content = re.sub(r"orgSel\.style\.position = 'absolute';", "", content)
    # Remove orgSel.style.position = '';
    content = re.sub(r"orgSel\.style\.position = '';", "", content)
    # Remove orgSel.style.zIndex = '999';
    content = re.sub(r"orgSel\.style\.zIndex = '999';", "", content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Fixed absolute positioning in {filename}")

print(f"Modified {count} files.")
