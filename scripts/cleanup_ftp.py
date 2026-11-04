try:  # local credentials file, never committed
    from _secrets import FTP_PASS
except ImportError:  # fall back to the environment
    import os
    FTP_PASS = os.environ.get('TH_FTP_PASS', '')
import ftplib
import os

# CONFIG
FTP_HOST = "newgiftsandgadgets.com"
FTP_USER = "serge@newgiftsandgadgets.com"
FTP_PASS = FTP_PASS

def delete_recursive(ftp, path):
    print(f"Purging {path} ...")
    try:
        ftp.cwd(path)
        items = ftp.nlst()
        for item in items:
            if item in [".", ".."]: continue
            try:
                # Try to enter (check if dir)
                ftp.cwd(item)
                ftp.cwd("..")
                delete_recursive(ftp, item)
            except:
                # Must be a file
                try:
                    ftp.delete(item)
                    print(f"DELETED FILE: {item}")
                except Exception as e:
                    print(f"ERROR DELETING {item}: {e}")
        
        ftp.cwd("..")
        ftp.rmd(path)
        print(f"DELETED DIR: {path}")
    except Exception as e:
        print(f"ERROR PURGING {path}: {e}")

if __name__ == "__main__":
    try:
        ftp = ftplib.FTP()
        ftp.connect(FTP_HOST, 21, timeout=60)
        ftp.login(FTP_USER, FTP_PASS)
        print("Logged in. Cleaning up...")
        
        # Purge problematic directories
        for target in ["comparisons", "audio"]:
            if target in ftp.nlst():
                delete_recursive(ftp, target)
        
        ftp.quit()
        print("\nCleanup Complete. Now run full sync.")
    except Exception as e:
        print(f"Fatal Error: {e}")
