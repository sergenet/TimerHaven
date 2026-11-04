try:  # local credentials file, never committed
    from _secrets import FTP_PASS
except ImportError:  # fall back to the environment
    import os
    FTP_PASS = os.environ.get('TH_FTP_PASS', '')
import ftplib

host = 'ftp.timerhaven.com'
user = 'contact@timerhaven.com'
passwd = FTP_PASS

ftp = ftplib.FTP(host, timeout=30)
ftp.login(user, passwd)
ftp.set_pasv(True)

files_to_upload = [
    'unit-converter-de.html',
    'unit-converter-el.html',
    'unit-converter-en.html'
]

for filename in files_to_upload:
    with open(f'C:\\TimerHavenWebsite\\{filename}', 'rb') as f:
        ftp.storbinary(f'STOR {filename}', f)
        print(f"Uploaded {filename}")

ftp.quit()
print("Done!")
