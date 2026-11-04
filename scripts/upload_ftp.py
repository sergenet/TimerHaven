try:  # local credentials file, never committed
    from _secrets import FTP_PASS
except ImportError:  # fall back to the environment
    import os
    FTP_PASS = os.environ.get('TH_FTP_PASS', '')
import os
import ftplib
import time
import json
import hashlib

host = 'ftp.timerhaven.com'
user = 'contact@timerhaven.com'
passwd = FTP_PASS
local_dir = r'C:\TimerHavenWebsite'
cache_file = os.path.join(local_dir, '.ftp_sync_cache.json')

# Load sync cache if exists
cache = {}
if os.path.exists(cache_file):
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache = json.load(f)
    except Exception:
        cache = {}

def get_file_hash(filepath):
    h = hashlib.md5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def get_ftp():
    for attempt in range(5):
        try:
            print("Connecting to FTP...")
            ftp = ftplib.FTP(host, timeout=60)
            ftp.login(user, passwd)
            ftp.set_pasv(True)
            return ftp
        except Exception as e:
            print(f"Connection attempt {attempt+1} failed: {e}. Retrying in 5s...")
            time.sleep(5)
    raise RuntimeError("Failed to connect to FTP after 5 attempts.")

def ensure_remote_dir(ftp_client, remote_path):
    dirs = remote_path.replace('\\', '/').strip('/').split('/')
    if not dirs or dirs == ['']:
        return
    current_dir = ftp_client.pwd()
    for d in dirs:
        try:
            ftp_client.cwd(d)
        except ftplib.error_perm:
            print(f"Creating remote directory {d}")
            ftp_client.mkd(d)
            ftp_client.cwd(d)
    ftp_client.cwd(current_dir)

# 1. Identify files that actually need uploading
files_to_upload = []
for root, dirs, files in os.walk(local_dir):
    # '.tmpcheck' is where local page backups live; syncing it published duplicate
    # copies of blog pages that Google could crawl (2026-11-01).
    if any(skip in root for skip in ['.git', 'node_modules', '.temp', '.tmpcheck', '_site', 'android', '.expo', 'chrome_', 'YouTube', 'timerhaven-extension']):
        continue
    for file in files:
        if file.endswith(('.html', '.css', '.js', '.xml')):
            local_path = os.path.join(root, file)
            rel_path = os.path.relpath(local_path, local_dir).replace('\\', '/')
            mtime = os.path.getmtime(local_path)
            file_hash = get_file_hash(local_path)
            
            # If not in cache or hash changed, queue for upload
            if cache.get(rel_path) != file_hash:
                files_to_upload.append((local_path, rel_path, file_hash))

print(f"Total files to upload: {len(files_to_upload)}")

if not files_to_upload:
    print("All files are already up-to-date on the server!")
    exit(0)

ftp = get_ftp()
uploaded_count = 0

for local_path, rel_path, file_hash in files_to_upload:
    remote_dir = os.path.dirname(rel_path)
    success = False
    
    for retry in range(3):
        try:
            if remote_dir:
                ensure_remote_dir(ftp, remote_dir)
            print(f"Uploading {rel_path}...")
            with open(local_path, 'rb') as f:
                ftp.storbinary(f'STOR {rel_path}', f)
            
            cache[rel_path] = file_hash
            uploaded_count += 1
            success = True
            time.sleep(0.08)  # Gentle delay to prevent Pure-FTPd rate-limiting
            break
        except Exception as e:
            print(f"Error on {rel_path}: {e}. Reconnecting...")
            try:
                ftp.quit()
            except Exception:
                pass
            time.sleep(3)
            ftp = get_ftp()
            
    if not success:
        print(f"FAILED permanently to upload {rel_path}")

try:
    ftp.quit()
except Exception:
    pass

# Save updated cache
with open(cache_file, 'w', encoding='utf-8') as f:
    json.dump(cache, f, indent=2)

print(f"Done! Successfully uploaded {uploaded_count} updated files.")
