import os
import re
import subprocess
from pathlib import Path

base_dir = "/Users/admin/Documents/profile_bich_ngan"
html_files = [
    "src/sections/6f-international-events.html",
    "src/sections/6g-domestic-events.html",
    "src/sections/6h-animating-skills.html"
]

for html_file in html_files:
    file_path = os.path.join(base_dir, html_file)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Find all data-video-src
    matches = re.finditer(r'<div class="vid-thumbnail[^>]*data-video-src="([^"]+)"[^>]*>\s*<img src="([^"]+)"', content)
    
    new_content = content
    for match in matches:
        video_src = match.group(1) # e.g. ./asset/voice/PANASONIC.mp4
        current_img_src = match.group(2)
        
        # Resolve real path of video
        # Remove ./ from start
        clean_video_src = video_src[2:] if video_src.startswith("./") else video_src
        real_video_path = os.path.join(base_dir, clean_video_src)
        
        if os.path.exists(real_video_path):
            thumb_name = os.path.splitext(os.path.basename(clean_video_src))[0] + ".webp"
            thumb_dir = os.path.join(base_dir, "asset", "thumbnails")
            os.makedirs(thumb_dir, exist_ok=True)
            real_thumb_path = os.path.join(thumb_dir, thumb_name)
            
            # Generate thumbnail with ffmpeg if it doesn't exist
            if not os.path.exists(real_thumb_path):
                print(f"Generating thumbnail for {clean_video_src} at 00:00:03")
                # Try 3 seconds in, if fail try 1 second
                cmd = ["ffmpeg", "-y", "-ss", "00:00:03", "-i", real_video_path, "-vframes", "1", "-q:v", "2", real_thumb_path]
                res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if res.returncode != 0:
                    cmd = ["ffmpeg", "-y", "-ss", "00:00:01", "-i", real_video_path, "-vframes", "1", "-q:v", "2", real_thumb_path]
                    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Replace img src in html
            new_img_src = f"./asset/thumbnails/{thumb_name}"
            # Replace exactly this img tag
            old_tag = f'<img src="{current_img_src}"'
            new_tag = f'<img src="{new_img_src}"'
            
            # We need to replace the specific img src inside this vid-thumbnail div
            # To be safe, we use re.sub on the specific block
            block_to_replace = match.group(0)
            new_block = block_to_replace.replace(f'"{current_img_src}"', f'"{new_img_src}"')
            new_content = new_content.replace(block_to_replace, new_block)
        else:
            print(f"Video not found: {real_video_path}")

    # Write back
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        print(f"Updated {html_file}")
