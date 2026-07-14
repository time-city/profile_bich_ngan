import os
from PIL import Image
import re

components_dir = "/Users/admin/Documents/profile_bich_ngan/src/components/projects"

for file_name in os.listdir(components_dir):
    if not file_name.startswith("project-") or not file_name.endswith(".html"):
        continue
        
    file_path = os.path.join(components_dir, file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    # Find all <img src="..."> inside gallery
    # Looking for <img src="./asset/event/.../..." alt="..." class="gallery-img">
    matches = re.findall(r'<img src="(\./asset/event/[^"]+)"[^>]*class="gallery-img"', html)
    if len(matches) >= 5:
        bottom_img_src = matches[4]
        bottom_img_src = bottom_img_src.replace("./asset", "/Users/admin/Documents/profile_bich_ngan/asset")
        if not os.path.exists(bottom_img_src):
            continue
            
        try:
            with Image.open(bottom_img_src) as img:
                width, height = img.size
                if height > width: # It's vertical!
                    print(f"FOUND PROJECT: {file_name}")
                    print(f"Bottom image is VERTICAL: {bottom_img_src} ({width}x{height})")
                    
                    # check first 4
                    for i in range(4):
                        src = matches[i].replace("./asset", "/Users/admin/Documents/profile_bich_ngan/asset")
                        if os.path.exists(src):
                            with Image.open(src) as top_img:
                                tw, th = top_img.size
                                if tw > th: # Horizontal!
                                    print(f"  Top image {i} is HORIZONTAL: {src} ({tw}x{th})")
                                    
        except Exception as e:
            pass
