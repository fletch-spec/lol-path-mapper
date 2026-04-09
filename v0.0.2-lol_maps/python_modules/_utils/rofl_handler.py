import os
import shutil

def find_files(self, directory):
    """Find .rofl replay files in the specified directory."""
    rofl_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".rofl"):
                rofl_files.append(os.path.join(root, file))
    return rofl_files

def save(self, path, PRINT=True):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return

    if not os.path.isfile(path):
        print(f"Path is not a file: {path}")
        return

    dest_dir = os.path.join(self.cache_dir, "replay_files")
    os.makedirs(dest_dir, exist_ok=True)

    filename = os.path.basename(path)
    dest_path = os.path.join(dest_dir, filename)

    # if the file already exists, skip copying
    if os.path.exists(dest_path):
        if PRINT:
            print(f"Replay file already exists: {dest_path}")
        return 0  # Indicate that the file was skipped
    try:
        shutil.copy(path, dest_path)
        print(f"Saved replay file to: {dest_path}")
        return dest_path
    except Exception as e:
        print(f"Error saving replay file: {e}")
        return 1

def batch_save(self, directory):
    """Find and save all .rofl files from the specified directory."""
    rofl_files = self.find_rofl_files(directory)
    if not rofl_files:
        print(f"No .rofl files found in: {directory}")
        return
    saved, skipped = 0, 0
    for path in rofl_files:
        try:
            result = self.save_rofl(path, PRINT=False)
            if result == 0:
                skipped += 1
            elif result == path:
                saved += 1
            elif result == 1:
                print(f"Failed to save: {path}")
        except Exception as e:
            print(f"Error processing {path}: {e}")
    print(f"Batch save complete: {saved} saved, {skipped} skipped.")
