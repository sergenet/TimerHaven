import os
import re

def remove_tip_section_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    # Remove <div class="tip-section">...</div> (supports multi-line, non-greedy)
    new_content = re.sub(
        r'<div\s+class="tip-section".*?>.*?</div>',
        '',
        content,
        flags=re.DOTALL | re.IGNORECASE
    )
    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Tip removed: {filepath}")

def process_html_files(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(".html"):
                remove_tip_section_from_file(os.path.join(subdir, file))

if __name__ == "__main__":
    # Change '.' to your html directory path if needed
    process_html_files(".")