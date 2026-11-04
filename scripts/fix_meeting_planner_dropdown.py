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

    # Fix: Make the <select> act as a listbox (expand) when typing, then close when a choice is made.
    # Replace the filterInput input listener:
    input_hook_sel = """        if (filterInput && !filterInput.dataset.hooked) {
          filterInput.addEventListener('input', () => {
            renderOptions(window.allCities, sel);
            if (filterInput.value.length >= 2) {
              sel.size = Math.min(sel.options.length, 6);
              sel.style.position = 'absolute';
              sel.style.zIndex = '999';
            } else {
              sel.size = 0;
              sel.style.position = '';
            }
          });
          filterInput.dataset.hooked = "true";
        }"""
    
    # We also need to add a click away listener to close it
    input_hook_sel += """
        document.addEventListener('click', (e) => {
          if (e.target !== filterInput && e.target !== sel) { sel.size = 0; sel.style.position = ''; }
        });
"""

    content = re.sub(r'if \(filterInput && !filterInput\.dataset\.hooked\) \{[\s\S]*?filterInput\.dataset\.hooked = "true";\s*\}', input_hook_sel, content, count=1)

    input_hook_orgSel = """        if (orgFilterInput && !orgFilterInput.dataset.hooked) {
          orgFilterInput.addEventListener('input', () => {
            renderOptions(window.allCities, orgSel, true);
            if (orgFilterInput.value.length >= 2) {
              orgSel.size = Math.min(orgSel.options.length, 6);
              orgSel.style.position = 'absolute';
              orgSel.style.zIndex = '999';
            } else {
              orgSel.size = 0;
              orgSel.style.position = '';
            }
          });
          orgFilterInput.dataset.hooked = "true";
        }"""
        
    input_hook_orgSel += """
        document.addEventListener('click', (e) => {
          if (e.target !== orgFilterInput && e.target !== orgSel) { orgSel.size = 0; orgSel.style.position = ''; }
        });
"""

    content = re.sub(r'if \(orgFilterInput && !orgFilterInput\.dataset\.hooked\) \{[\s\S]*?orgFilterInput\.dataset\.hooked = "true";\s*\}', input_hook_orgSel, content, count=1)

    # Now update the change listeners to reset size to 0
    change_hook_sel = """        if (sel && !sel.dataset.hookedChange) {
          sel.addEventListener('change', () => {
            sel.size = 0;
            sel.style.position = '';
            if (filterInput && filterInput.value) {
              const val = sel.value;
              filterInput.value = '';
              renderOptions(window.allCities, sel);
              sel.value = val;
            }
          });
          sel.dataset.hookedChange = "true";
        }"""
    content = re.sub(r'if \(sel && !sel\.dataset\.hookedChange\) \{[\s\S]*?sel\.dataset\.hookedChange = "true";\s*\}', change_hook_sel, content, count=1)

    change_hook_orgSel = """        if (orgSel && !orgSel.dataset.hookedChange) {
          orgSel.addEventListener('change', () => {
            orgSel.size = 0;
            orgSel.style.position = '';
            if (orgFilterInput && orgFilterInput.value) {
              const val = orgSel.value;
              orgFilterInput.value = '';
              renderOptions(window.allCities, orgSel, true);
              orgSel.value = val;
            }
          });
          orgSel.dataset.hookedChange = "true";
        }"""
    content = re.sub(r'if \(orgSel && !orgSel\.dataset\.hookedChange\) \{[\s\S]*?orgSel\.dataset\.hookedChange = "true";\s*\}', change_hook_orgSel, content, count=1)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Fixed dropdown UI in {filename}")

print(f"Modified {count} files.")
