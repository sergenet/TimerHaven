import os
import re
from datetime import datetime, timedelta
from babel.dates import format_date

BASE_DIR = r"C:\TimerHavenWebsite"
LANGUAGES = {
    "en": "en_US",
    "fr": "fr_FR",
    "es": "es_ES",
    "de": "de_DE",
    "ru": "ru_RU",
    "el": "el_GR",
    "ar": "ar_AE"
}

def main():
    blog_dir = os.path.join(BASE_DIR, "blog")
    files = [f for f in os.listdir(blog_dir) if f.endswith(".html") and f != "index.html"]
    files.sort() # Ensure consistent ordering for dates
    
    start_date = datetime(2026, 1, 20)
    
    for idx, filename in enumerate(files):
        # Calculate date for this specific blog post
        post_date = start_date + timedelta(days=(idx * 7))
        meta_date = post_date.strftime("%Y-%m-%d")
        
        for lang_code, locale in LANGUAGES.items():
            if lang_code == "en":
                filepath = os.path.join(BASE_DIR, "blog", filename)
            else:
                filepath = os.path.join(BASE_DIR, lang_code, "blog", filename)
                
            if not os.path.exists(filepath):
                continue
                
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Generate the localized display date
            # 'medium' format usually produces things like "Feb 7, 2026" or "7 fév. 2026"
            display_date = format_date(post_date, format='medium', locale=locale)
            
            # Replace meta tags
            content = re.sub(r'<meta name="datePublished" content=".*?">', f'<meta name="datePublished" content="{meta_date}">', content)
            content = re.sub(r'<meta name="dateModified" content=".*?">', f'<meta name="dateModified" content="{meta_date}">', content)
            
            # Replace JSON-LD properties
            content = re.sub(r'"datePublished":\s*".*?"', f'"datePublished": "{meta_date}"', content)
            content = re.sub(r'"dateModified":\s*".*?"', f'"dateModified": "{meta_date}"', content)
            
            # Replace visual display date
            # Matches: <div class="meta">Text: [date] Reading time...
            # We look for the year 2026 to anchor the end of the date string
            # Notice the non-greedy match .*?2026
            meta_pattern = r'(<div class="meta">[^:]+:\s*).*?2026(.*?</div)'
            # If the language uses a different format that doesn't include "2026" specifically, we replace the whole contents but we must preserve the reading time.
            # A safer regex: capture from the colon up to the next span or text block.
            # Actually, ".*?2026" works perfectly because all current files are hardcoded to 2026.
            content = re.sub(meta_pattern, r'\g<1>' + display_date + r'\g<2>', content)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
                
        print(f"Updated '{filename}' across all languages to {meta_date}")

if __name__ == "__main__":
    main()
