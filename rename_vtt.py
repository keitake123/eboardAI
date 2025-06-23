import os
import re

# Function to extract number from filename
def extract_number(filename):
    match = re.search(r'(\d+)', filename)
    return match.group(1) if match else None

# Get all VTT files in current directory
vtt_files = [f for f in os.listdir('.') if f.endswith('.vtt')]

# Process each VTT file
for vtt_file in vtt_files:
    number = extract_number(vtt_file)
    if number:
        new_name = f"{number}.vtt"
        # If multiple files have the same number, keep the larger one (likely more complete)
        if os.path.exists(new_name):
            if os.path.getsize(vtt_file) > os.path.getsize(new_name):
                os.remove(new_name)
                os.rename(vtt_file, new_name)
                print(f"Replaced {new_name} with larger file {vtt_file}")
            else:
                os.remove(vtt_file)
                print(f"Kept existing {new_name}, removed smaller file {vtt_file}")
        else:
            os.rename(vtt_file, new_name)
            print(f"Renamed {vtt_file} to {new_name}")
    else:
        print(f"Could not extract number from {vtt_file}")

print("\nRenaming complete!") 