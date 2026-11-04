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

    # The block we injected in the change listener:
    #       const allU = getUnitsForType(t);
    #       if (allU.length > 0) { ... unitFilter.placeholder = template.replace('{ex}', example); }
    
    # We will remove it from the change listener
    match_injected = re.search(r'const allU = getUnitsForType\(t\);\s*if \(allU\.length > 0\) \{.*?unitFilter\.placeholder = template\.replace\([^)]+\);\s*\}', content, re.DOTALL)
    if match_injected:
        content = content.replace(match_injected.group(0), '')
        
        # Now we will inject it into populateUnits(type)
        # Function signature: function populateUnits(type) { ...
        # Let's insert it right at the beginning of populateUnits
        # But wait, populateUnits uses 'type' instead of 't'.
        # Let's generate the new logic
        
        # To make it clean, we find the template attribute on unitFilter
        template_match = re.search(r'<input\s+id="unitFilter"[^>]*data-template="([^"]+)"', content)
        if template_match:
            template = template_match.group(1)
            
            logic = f"""function populateUnits(type) {{
      const allU = getUnitsForType(type);
      if (allU.length > 0) {{
        let example = allU[0].toLowerCase().split(' ')[0];
        if (type === 'temperature') example = 'celsius';
        if (type === 'speed') example = 'km/h';
        if (type === 'length') example = 'meter';
        if (type === 'area') example = 'square';
        if (type === 'volume') example = 'liter';
        if (type === 'data') example = 'byte';
        if (type === 'frequency') example = 'hz';
        const template = document.getElementById('unitFilter').getAttribute('data-template') || "{template}";
        document.getElementById('unitFilter').placeholder = template.replace('{{ex}}', example);
      }}"""
            
            # Replace the start of populateUnits
            content = re.sub(r'function populateUnits\(type\) \{', logic, content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Fixed placeholder logic in {filename}")

print(f"Modified {count} files.")
