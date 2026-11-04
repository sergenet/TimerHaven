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

    # 1. Remove the entire `else` block in `renderOptions` so it falls back to showing all cities
    # We will regex replace the entire else block.
    # The block looks like this:
    #                 } else {
    #           // When no search query, show curated popular cities instead of first 200 alphabetically
    #           filtered = FALLBACK.map(pc => entries.find(e => e.name === pc.name && e.timezone === pc.timezone)).filter(Boolean);
    #           const currentVal = targetSel.value;
    #           if (currentVal && currentVal !== "") {
    #             const [cName, cTz] = currentVal.split('|');
    #             const currentEntry = entries.find(e => e.name === cName && e.timezone === cTz);
    #             if (currentEntry && !filtered.some(f => f.name === currentEntry.name && f.timezone === currentEntry.timezone)) {
    #               filtered.unshift(currentEntry);
    #             }
    #           }
    #         }
    # We'll replace it with a much simpler else block that just keeps the full list but ensures the selected value is preserved/visible?
    # Actually, if filtered is the full list, the selected value IS ALREADY IN IT! We don't need any special logic.
    
    new_else_block = """        }"""
    
    content = re.sub(r'\} else \{\s*// When no search query[\s\S]*?filtered\.unshift\(currentEntry\);\s*\}\s*\}\s*\}', new_else_block, content)

    # 2. Change placeholder text from "Use filter above to search cities" to "Select a city..."
    content = re.sub(r"const placeholderText = isOrg \? 'Use filter above to search cities' : 'Use filter above to search cities';", "const placeholderText = isOrg ? 'Select a city...' : 'Select a city...';", content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Fixed dropdown list in {filename}")

print(f"Modified {count} files.")
