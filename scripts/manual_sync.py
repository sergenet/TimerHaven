import sys
import os

# Add the engine directory to path
sys.path.append(r"c:\newgiftsandgadgets.com\engine")

from auto_affiliate_updater import upload_to_ftp

# Site root locally
PUBLIC_DIR = r"c:\newgiftsandgadgets.com\public"

if __name__ == "__main__":
    print("Starting manual FTP sync of 42 URLs...")
    upload_to_ftp(PUBLIC_DIR)
    print("Manual sync complete.")
