import glob
import os

SITE_URL = "https://timerhaven.com"  # Change to your domain

files = glob.glob("**/*.html", recursive=True)
print(f"Found {len(files)} HTML files.")

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for file in files:
        # Skip files in hidden folders or system files
        if file.startswith('.') or '404' in file:
            continue
        url = SITE_URL + '/' + file.replace("\\", "/")
        print(f"Adding: {url}")
        f.write(f'  <url><loc>{url}</loc></url>\n')
    f.write('</urlset>\n')
print("sitemap.xml generated!")