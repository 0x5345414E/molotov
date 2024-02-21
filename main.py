import os, platform
import platform
if platform.system() == "Windows":
    import winshell
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from subprocess import call
from tqdm import tqdm
import emoji, time

def loading_bar(duration=10):
    for i in tqdm(range(duration), desc="🚀 Cleaning in progress..."):
        time.sleep(1)  # Simulating work

def get_os_type():
    os_type = platform.system()
    return os_type


def confirm_and_delete_files(files):
    """Ask for confirmation before deleting files."""
    if not files:
        print("No old files found to delete.")
        return

    print(f"Found {len(files)} files to delete. Proceed? (y/n):")
    for file in files:
        print(file)
    if input().lower() == "y":
        for file in tqdm(files, desc="Deleting files"):
            try:
                os.remove(file)
                print(f"Successfully deleted {file}")
            except Exception as e:
                print(f"Failed to delete {file}: {e}")
    else:
        print("Deletion canceled.")


def clean_os_specific_folders(temp_folders):
    """Clean OS-specific temp folders."""
    for folder in temp_folders:
        old_files = find_old_files(folder, days=365)  # Example: Adjust 'days' as needed
        confirm_and_delete_files(old_files)


def find_old_files(directory, days=365):
    """Find files not accessed in the last 'days' days."""
    now = datetime.now()
    old_files = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            filepath = Path(root) / name
            if now - datetime.fromtimestamp(filepath.stat().st_atime) > timedelta(
                days=days
            ):
                old_files.append(filepath)
    return old_files

def delete_files(files):
    """Delete files and show progress."""
    for file in tqdm(files, desc="🔥 Deleting files"):
        try:
            os.remove(file)
            print(
                emoji.emojize(f":fire: Successfully deleted {file}", use_aliases=True)
            )
        except Exception as e:
            print(
                emoji.emojize(
                    f":warning: Failed to delete {file}: {e}", use_aliases=True
                )
            )


def clean_windows():
    temp_folders = [os.environ["TEMP"], os.environ["WINDIR"] + "\\Prefetch"]

    print("🧹 Cleaning Windows temp files...")
    for folder in temp_folders:
        for item in Path(folder).glob("*"):
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
                print(f"✅ Removed: {item}")
            except Exception as e:
                print(f"❌ Could not remove {item}: {e}")

    print("🧹 Emptying Recycle Bin...")
    try:
        # Correctly use winshell to empty the Recycle Bin
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
        print("✅ Recycle Bin emptied successfully!")
    except Exception as e:
        print(f"❌ Failed to empty Recycle Bin: {e}")


def clean_linux():
    temp_folders = ["/tmp", os.path.expanduser("~/.cache")]
    clean_os_specific_folders(temp_folders)

    print("🧹 Cleaning Linux temp files...")
    for folder in temp_folders:
        for item in Path(folder).glob("*"):
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
                print(f"✅ Removed: {item}")
            except Exception as e:
                print(f"❌ Could not remove {item}: {e}")

    print("🧹 Purging old packages with apt...")
    call(["sudo", "apt-get", "autoremove", "-y"])
    call(["sudo", "apt-get", "autoclean", "-y"])
    print("✅ Old packages purged successfully!")


def clean_macos():
    temp_folders = ["/tmp", os.path.expanduser("~/.cache")]
    clean_os_specific_folders(temp_folders)

    print("🧹 Cleaning macOS temp files...")
    for folder in temp_folders:
        for item in Path(folder).glob("*"):
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
                print(f"✅ Removed: {item}")
            except Exception as e:
                print(f"❌ Could not remove {item}: {e}")

    print("🧹 Emptying Trash...")
    try:
        trash = os.path.expanduser("~/.Trash")
        for item in Path(trash).glob("*"):
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
        print("✅ Trash emptied successfully!")
    except Exception as e:
        print(f"❌ Failed to empty Trash: {e}")

def main():
    os_type = get_os_type()
    print(f"Detected OS: {os_type}")

    if os_type == "Windows":
        clean_windows()
    elif os_type == "Linux":
        clean_linux()
    elif os_type == "Darwin":
        clean_macos()
    else:
        print("Unsupported OS. Molotov currently supports Windows, Linux, and macOS.")

if __name__ == "__main__":
    main()
