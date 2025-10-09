import glob
import re

# Change this to your project folder if needed
PROJECT_FOLDER = "."

title_set = set()
desc_set = set()
issues = []

for filename in glob.glob(PROJECT_FOLDER + "/**/*.html", recursive=True):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    title_match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
    meta_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE | re.DOTALL)
    title = title_match.group(1).strip() if title_match else None
    desc = meta_match.group(1).strip() if meta_match else None

    if not title:
        issues.append(f"{filename}: MISSING <title>")
    else:
        if title in title_set:
            issues.append(f"{filename}: DUPLICATE <title>: {title}")
        title_set.add(title)

    if not desc:
        issues.append(f"{filename}: MISSING <meta name=\"description\">")
    else:
        if desc in desc_set:
            issues.append(f"{filename}: DUPLICATE <meta description>: {desc}")
        desc_set.add(desc)

if not issues:
    print("All files have unique <title> and <meta name=\"description\"> tags!")
else:
    print("SEO Meta Tag Audit Report:")
    for issue in issues:
        print(issue)