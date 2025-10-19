import os
import re

# Set your folder(s) containing the files to update
folders = [
    "notes_pages",
    "notes_articles",
    "localized_homepages"
]

# Patterns to match any localized index (e.g. index-fr.html, index-de.html, etc.)
localized_index_pattern = re.compile(r'index-[a-z]{2}\.html')

# Patterns to match the back link in notes and articles
back_link_patterns = [
    # <a href="index-xx.html" ...>...</a>
    re.compile(r'(<a\s+href=")index-[a-z]{2}\.html(".*?>)', re.IGNORECASE),
    # <a href="notes-xx.html" ...>...</a>
    re.compile(r'(<a\s+href=")notes-[a-z]{2}\.html(".*?>)', re.IGNORECASE),
]

# Replace function
def replace_links_in_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    for pat in back_link_patterns:
        content = pat.sub(r'\1index.html\2', content)
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {filepath}")

def main():
    for folder in folders:
        if not os.path.exists(folder):
            continue
        for fname in os.listdir(folder):
            if fname.endswith(".html"):
                path = os.path.join(folder, fname)
                replace_links_in_file(path)
    print("All back links updated to index.html.")

if __name__ == "__main__":
    main()