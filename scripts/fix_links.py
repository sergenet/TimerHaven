import os
import re

directory = r'C:\TimerHavenWebsite'
html_files = []

for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

# Regex to match href="..//privacy.html", href="//privacy.html", etc.
pattern = re.compile(r'href="(?:(?:\.\./)+|//|(?:\.\./)+//)(privacy|terms|contact)\.html"')

replaced_count = 0

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, num_subs = pattern.subn(r'href="/\1.html"', content)
        
        # Also let's catch plain `href="//privacy.html"` if the regex above missed it due to quotes variations
        new_content, num_subs2 = re.subn(r"href='(?:(?:\.\./)+|//|(?:\.\./)+//)(privacy|terms|contact)\.html'", r"href='/\1.html'", new_content)
        
        if num_subs > 0 or num_subs2 > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            replaced_count += 1
            print(f"Fixed links in: {file_path} ({num_subs + num_subs2} replacements)")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print(f"\nDone. Fixed links in {replaced_count} files.")
