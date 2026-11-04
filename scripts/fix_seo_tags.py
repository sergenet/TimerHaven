import os
import re

directory = r'C:\TimerHavenWebsite'
tools = [
    'calendar', 'clipboard-manager', 'countdown', 'currency', 'focus-music', 
    'habit-tracker', 'meeting-planner', 'notes', 'password-generator', 
    'pomodoro', 'stopwatch', 'timer', 'unit-converter', 'weather', 'world-clock', 'index'
]

langs = ['en', 'fr', 'es', 'de', 'ru', 'el', 'ar']

replaced_files = 0

for tool in tools:
    # Build list of files for this tool
    files_to_check = [f"{tool}.html"] + [f"{tool}-{lang}.html" for lang in langs]
    
    for filename in files_to_check:
        file_path = os.path.join(directory, filename)
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # 1. Fix Canonical Tags
        # Find canonical link and replace its href with the actual filename
        content = re.sub(
            r'<link rel="canonical" href="https://timerhaven.com/[^"]+"',
            f'<link rel="canonical" href="https://timerhaven.com/{filename}"',
            content
        )
        # Also catch self-closing variant
        content = re.sub(
            r'<link rel="canonical" href="https://timerhaven.com/[^"]+"\s*/>',
            f'<link rel="canonical" href="https://timerhaven.com/{filename}" />',
            content
        )

        # 2. Fix hreflang Tags
        def hreflang_replacer(match):
            href_prefix = match.group(1) # <link rel="alternate" href="
            url = match.group(2) # https://timerhaven.com/...
            hreflang_suffix = match.group(3) # " hreflang="fr" />
            lang = match.group(4) # fr
            
            target_url = f"https://timerhaven.com/{tool}-{lang}.html"
            if lang == 'en' or lang == 'x-default':
                target_url = f"https://timerhaven.com/{tool}-en.html"
                
            return f'{href_prefix}{target_url}{hreflang_suffix}'

        # Match <link rel="alternate" href="URL" hreflang="LANG" />
        content = re.sub(
            r'(<link\s+rel="alternate"\s+href=")(https://timerhaven.com/[^"]+)("\s+hreflang="([^"]+)"\s*/>)',
            hreflang_replacer,
            content
        )
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            replaced_files += 1
            print(f"Fixed canonical/hreflang in: {filename}")

print(f"\nDone. Fixed tags in {replaced_files} files.")
