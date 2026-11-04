import os
import re

directory = r"C:\TimerHavenWebsite"
includes_dir = os.path.join(directory, "_includes", "partials")
os.makedirs(includes_dir, exist_ok=True)

main_nav = """<nav class="main-nav">
  <div class="nav-container">
    <a href="/index.html" class="nav-link" id="nav-home">🏠 Home</a>
    <a href="/blog/index.html" class="nav-link" id="nav-blog">📚 Blog</a>
    <a href="/guides.html" class="nav-link" id="nav-guides">📖 Guides</a>
    <a href="/recommendations/index.html" class="nav-link" id="nav-recommendations">🎯 Recommendations</a>
    <a href="/pricing.html" class="nav-link" id="nav-pricing">🏷️ Pricing</a>
    <a href="/support.html" class="nav-link nav-link-support" id="nav-support">☕ Support Us</a>
    <a href="/about.html" class="nav-link" id="nav-about">ℹ️ About</a>
    <a href="/contact.html" class="nav-link" id="nav-contact">✉️ Contact</a>
  </div>
</nav>"""

main_footer = """<div class="footer-container">
    <div class="footer-brand">
      <h3>TimerHaven</h3>
      <p id="footer-copyright">&copy; 2025 TimerHaven. All tools are free and privacy-friendly.</p>
    </div>
    <div class="footer-links">
      <div class="footer-column">
        <h5 id="foot-col-tools">Tools</h5>
        <a href="/timer.html">Task Timer</a>
        <a href="/pomodoro.html">Pomodoro</a>
        <a href="/stopwatch.html">Stopwatch</a>
        <a href="/world-clock.html">World Clock</a>
      </div>
      <div class="footer-column">
        <h5 id="foot-col-res">Resources</h5>
        <a href="/blog/index.html" id="foot-link-blog">Blog</a>
        <a href="/guides.html" id="foot-link-guides">Guides</a>
        <a href="/recommendations/index.html" id="foot-link-gear">Gear</a>
      </div>
      <div class="footer-column">
        <h5 id="foot-col-support">Support</h5>
        <a href="/about.html" id="foot-link-about">About</a>
        <a href="/contact.html" id="foot-link-contact">Contact</a>
        <a href="/pricing.html" id="foot-link-pricing">Pricing</a>
        <a href="/support.html" id="foot-link-donate">Support Us</a>
      </div>
    </div>
  </div>"""

tool_footer = """<div style="font-size: 0.85em; color: #6b7c89; margin-bottom: 1em; max-width: 600px; margin-left: auto; margin-right: auto; text-align: center;">TimerHaven is your go-to destination for <strong>online timer</strong> and other <strong>privacy-first productivity tools</strong>.</div>
&copy; 2025 TimerHaven. <a href="/privacy.html">Privacy Policy</a> &middot; <a href="/terms.html">Terms</a> &middot;
  <a href="/pricing.html">Pricing</a> &middot; <a href="/contact.html">Contact</a>"""

with open(os.path.join(includes_dir, "main-nav.njk"), "w", encoding="utf-8") as f:
    f.write(main_nav)

with open(os.path.join(includes_dir, "main-footer.njk"), "w", encoding="utf-8") as f:
    f.write(main_footer)

with open(os.path.join(includes_dir, "tool-footer.njk"), "w", encoding="utf-8") as f:
    f.write(tool_footer)

files = [f for f in os.listdir(directory) if f.endswith(".html")]

for filename in files:
    filepath = os.path.join(directory, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace main nav
    content = re.sub(r'<nav class="main-nav">.*?</nav>', '{% include "partials/main-nav.njk" %}', content, flags=re.DOTALL)
    
    # Replace main footer
    content = re.sub(r'(<footer class="main-site-footer">)(.*?)(</footer>)', r'\1\n{% include "partials/main-footer.njk" %}\n\3', content, flags=re.DOTALL)
    
    # Replace tool footer - specifically targeting the content before SEO tags
    tool_footer_pattern = r'(<footer class="site" style="text-align:center; margin-top:1.5rem; color:#6b7280;">\s*<div style="font-size: 0.85em;.*?)(\s*<!-- SEO Content Section -->)'
    content = re.sub(tool_footer_pattern, r'<footer class="site" style="text-align:center; margin-top:1.5rem; color:#6b7280;">\n{% include "partials/tool-footer.njk" %}\n\2', content, flags=re.DOTALL)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Migration script completed!")
