import os

# The code snippets to insert
ADSENSE = '''<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-0467059729557007"
     crossorigin="anonymous"></script>
'''

ANALYTICS = '''<script async src="https://www.googletagmanager.com/gtag/js?id=G-R1F6Y45MW2"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-R1F6Y45MW2');
</script>
'''

INSERT_CODE = ADSENSE + ANALYTICS

def insert_code_in_head(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    # Check if already present
    if 'ca-pub-0467059729557007' in content or 'G-R1F6Y45MW2' in content:
        print(f"Skipping (already contains code): {filename}")
        return
    # Insert right after <head>
    new_content = content.replace('<head>', f'<head>\n{INSERT_CODE}', 1)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Inserted in: {filename}")

def main():
    for fname in os.listdir('.'):
        if fname.lower().endswith('.html'):
            insert_code_in_head(fname)

if __name__ == "__main__":
    main()