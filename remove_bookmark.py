import os
import glob

# Folder containing your HTML files
HTML_FOLDER = "./"  # Change to your folder if needed

# Text to search for (case-insensitive)
SEARCH_TEXT = "Bookmark this page:"

# File pattern (all HTML files)
file_pattern = os.path.join(HTML_FOLDER, "*.html")

for filepath in glob.glob(file_pattern):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # Remove any line containing SEARCH_TEXT
    new_lines = [line for line in lines if SEARCH_TEXT.lower() not in line.lower()]
    if len(new_lines) != len(lines):
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"Removed bookmark line from: {filepath}")
    else:
        print(f"No bookmark line found in: {filepath}")