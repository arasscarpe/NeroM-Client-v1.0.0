import os
import sys
import ctypes
import time
import string

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def show_error_popup(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 16)

def get_drives():
    drives = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(f"{letter}:\\")
        bitmask >>= 1
    return drives

def scan_files():
    targets = ["neo_macros", "macros", "macro", "nerom", "neromacros"]
    found_files = []
    all_drives = get_drives()

    print(f"[*] Scanning all drives: {', '.join(all_drives)}")
    
    for drive in all_drives:
        for root, dirs, files in os.walk(drive):
            if any(x in root for x in ["Windows", "WinSxS", "Microsoft", "$Recycle.Bin"]):
                continue
            
            for file in files:
                if file.lower().endswith(".exe"):
                    if any(t in file.lower() for t in targets):
                        full_path = os.path.join(root, file)
                        found_files.append(full_path)
                        print(f"[!] Found: {file}")
            
    return found_files

def remove_shortcuts(exe_name):
    base_name = os.path.splitext(exe_name)[0]
    common_paths = [
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/AppData/Roaming/Microsoft/Windows/Start Menu/Programs"),
        "C:\\Users\\Public\\Desktop"
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            for item in os.listdir(path):
                if item.lower().startswith(base_name.lower()) and item.lower().endswith(".lnk"):
                    try:
                        os.remove(os.path.join(path, item))
                        print(f"[+] Shortcut removed: {item}")
                    except:
                        pass

def kill_and_delete(file_path):
    file_name = os.path.basename(file_path)
    print(f"\n[*] Terminating: {file_name}")
    os.system(f"taskkill /F /T /IM {file_name} >nul 2>&1")
    time.sleep(1)
    
    try:
        os.remove(file_path)
        print(f"[SUCCESS] {file_name} permanently deleted.")
        remove_shortcuts(file_name)
    except Exception:
        print(f"[!] ERROR: Access Denied for {file_name}")
        show_error_popup("Delete Failed", f"Access Denied: {file_name}")

def main():
    os.system("title Nero Macros Deleter")
    
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    print("--- Nero Macros Deleter ---")
    
    found = scan_files()
    
    if not found:
        print("\n[-] No macro files found on the entire system.")
    else:
        print(f"\n[+] Results ({len(found)}):")
        for i, path in enumerate(found, 1):
            print(f"{i} = {path}")

        print("\n[?] Choice: Enter Number, 'A' for All, or 'Q' to Quit.")
        choice = input("Select: ").strip().upper()

        if choice == 'A':
            for p in found: kill_and_delete(p)
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(found):
                kill_and_delete(found[idx])

    print("\n--- Finished ---")
    input("Press ENTER to exit...")

if __name__ == "__main__":
    main()
