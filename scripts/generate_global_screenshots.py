from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import os
import time

urls_to_capture = {
    "timer": "file:///C:/TimerHavenWebsite/timer-en.html",
    "pomodoro": "file:///C:/TimerHavenWebsite/pomodoro-en.html",
    "unit_converter": "file:///C:/TimerHavenWebsite/unit-converter-en.html"
}

try:
    print("Starting Chrome for full page screenshots...")
    options = Options()
    options.add_argument("--headless")
    # Set the exact window size required by Chrome Web Store
    options.add_argument("--window-size=1280,800")
    options.add_argument("--hide-scrollbars")
    
    driver = webdriver.Chrome(options=options)
    
    for name, url in urls_to_capture.items():
        print(f"Capturing {name}...")
        driver.get(url)
        time.sleep(2)  # Wait for UI to render
        
        raw_path = rf"C:\TimerHavenWebsite\raw_{name}.png"
        final_path = rf"C:\TimerHavenWebsite\global_screenshot_{name}.jpg"
        
        # Take screenshot of the exact viewport (1280x800)
        driver.save_screenshot(raw_path)
        
        # Open and ensure it is exactly 1280x800, then save as JPEG (no alpha)
        img = Image.open(raw_path)
        img = img.convert("RGB")
        img = img.resize((1280, 800), Image.Resampling.LANCZOS)
        img.save(final_path, "JPEG", quality=95)
        
        print(f"Saved {final_path}")
        
        # Cleanup
        if os.path.exists(raw_path):
            os.remove(raw_path)

    driver.quit()
    print("All global screenshots captured successfully.")

except Exception as e:
    print(f"Error: {e}")
