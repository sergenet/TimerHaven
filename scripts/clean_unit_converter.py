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

    # 1. Remove <div class="tool-intro" id="tool-help" data-preserve="true"> ... </div>
    # It ends before <a id="read-guide-btn"
    pattern1 = r'<div class="tool-intro"[^>]*id="tool-help"[^>]*data-preserve="true"[^>]*>.*?</div>\s*(?=<a id="read-guide-btn")'
    content = re.sub(pattern1, '', content, flags=re.DOTALL)

    # Wait, in the Spanish version, the ID might not be "read-guide-btn", let's be more generic.
    # It might just be <a class="read-guide" ...>
    pattern1_fallback = r'<div class="tool-intro"[^>]*id="tool-help"[^>]*data-preserve="true"[^>]*>.*?</div>\s*(?=<a[^>]*class="[^"]*read-guide[^"]*")'
    content = re.sub(pattern1_fallback, '', content, flags=re.DOTALL)

    # 2. Remove <details class="faq-section"> ... </details>
    # It ends before </div>\s*</section>
    pattern2 = r'<details class="faq-section".*?</details>\s*(?=<)'
    content = re.sub(pattern2, '', content, flags=re.DOTALL)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Cleaned {filename}")

print(f"Modified {count} files.")
