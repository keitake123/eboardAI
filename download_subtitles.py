import csv
import subprocess
import os
import re

def clean_youtube_url(url):
    # Remove trailing slash if present
    url = url.strip('/')
    # Extract video ID if it's a full URL
    if 'youtube.com/watch?v=' in url:
        video_id = url.split('watch?v=')[1].split('&')[0]
        return f'https://www.youtube.com/watch?v={video_id}'
    return url

# Create directory for VTT files if it doesn't exist
vtt_dir = 'vtt_files'
if not os.path.exists(vtt_dir):
    os.makedirs(vtt_dir)

# Read the CSV file
with open('eboardに公開されている動画の一覧 - シート2.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        try:
            # Get the ID (6th column) and YouTube URL (last column)
            video_id = row[5].strip()
            youtube_url = clean_youtube_url(row[-1])
            
            print(f"Downloading subtitles for video ID {video_id} from {youtube_url}")
            
            # Use local yt-dlp binary with updated options
            command = [
                './yt-dlp',
                '--skip-download',      # Don't download the video
                '--write-sub',          # Write subtitles
                '--write-auto-sub',     # Write automatic subtitles if manual not available
                '--sub-format', 'vtt',  # Get VTT format
                '--sub-lang', 'ja',     # Get Japanese subtitles
                '--format', 'best',     # Use best available format
                '--prefer-free-formats',# Prefer non-DRM formats
                '--no-check-certificates',
                '--ignore-errors',      # Continue on download errors
                '--no-warnings',        # Suppress warnings
                '--extractor-args', 'youtube:player_client=android',  # Try android client
                youtube_url
            ]
            
            subprocess.run(command, check=True)
            
            # Process downloaded VTT files
            largest_size = 0
            largest_file = None
            
            # Find the largest VTT file
            for file in os.listdir('.'):
                if file.endswith('.vtt'):
                    size = os.path.getsize(file)
                    if size > largest_size:
                        if largest_file:  # Remove smaller file if exists
                            os.remove(largest_file)
                        largest_size = size
                        largest_file = file
                    else:  # Remove smaller file
                        os.remove(file)
            
            # Move the largest file to vtt_dir with just the number
            if largest_file:
                new_name = f"{video_id}.vtt"
                target_path = os.path.join(vtt_dir, new_name)
                
                if os.path.exists(target_path):  # If a file with this name already exists in vtt_dir
                    if os.path.getsize(largest_file) > os.path.getsize(target_path):
                        os.remove(target_path)  # Remove existing if new one is larger
                        os.rename(largest_file, target_path)
                        print(f"Replaced {new_name} with larger file in {vtt_dir}")
                    else:
                        os.remove(largest_file)  # Keep existing if it's larger
                        print(f"Kept existing {new_name} in {vtt_dir} (larger)")
                else:
                    os.rename(largest_file, target_path)
                    print(f"Saved subtitle as {new_name} in {vtt_dir}")
                    
        except Exception as e:
            print(f"Error processing row: {e}")
            continue

print(f"\nDownload complete! All files are saved in the {vtt_dir} directory") 