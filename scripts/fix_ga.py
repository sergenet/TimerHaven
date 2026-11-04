import os
import re

directory = r'C:\TimerHavenWebsite'
html_files = []

for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

# Regex to match the duplicate Google Analytics tag block
# It usually looks like this:
# <!-- Google tag (gtag.js) -->
# <script async src="https://www.googletagmanager.com/gtag/js?id=G-R1F6Y45MW2"></script>
# <script>
#     window.dataLayer = window.dataLayer || [];
#     function gtag(){dataLayer.push(arguments);}
#     gtag('js', new Date());
#     gtag('config', 'G-R1F6Y45MW2');
# </script>

pattern = re.compile(
    r'<!--\s*Google tag \(gtag\.js\)\s*-->\s*<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-R1F6Y45MW2"></script>\s*<script>\s*window\.dataLayer = window\.dataLayer \|\| \[\];\s*function gtag\(\)\s*\{[^\}]*\}\s*gtag\(\'js\', new Date\(\)\);\s*gtag\(\'config\', \'G-R1F6Y45MW2\'\);\s*</script>',
    re.IGNORECASE | re.DOTALL
)

# Also check for just the script tags without the comment
pattern2 = re.compile(
    r'<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-R1F6Y45MW2"></script>\s*<script>\s*window\.dataLayer = window\.dataLayer \|\| \[\];\s*function gtag\(\)\s*\{[^\}]*\}\s*gtag\(\'js\', new Date\(\)\);\s*gtag\(\'config\', \'G-R1F6Y45MW2\'\);\s*</script>',
    re.IGNORECASE | re.DOTALL
)

replaced_count = 0

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, count = pattern.subn('', content)
        new_content, count2 = pattern2.subn('', new_content)
        
        total_count = count + count2
        
        if total_count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            replaced_count += 1
            print(f"Removed duplicate GA tag from: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print(f"\nDone. Removed GA tag from {replaced_count} files.")
