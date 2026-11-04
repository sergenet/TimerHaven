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

with open(r'C:\TimerHavenWebsite\currency-en.html', 'rb') as f:
    ftp.storbinary('STOR currency-en.html', f)

ftp.quit()
print("Uploaded currency-en.html")
