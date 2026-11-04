import subprocess
import os
import sys

# PATHS
BUILD_SCRIPT = r"c:\newgiftsandgadgets.com\engine\build.py"
SYNC_SCRIPT = r"c:\TimerHavenWebsite\manual_sync.py"

def run():
    print("--- STEP 1: REBUILDING SITE ---")
    try:
        subprocess.run([sys.executable, BUILD_SCRIPT], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Build Failed: {e}")
        return

    print("\n--- STEP 2: SYNCRONIZING TO PRODUCTION ---")
    try:
        subprocess.run([sys.executable, SYNC_SCRIPT], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Sync Failed: {e}")
        return

    print("\nPUBLISH COMPLETE! Your site is live and 100% updated.")

if __name__ == "__main__":
    run()
