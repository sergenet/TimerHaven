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

    # Find the data-template we injected earlier
    template_match = re.search(r'<input\s+id="unitFilter"[^>]*data-template="([^"]+)"', content)
    if template_match:
        template = template_match.group(1)
        
        # Check if the logic is already inside populateUnits
        # If it's not, we will inject it.
        # Function signature might be: `function populateUnits(type) {` or `function populateUnits(t) {` etc.
        # It's probably `function populateUnits(type) {`
        if "document.getElementById('unitFilter').placeholder =" not in content:
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
            
            content = re.sub(r'function populateUnits\(type\)\s*\{', logic, content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Fixed placeholder init in {filename}")

print(f"Modified {count} files.")
