import os
import glob

def rename_files(target_dir):
    # Ensure the path is absolute or relative to current location
    search_path = os.path.join(target_dir, "*.txt")
    
    for old_path in glob.glob(search_path):
        filename = os.path.basename(old_path)
        
        # Check if file matches your specific naming convention
        if filename.startswith(('dimvars-M', 'ndvars-M')):
            new_filename = filename.replace('-M', '-').replace('--', '-')
            new_path = os.path.join(target_dir, new_filename)
            
            try:
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")
            except OSError as e:
                print(f"Error: {e}")