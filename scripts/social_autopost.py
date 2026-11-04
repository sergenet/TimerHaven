import json
import os
import random
import sys
import argparse
from pathlib import Path

# Add engine path to import PRODUCTS_POOL
ENGINE_PATH = r"c:\newgiftsandgadgets.com\engine"
if ENGINE_PATH not in sys.path:
    sys.path.append(ENGINE_PATH)

try:
    from products_data import PRODUCTS_POOL
except ImportError:
    print(f"Error: Could not find products_data.py in {ENGINE_PATH}")
    sys.path.append(".")
    PRODUCTS_POOL = {}

# Configuration
CONFIG_FILE = "social_config.json"
HISTORY_FILE = "post_history.json"
AFFILIATE_TAG = "sergenet01-20"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return {"posted_asins": []}

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def select_next_product(history):
    all_products = []
    for category, products in PRODUCTS_POOL.items():
        for p in products:
            p['category'] = category
            all_products.append(p)
    
    # Filter out recently posted products
    available = [p for p in all_products if p['asin'] not in history['posted_asins']]
    
    # If all products have been posted, reset history
    if not available:
        print("Resetting post history...")
        history['posted_asins'] = []
        available = all_products
    
    # Prioritize trending or new items
    trending = [p for p in available if p.get('is_trending') or p.get('is_new')]
    if trending:
        product = random.choice(trending)
    else:
        product = random.choice(available)
        
    return product

def format_twitter_post(product):
    hashtags = ["#AmazonBigSpringSale", "#TechDeals", "#SpringDeals", f"#{product['category'].replace('-', '')}"]
    tags_str = " ".join(hashtags)
    
    post = (
        f"🚨 HOT DEAL: {product['name']} 🌸\n\n"
        f"{product['desc'][:100]}...\n\n"
        f"🏷️ Price: {product['price']}\n"
        f"🔗 Get it here: https://www.amazon.com/dp/{product['asin']}?tag={AFFILIATE_TAG}\n\n"
        f"{tags_str}"
    )
    return post

def format_pinterest_post(product):
    return {
        "title": f"{product['name']} - Amazon Big Spring Sale Deals 2026",
        "description": f"{product['desc']} Check out the best tech deals for spring 2026. #AmazonDeals #Tech #SpringSale",
        "link": f"https://www.amazon.com/dp/{product['asin']}?tag={AFFILIATE_TAG}",
        "image_url": "https://newgiftsandgadgets.com/assets/images/placeholder.jpg" # Update with actual site URL if hosted
    }

def main():
    parser = argparse.ArgumentParser(description="Auto-post sale items to social media.")
    parser.add_argument("--dry-run", action="store_true", help="Print posts without sending.")
    parser.add_argument("--platform", choices=["twitter", "pinterest", "all"], default="all")
    args = parser.parse_args()

    history = load_history()
    product = select_next_product(history)
    
    print(f"--- AUTO-POSTING: {product['name']} ---")
    
    if args.platform in ["twitter", "all"]:
        tweet = format_twitter_post(product)
        print("\n[TWITTER/X DRAFT]:")
        print(tweet)
        
    if args.platform in ["pinterest", "all"]:
        pin = format_pinterest_post(product)
        print("\n[PINTEREST DRAFT]:")
        print(f"Title: {pin['title']}")
        print(f"Desc: {pin['description']}")
        print(f"URL: {pin['link']}")

    if not args.dry_run:
        # Placeholder for actual API calls
        # if config.get('X_API_KEY'): ...
        print("\n[LIVE POSTING DISABLED] Please add your API logic or use manual mode.")
        pass
    else:
        print("\n[DRY RUN] No live posts were made.")

    # Update history
    history['posted_asins'].append(product['asin'])
    save_history(history)

if __name__ == "__main__":
    main()
