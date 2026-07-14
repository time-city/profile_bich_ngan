import os
import re
from PIL import Image

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
    
    # We will find all <div class="vid-thumbnail..." data-video-src="...">
    matches = list(re.finditer(r'<div class="vid-thumbnail([^"]*)"\s*data-video-src="([^"]+)"', content))
    
    new_content = content
    for match in matches:
        classes = match.group(1)
        video_src = match.group(2)
        
        # Determine thumbnail path
        clean_video_src = video_src[2:] if video_src.startswith("./") else video_src
        thumb_name = os.path.splitext(os.path.basename(clean_video_src))[0] + ".webp"
        thumb_path = os.path.join(base_dir, "asset", "thumbnails", thumb_name)
        
        if os.path.exists(thumb_path):
            try:
                with Image.open(thumb_path) as img:
                    width, height = img.size
                    
                    is_vertical = height > width
                    has_class = "vid-vertical" in classes
                    
                    if is_vertical and not has_class:
                        print(f"Adding vid-vertical to {thumb_name}")
                        # Replace exact match
                        old_str = f'<div class="vid-thumbnail{classes}" data-video-src="{video_src}"'
                        new_str = f'<div class="vid-thumbnail{classes} vid-vertical" data-video-src="{video_src}"'
                        new_content = new_content.replace(old_str, new_str)
                    elif not is_vertical and has_class:
                        print(f"Removing vid-vertical from {thumb_name}")
                        old_str = f'<div class="vid-thumbnail{classes}" data-video-src="{video_src}"'
                        new_classes = classes.replace(" vid-vertical", "").replace("vid-vertical", "")
                        new_str = f'<div class="vid-thumbnail{new_classes}" data-video-src="{video_src}"'
                        new_content = new_content.replace(old_str, new_str)
            except Exception as e:
                print(f"Error reading {thumb_path}: {e}")
                
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        print(f"Updated {html_file}")
