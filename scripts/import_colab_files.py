import os
import shutil
import glob
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def main():
    # Detect the Windows user home and Downloads folder
    user_home = os.path.expanduser("~")
    downloads_dir = os.path.join(user_home, "Downloads")
    
    # Define files to find and where they should go
    files_to_import = [
        {
            "filename": "astronet_best.h5",
            "destination": "models/astronet_best.h5"
        },
        {
            "filename": "training_log_advanced.csv",
            "destination": "outputs/training_log_advanced.csv"
        }
    ]
    
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    log.info(f"Scanning local Downloads folder: {downloads_dir}")
    
    imported_count = 0
    for item in files_to_import:
        filename = item["filename"]
        dest_rel = item["destination"]
        dest_abs = os.path.join(project_root, dest_rel)
        
        # Handle cases where multiple downloads exist (e.g., astronet_best (1).h5)
        # Search using glob pattern
        name_part, ext_part = os.path.splitext(filename)
        search_pattern = os.path.join(downloads_dir, f"{name_part}*{ext_part}")
        matches = glob.glob(search_pattern)
        
        if not matches:
            log.warning(f"❌ File '{filename}' not found in Downloads folder.")
            continue
            
        # Get the latest modified file (most recent download)
        latest_file = max(matches, key=os.path.getmtime)
        log.info(f"Found match: {latest_file} (Modified: {os.path.getmtime(latest_file)})")
        
        # Ensure destination directory exists
        os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
        
        # Copy file
        try:
            shutil.copy2(latest_file, dest_abs)
            log.info(f"✅ Imported to: {dest_rel}")
            imported_count += 1
        except Exception as e:
            log.error(f"Failed to copy {latest_file} to {dest_abs}: {e}")
            
    if imported_count == len(files_to_import):
        log.info("🎉 All Colab files imported successfully!")
    elif imported_count > 0:
        log.info(f"Imported {imported_count}/{len(files_to_import)} files.")
    else:
        log.warning("No files were imported. Make sure you have downloaded them from Colab.")

if __name__ == "__main__":
    main()
