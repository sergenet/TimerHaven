import shutil
import os

source_dir = r'C:\TimerHavenWebsite\timerhaven-extension'
output_filename = r'C:\TimerHavenWebsite\timerhaven-extension-v2'

# Create a zip archive (the extension adds .zip automatically)
shutil.make_archive(output_filename, 'zip', source_dir)

print(f"Created {output_filename}.zip successfully.")
