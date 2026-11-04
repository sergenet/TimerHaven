import os
import re

directory = r'C:\TimerHavenWebsite'

files_to_check = [f for f in os.listdir(directory) if f.startswith('meeting-planner') and f.endswith('.html')]

count = 0
for filename in files_to_check:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    # 1. Change H:mm to h:mm a
    content = re.sub(r"\.toFormat\('H:mm'\)", ".toFormat('h:mm a')", content)
    
    # 2. Remove the corrupted selected character: ${hourLabel}${isSelected ? '' : ''}
    content = re.sub(r"\$\{hourLabel\}\$\{isSelected \? '[^']*' : ''\}", "${hourLabel}", content)

    # 3. Add change event listener for sel (participantCity)
    hook_sel = """        if (sel && !sel.dataset.hookedChange) {
          sel.addEventListener('change', () => {
            if (filterInput && filterInput.value) {
              const val = sel.value;
              filterInput.value = '';
              renderOptions(window.allCities, sel);
              sel.value = val;
            }
          });
          sel.dataset.hookedChange = "true";
        }"""
    
    # Add change event listener for orgSel (organizerTz)
    hook_orgSel = """        if (orgSel && !orgSel.dataset.hookedChange) {
          orgSel.addEventListener('change', () => {
            if (orgFilterInput && orgFilterInput.value) {
              const val = orgSel.value;
              orgFilterInput.value = '';
              renderOptions(window.allCities, orgSel, true);
              orgSel.value = val;
            }
          });
          orgSel.dataset.hookedChange = "true";
        }"""
        
    # We will inject these right after filterInput.dataset.hooked = "true";
    if 'sel.dataset.hookedChange' not in content:
        content = re.sub(r'(filterInput\.dataset\.hooked = "true";\s*})', r'\1\n' + hook_sel, content)
        content = re.sub(r'(orgFilterInput\.dataset\.hooked = "true";\s*})', r'\1\n' + hook_orgSel, content)
        
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Fixed bugs in {filename}")

print(f"Fixed {count} files.")
