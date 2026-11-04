import os
import random
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Configuration
BLOG_DIR = r"C:\TimerHavenWebsite\blog"
BASE_URL = "https://timerhaven.com/blog/"

def extract_title(html_content):
    match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
    if match:
        title = match.group(1).replace(" | TimerHaven", "").replace(" | Productivity Guide", "").strip()
        return title
    return "Productivity Guide"

def extract_description(html_content):
    match = re.search(r'<meta name="description" content="(.*?)">', html_content, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return "Check out this guide to boost your productivity!"

def generate_twitter_post(title, desc, url):
    hashtags = ["#Productivity", "#DeepWork", "#TimeManagement", "#TimerHaven"]
    tags_str = " ".join(random.sample(hashtags, 3))
    
    post = (
        f"🧠 {title}\n\n"
        f"💡 {desc[:150]}...\n\n"
        f"Read the full guide (100% Free & No Ads): \n"
        f"🔗 {url}\n\n"
        f"{tags_str}"
    )
    return post

def generate_pinterest_post(title, desc, url):
    return {
        "title": f"{title} - Productivity Guide",
        "description": f"{desc} Learn how to master your time with TimerHaven's free tools and guides. #Productivity #StudyTips #DeepWork",
        "link": url,
        "image_url": "https://timerhaven.com/images/social-banner.webp"
    }

def main():
    print("--- TimerHaven Social Post Generator ---\n")
    files = [f for f in os.listdir(BLOG_DIR) if f.endswith(".html") and f != "index.html"]
    
    # Pick 3 random articles for today
    selected_files = random.sample(files, min(3, len(files)))
    
    for filename in selected_files:
        filepath = os.path.join(BLOG_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        title = extract_title(content)
        desc = extract_description(content)
        url = BASE_URL + filename
        
        tweet = generate_twitter_post(title, desc, url)
        pin = generate_pinterest_post(title, desc, url)
        
        print(f"✅ Generating posts for: {title}")
        print("-" * 40)
        print("[TWITTER / X DRAFT]:")
        print(tweet)
        print("\n[PINTEREST DRAFT]:")
        print(f"Title: {pin['title']}")
        print(f"Desc:  {pin['description']}")
        print(f"URL:   {pin['link']}")
        print("=" * 60 + "\n")
        
    print("TIP: Copy these drafts and schedule them in your social media manager (like Buffer, TweetDeck, or manually).")

if __name__ == "__main__":
    main()
