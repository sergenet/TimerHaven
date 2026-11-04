try:  # local credentials file, never committed
    from _secrets import FTP_PASS
except ImportError:  # fall back to the environment
    import os
    FTP_PASS = os.environ.get('TH_FTP_PASS', '')
import os
import ftplib

host = 'ftp.timerhaven.com'
user = 'contact@timerhaven.com'
passwd = FTP_PASS

directory = r'C:\TimerHavenWebsite'
files_to_upload = [f for f in os.listdir(directory) if f.endswith('.html')]

ftp = ftplib.FTP(host, timeout=30)
ftp.login(user, passwd)
ftp.set_pasv(True)

count = 0
for filename in files_to_upload:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'rb') as f:
        ftp.storbinary(f'STOR {filename}', f)
        count += 1
        print(f"Uploaded {filename}")

ftp.quit()
print(f"Done! Uploaded {count} files.")
