try:  # local credentials file, never committed
    from _secrets import FTP_PASS
except ImportError:  # fall back to the environment
    import os
    FTP_PASS = os.environ.get('TH_FTP_PASS', '')
import ftplib

def test_ftp():
    hosts_to_try = ['ftp.timerhaven.com', 'timerhaven.com']
    user = 'contact@timerhaven.com'
    passwd = FTP_PASS
    
    for host in hosts_to_try:
        print(f"Trying host: {host}")
        try:
            ftp = ftplib.FTP(host, timeout=10)
            ftp.login(user, passwd)
            print(f"Successfully logged in to {host}!")
            print("Current directory:", ftp.pwd())
            print("Directory listing:")
            ftp.retrlines('LIST')
            ftp.quit()
            return host
        except Exception as e:
            print(f"Failed to connect to {host}: {e}")
            
    return None

test_ftp()
