import glob
import os

# Customize this to match your project folder
PROJECT_FOLDER = "."  # "." means current folder; or set to your folder path

# Your new footer (copy this exactly)
new_footer = """
<footer>
  &copy; 2025 TimerHaven. All tools are free and privacy-friendly.<br>
  <a href="privacy.html">Privacy Policy</a> &bull;
  <a href="terms.html">Terms</a> &bull;
  <a href="contact.html">Contact</a>
</footer>
"""

def update_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    # Try to replace old <footer>...</footer> with new_footer
    if "<footer" in content and "</footer>" in content:
        start = content.find("<footer")
        end = content.find("</footer>") + len("</footer>")
        content = content[:start] + new_footer + content[end:]
    else:
        # If no footer, add before </body>
        if "</body>" in content:
            content = content.replace("</body>", new_footer + "\n</body>")
        else:
            # If no </body>, add at end
            content = content + "\n" + new_footer
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    # Find all HTML files (including in subfolders)
    for filename in glob.glob(os.path.join(PROJECT_FOLDER, "**", "*.html"), recursive=True):
        print(f"Updating: {filename}")
        update_file(filename)
    print("All footers updated!")

if __name__ == "__main__":
    main()