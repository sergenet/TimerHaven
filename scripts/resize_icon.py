from PIL import Image
import os

source_path = r"C:\TimerHavenWebsite\timerhaven-extension\icons\icon128.png"
output_path = r"C:\TimerHavenWebsite\store_icon_128x128.png"

try:
    with Image.open(source_path) as img:
        print(f"Original size: {img.size}")
        
        # Resize to exactly 128x128
        resized_img = img.resize((128, 128), Image.Resampling.LANCZOS)
        resized_img.save(output_path, "PNG")
        print(f"Saved exactly 128x128 PNG to {output_path}")

except Exception as e:
    print(f"Error: {e}")
