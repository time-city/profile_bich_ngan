import os
import re

html_dir = './src/sections'
js_file = './script.js'

images = [
    "./asset/portrait/image copy 2.webp",
    "./asset/portrait/image copy 3.webp",
    "./asset/portrait/image copy 4.webp",
    "./asset/portrait/image copy.webp",
    "./asset/portrait/image.webp"
]

img_idx = 0

def get_next_img():
    global img_idx
    img = images[img_idx]
    img_idx = (img_idx + 1) % len(images)
    return img

for root, _, files in os.walk(html_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Replace poster in <video> tags
            # Find all <video ...>
            def repl_video(match):
                img = get_next_img()
                tag = match.group(0)
                if 'poster=' in tag:
                    tag = re.sub(r'poster="[^"]*"', f'poster="{img}"', tag)
                else:
                    tag = tag.replace('<video ', f'<video poster="{img}" ')
                return tag
            
            content = re.sub(r'<video[^>]+>', repl_video, content)
            
            # Replace thumbnails and add data-poster
            # Need to parse 
            # <div class="... vid-thumbnail ..." data-video-src="...">
            #   <img src="..." alt="...">
            
            # regex to find vid-thumbnail div and its img
            # It's multiline, so we can use a more general approach or simple string replacement.
            # Let's find `<div[^>]*class="[^"]*vid-thumbnail[^"]*"[^>]*data-video-src="[^"]*"[^>]*>`
            # and then the following `<img src="[^"]*"`
            
            def repl_thumbnail(match):
                div_tag = match.group(1)
                img_tag = match.group(2)
                img = get_next_img()
                
                # Add or replace data-poster in div_tag
                if 'data-poster=' in div_tag:
                    div_tag = re.sub(r'data-poster="[^"]*"', f'data-poster="{img}"', div_tag)
                else:
                    div_tag = div_tag.replace('data-video-src=', f'data-poster="{img}" data-video-src=')
                
                # Replace src in img_tag
                img_tag = re.sub(r'src="[^"]*"', f'src="{img}"', img_tag)
                
                return div_tag + img_tag

            content = re.sub(r'(<div[^>]*class="[^"]*vid-thumbnail[^"]*"[^>]*data-video-src="[^"]*"[^>]*>)\s*(<img[^>]*src="[^"]*"[^>]*>)', repl_thumbnail, content)

            # Some might just have `data-video-src` on multiple lines, so we might need a more robust approach if it fails.
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated {filepath}")

# Update script.js to use data-poster
with open(js_file, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Replace: const videoHTML = `<video src="${src}" autoplay controls playsinline style="width:100%; height:100%; object-fit:cover; border-radius:8px; background:#000;"></video>`;
# With: const posterSrc = thumbContainer.getAttribute('data-poster') || '';
# const videoHTML = `<video src="${src}" poster="${posterSrc}" autoplay controls playsinline style="width:100%; height:100%; object-fit:cover; border-radius:8px; background:#000;"></video>`;

if 'const posterSrc = thumbContainer.getAttribute(\'data-poster\') || \'\';' not in js_content:
    # First modal instance
    js_content = re.sub(
        r'(const videoHTML = `<video src="\$\{src\}" autoplay controls playsinline style="width:100%; height:100%; object-fit:cover; border-radius:8px; background:#000;"></video>`;)',
        r"const posterSrc = thumbContainer.getAttribute('data-poster') || '';\n      const videoHTML = `<video src=\"${src}\" poster=\"${posterSrc}\" autoplay controls playsinline style=\"width:100%; height:100%; object-fit:cover; border-radius:8px; background:#000;\"></video>`;",
        js_content
    )
    # Second autoplay instance
    js_content = re.sub(
        r'(const videoHTML = `<video src="\$\{src\}" autoplay controls muted playsinline loop style="width:100%; height:100%; object-fit:cover; border-radius:8px; background:#000;"></video>`;)',
        r"const posterSrc = thumbContainer.getAttribute('data-poster') || '';\n            const videoHTML = `<video src=\"${src}\" poster=\"${posterSrc}\" autoplay controls muted playsinline loop style=\"width:100%; height:100%; object-fit:cover; border-radius:8px; background:#000;\"></video>`;",
        js_content
    )
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"Updated {js_file}")
