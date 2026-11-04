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

def list_remote(ftp, path="."):
    print(f"\n--- LISTING: {path} ---")
    items = ftp.nlst()
    for item in items:
        # Check if directory
        try:
            ftp.cwd(item)
            print(f"[DIR]  {item}")
            ftp.cwd("..")
        except:
            # Get size for files
            try:
                size = ftp.size(item)
                print(f"[FILE] {item} ({size} bytes)")
            except:
                print(f"[FILE] {item} (Unknown size)")

if __name__ == "__main__":
    try:
        ftp = ftplib.FTP()
        ftp.connect(FTP_HOST, 21, timeout=30)
        ftp.login(FTP_USER, FTP_PASS)
        print("Logged in. FTP Root:", ftp.pwd())
        
        list_remote(ftp)
        
        if "comparisons" in ftp.nlst():
            ftp.cwd("comparisons")
            list_remote(ftp, "comparisons")
            ftp.cwd("..")
            
        ftp.quit()
    except Exception as e:
        print(f"Error: {e}")
