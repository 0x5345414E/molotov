import os
import platform
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from subprocess import call
from tqdm import tqdm
import time

# Conditional import for Windows
if platform.system() == "Windows":
    import winshell


def get_os_type():
    """Detect the operating system."""
    return platform.system()


def find_old_files(directory, days=365):
    """Find files not accessed in the last 'days' days."""
    now = datetime.now()
    old_files = []
    for root, _, files in os.walk(directory):
        for name in files:
            filepath = Path(root) / name
            try:
                if now - datetime.fromtimestamp(filepath.stat().st_atime) > timedelta(
                    days=days
                ):
                    old_files.append(filepath)
            except FileNotFoundError:
                print(f"Warning: {filepath} was not found or has been deleted.")
    return old_files


def menu_prompt(files):
    """Ask for confirmation before deleting files."""
    if not files:
        print("No old files found to delete.")
        return False
    print(f"Found {len(files)} files to delete. Proceed with deletion? (y/n):")
    user_input = input().lower()
    if user_input == "y":
        return True
    else:
        print("Deletion canceled.")
        return False


def confirm_and_delete_files(files):
    """Delete files after user confirmation."""
    for file in tqdm(files, desc="🔥 Deleting files... 🔥", unit="file"):
        try:
            time.sleep(0.5)  # Simulate a short delay
            os.remove(file)
            print(f"🔥 Successfully burned {file}")
        except Exception as e:
            print(f"❌ Failed to burn {file}: {e}")


def clean_folders_and_ask_confirmation(temp_folders):
    """Gather old files, ask for confirmation, and delete if confirmed."""
    old_files = []
    for folder in temp_folders:
        old_files.extend(find_old_files(folder, days=365))  # Adjust 'days' as needed
    if old_files and menu_prompt(old_files):
        confirm_and_delete_files(old_files)


def clean_windows():
    """Clean temporary files and empty the Recycle Bin on Windows."""
    temp_folders = [os.environ["TEMP"], os.environ["WINDIR"] + "\\Prefetch"]
    clean_folders_and_ask_confirmation(temp_folders)
    print("🧹 Emptying Recycle Bin...")
    try:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
        print("🔥 Recycle Bin was burned successfully!")
    except Exception as e:
        print(f"❌Failed to burn Recycle Bin: {e}")


def clean_linux():
    """Clean temporary files and purge old packages on Linux."""
    temp_folders = ["/tmp", os.path.expanduser("~/.cache")]
    clean_folders_and_ask_confirmation(temp_folders)
    print("🔥 Burning old packages with apt...")
    call(["sudo", "apt-get", "autoremove", "-y"])
    call(["sudo", "apt-get", "autoclean", "-y"])
    print("🔥 Old packages purged successfully!")


def clean_macos():
    """Clean temporary files and empty the Trash on macOS."""
    temp_folders = ["/tmp", os.path.expanduser("~/.cache")]
    clean_folders_and_ask_confirmation(temp_folders)
    print("🔥 Emptying Trash...")
    try:
        trash = os.path.expanduser("~/.Trash")
        for item in Path(trash).glob("*"):
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
        print("🔥 Trash burned successfully!")
    except Exception as e:
        print(f"❌Failed to burn Trash: {e}")


def main():
    """Main function to detect OS and perform cleaning based on user confirmation."""
    os_type = get_os_type()
    print(f"Detected OS: {os_type}")

    if os_type == "Windows":
        clean_windows()
    elif os_type == "Linux":
        clean_linux()
    elif os_type == "Darwin":  # macOS
        clean_macos()
    else:
        print("Unsupported OS. Molotov currently supports Windows, Linux, and macOS.")


if __name__ == "__main__":
    main()
