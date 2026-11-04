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

    # Find the unitFilter input
    # e.g., <input id="unitFilter" class="form-control unit-filter" placeholder="Filter units (e.g. 'square')..." title="Type here to filter unit lists" />
    # or Spanish: <input id="unitFilter" class="form-control unit-filter" placeholder="Filtro (ej.: liter o m)" />
    match_input = re.search(r'<input\s+id="unitFilter"[^>]*placeholder="([^"]+)"[^>]*>', content)
    if match_input:
        original_placeholder = match_input.group(1)
        
        # Create a template by replacing the specific example
        template = original_placeholder
        if "'square'" in template:
            template = template.replace("'square'", "'{ex}'")
        elif "liter o m" in template:
            template = template.replace("liter o m", "'{ex}'")
        elif "liter ou m" in template:
            template = template.replace("liter ou m", "'{ex}'")
        elif "liter \u0438\u043b\u0438 m" in template: # Russian
            template = template.replace("liter \u0438\u043b\u0438 m", "'{ex}'")
        elif "liter oder m" in template:
            template = template.replace("liter oder m", "'{ex}'")
        elif "liter \u03ae m" in template: # Greek
            template = template.replace("liter \u03ae m", "'{ex}'")
        elif "liter \u0623\u0648 m" in template: # Arabic
            template = template.replace("liter \u0623\u0648 m", "'{ex}'")
        else:
            # Fallback if no exact match, try to just replace "liter" or "square"
            template = re.sub(r'liter|square', '{ex}', template)
            
        # Add data-template to the input if not already there
        if 'data-template="' not in match_input.group(0):
            new_input = match_input.group(0).replace('placeholder="', f'data-template="{template}" placeholder="')
            content = content.replace(match_input.group(0), new_input)
            
        # Now update the javascript to use the template
        # Find typeSelect.addEventListener
        js_hook = "unitFilter.value = '';\n      populateUnits(t);"
        new_js = f"""unitFilter.value = '';
      populateUnits(t);
      const allU = getUnitsForType(t);
      if (allU.length > 0) {{
        let example = allU[0].toLowerCase().split(' ')[0];
        if (t === 'temperature') example = 'celsius';
        if (t === 'speed') example = 'km/h';
        if (t === 'length') example = 'meter';
        if (t === 'area') example = 'square';
        if (t === 'volume') example = 'liter';
        if (t === 'data') example = 'byte';
        if (t === 'frequency') example = 'hz';
        const template = unitFilter.getAttribute('data-template') || "{template}";
        unitFilter.placeholder = template.replace('{{ex}}', example);
      }}"""
        
        # Only inject if we haven't already
        if "unitFilter.getAttribute('data-template')" not in content:
            content = content.replace(js_hook, new_js)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Updated {filename}")

print(f"Modified {count} files.")
