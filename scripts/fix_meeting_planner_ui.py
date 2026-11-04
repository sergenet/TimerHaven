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

    # Fix 1: Remove the annoying sel.focus() and sel.showPicker() that steals focus while typing
    # Regex will replace:
    #             if (filterInput.value.length >= 3) {
    #               sel.focus();
    #               if (sel.showPicker) sel.showPicker(); // Modern browsers
    #             }
    # and the equivalent for orgSel.
    content = re.sub(r'// Auto-focus and try to open dropdown for better UX \(minimum 3 chars\)\s*if \(filterInput\.value\.length >= 3\) \{\s*sel\.focus\(\);\s*if \(sel\.showPicker\) sel\.showPicker\(\);\s*// Modern browsers\s*\}', '', content)
    content = re.sub(r'// Auto-focus and try to open dropdown for better UX \(minimum 3 chars\)\s*if \(orgFilterInput\.value\.length >= 3\) \{\s*orgSel\.focus\(\);\s*if \(orgSel\.showPicker\) orgSel\.showPicker\(\);\s*// Modern browsers\s*\}', '', content)

    # Fix 2: Ensure the currently selected option is preserved in renderOptions when query is empty
    # Find:
    #        } else {
    #          // When no search query, show curated popular cities instead of first 200 alphabetically
    #          filtered = FALLBACK.map(pc => entries.find(e => e.name === pc.name && e.timezone === pc.timezone)).filter(Boolean);
    #        }
    render_fix = """        } else {
          // When no search query, show curated popular cities instead of first 200 alphabetically
          filtered = FALLBACK.map(pc => entries.find(e => e.name === pc.name && e.timezone === pc.timezone)).filter(Boolean);
          const currentVal = targetSel.value;
          if (currentVal && currentVal !== "") {
            const [cName, cTz] = currentVal.split('|');
            const currentEntry = entries.find(e => e.name === cName && e.timezone === cTz);
            if (currentEntry && !filtered.some(f => f.name === currentEntry.name && f.timezone === currentEntry.timezone)) {
              filtered.unshift(currentEntry);
            }
          }
        }"""
    
    content = re.sub(r'\} else \{\s*// When no search query, show curated popular cities instead of first 200 alphabetically\s*filtered = FALLBACK\.map\(pc => entries\.find\(e => e\.name === pc\.name && e\.timezone === pc\.timezone\)\)\.filter\(Boolean\);\s*\}', render_fix, content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Fixed meeting planner logic in {filename}")

print(f"Modified {count} files.")
