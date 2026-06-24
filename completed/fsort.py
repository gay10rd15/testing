import shutil
from pathlib import Path
import argparse

# Define file extensions
video = (".mp4", ".mov", ".webm")
audio = (".mp3", ".flac", ".wav")
img = (".jpg", ".png", ".jpeg", ".svg")
prints = (".stl", ".3mf")

# Define destination directories
home = Path.home()
music = home / "Music"
movies = home / "Movies"
screenshots_dir = home / "screenshots"
pictures = home / "pictures"
prints_dir = home / "prints"

# Ensure destination directories exist
destinations = [music, movies, screenshots_dir, pictures, prints_dir]
for dest in destinations:
    dest.mkdir(parents=True, exist_ok=True)

# Resolve protected paths fully to ensure robust matching
protected_paths = {
    str(Path('~/testing/.venv').expanduser().resolve()),
    str(Path("~/testing/Calc").expanduser().resolve()),
}

def get_unique_path(destination: Path, filename: str) -> Path:
    dest_path = destination / filename
    if not dest_path.exists():
        return dest_path
    
    stem = Path(filename).stem
    suffix = Path(filename).suffix
    counter = 1
    
    while (destination / f"{stem}_{counter}{suffix}").exists():
        counter += 1
    
    return destination / f"{stem}_{counter}{suffix}"   

def get_target_directory(item: Path) -> Path:
    """Determine target directory based on extension, path safety, and current location."""
    resolved_path = str(item.resolve())
    
    # 1. Skip if the file resides inside any protected path string
    for protected in protected_paths:
        if protected in resolved_path:
            return None
            
    # 2. Skip if the file is already sitting inside any of our destination directories
    for dest in destinations:
        if dest.resolve() in item.parents:
            return None

    ext = item.suffix.lower()
    name = item.name

    if ext in audio:
        return music
    elif ext in video:
        return movies
    elif ext in img and "screenshot" in name.lower():
        return screenshots_dir
    elif ext in img:
        return pictures
    elif ext in prints:
        return prints_dir
    return None

def clean_dir_recursively(final_dir: Path):
    print(f"Recursively cleaning: {final_dir}")
    # Convert generator to list to freeze state and prevent FileNotFoundError mid-loop
    items = list(final_dir.rglob("*"))
    for item in items:
        if not item.is_file():
            continue
        
        target_dir = get_target_directory(item)
        if target_dir:
            target = get_unique_path(target_dir, item.name)
            if target != item:
                shutil.move(str(item), str(target))
                print(f"Moved ({item.suffix.lower()}) to: {target}")

def clean_dir(final_dir: Path):
    print(f"Cleaning: {final_dir}")
    for item in list(final_dir.iterdir()):
        if not item.is_file():
            continue
        
        target_dir = get_target_directory(item)
        if target_dir:
            target = get_unique_path(target_dir, item.name)
            if target != item:
                shutil.move(str(item), str(target))
                print(f"Moved ({item.suffix.lower()}): {item.name}")

def dry_run(final_dir: Path):
    print(f"Dry run - would clean: {final_dir}")
    for item in final_dir.iterdir():
        if not item.is_file():
            continue
        
        target_dir = get_target_directory(item)
        if target_dir:
            target = get_unique_path(target_dir, item.name)
            if target != item:
                print(f"Would move ({item.suffix.lower()}): {item.name} → {target}")

def dry_run_recursively(final_dir: Path):
    print(f"Dry run - would recursively clean: {final_dir}")
    for item in final_dir.rglob("*"):
        if not item.is_file():
            continue
        
        target_dir = get_target_directory(item)
        if target_dir:
            target = get_unique_path(target_dir, item.name)
            if target != item:
                print(f"Would move ({item.suffix.lower()}): {item} → {target}")

# 1. Inherit from 'Exception' and fix the '__init__' spelling
class PathError(Exception):
    def __init__(self, message="the path selected does not exist"):
        # Pass the message variable directly to the parent class
        super().__init__(message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sort files into media folders safely.")
    parser.add_argument("path", help="Path to the directory to clean")
    parser.add_argument("-r", "--recursive", action='store_true', 
                       help="Sort files recursively")
    parser.add_argument("-d", "--dry-run", action='store_true', 
                       help="Show which files would be moved without moving them")
    
    args = parser.parse_args()
    target_path = Path(args.path).expanduser().resolve()
    
    if not target_path.exists() or not target_path.is_dir():
        raise PathError
        (f"Error: {target_path} is not a valid directory.")
        exit(1)

    if args.dry_run:
        if args.recursive:
            dry_run_recursively(target_path)
        else:
            dry_run(target_path)
    else:
        if args.recursive:
            clean_dir_recursively(target_path)
        else:
            clean_dir(target_path)
