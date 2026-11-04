import re

file_path = r'C:\TimerHavenWebsite\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract translations block
match = re.search(r'en:\s*{(.*?)}', content, re.DOTALL)
if not match:
    print("Could not find translations block")
    exit(1)

en_dict_text = match.group(1)
en_dict = {}
for line in en_dict_text.split('\n'):
    line = line.strip()
    if ':' in line:
        key, val = line.split(':', 1)
        key = key.strip().strip('"').strip("'")
        val = val.strip().strip(',').strip('"').strip("'")
        en_dict[key] = val

replaced = 0
for key, text in en_dict.items():
    # Looking for <div class="..." id="key"></div>
    # or <h2 id="key"></h2>
    # or <a ... id="key"></a>
    
    # regex to match empty tag with this id
    pattern = re.compile(rf'(<[^>]+id="{key}"[^>]*>)\s*(</[^>]+>)')
    new_content, count = pattern.subn(rf'\g<1>{text}\g<2>', content)
    
    if count > 0:
        content = new_content
        replaced += count

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Injected {replaced} default text strings into index.html")
