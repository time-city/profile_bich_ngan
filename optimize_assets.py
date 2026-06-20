import os
import re
from PIL import Image

ASSET_DIR = './asset'
MAX_WIDTH = 1600
QUALITY = 80

EXTENSIONS_TO_CONVERT = ('.jpg', '.jpeg', '.png')
ALL_IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp')

def optimize_image(filepath):
    """
    Opens an image, resizes if width > MAX_WIDTH, and saves as webp.
    Returns the new filepath if converted/optimized, or None if failed.
    """
    try:
        with Image.open(filepath) as img:
            # Convert to RGB if necessary (e.g. RGBA pngs)
            if img.mode in ('RGBA', 'P', 'LA'):
                # For RGBA, we want to preserve transparency in webp, so we keep it RGBA
                pass
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            width, height = img.size
            if width > MAX_WIDTH:
                new_height = int((MAX_WIDTH / width) * height)
                img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
            
            # Determine new filename
            directory, filename = os.path.split(filepath)
            name, ext = os.path.splitext(filename)
            new_filepath = os.path.join(directory, name + '.webp')
            
            # Save as webp
            img.save(new_filepath, 'webp', quality=QUALITY)
            
            # Remove original if it's different and conversion succeeded
            if filepath != new_filepath:
                os.remove(filepath)
            
            return new_filepath
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return None

def process_assets():
    processed_count = 0
    for root, dirs, files in os.walk(ASSET_DIR):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in ALL_IMAGE_EXTENSIONS:
                filepath = os.path.join(root, file)
                print(f"Processing: {filepath}")
                optimize_image(filepath)
                processed_count += 1
    print(f"Processed {processed_count} images.")

def update_codebase():
    """
    Replaces .png, .jpg, .jpeg with .webp in HTML, CSS, JS, PY files.
    """
    target_exts = ('.html', '.css', '.js', '.py')
    # Files/Dirs to ignore
    ignore_files = ['optimize_assets.py']
    
    # Regex to catch .png, .jpg, .jpeg (case insensitive)
    # We want to replace it only when it's likely an extension, e.g. followed by quote, question mark, or space
    pattern = re.compile(r'\.(png|jpg|jpeg)(?=["\'\s?])', re.IGNORECASE)
    
    updated_count = 0
    for root, dirs, files in os.walk('.'):
        # ignore node_modules or .git if any
        if '.git' in root or 'node_modules' in root:
            continue
            
        for file in files:
            if file in ignore_files:
                continue
                
            if file.endswith(target_exts):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = pattern.sub('.webp', content)
                
                # Special case for generate_projects.py where it might have:
                # "LUMIA.png" inside a string that doesn't strictly match the lookahead if not careful,
                # but the regex `(?=["\'\s?])` catches quotes.
                
                # Also handle cases like .endswith(('.jpg', '.png'))
                # We can just blindly replace .png with .webp if we want, but regex is safer.
                # Let's do a more aggressive replace since we want NO jpg/png references anywhere.
                
                # Actually, simple string replace is very effective here since we converted EVERYTHING.
                # But we might replace variable names if they have `.png` which is rare.
                # Let's do a simple replace for all known extensions.
                
                content_replaced = content
                for ext in ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG']:
                    content_replaced = content_replaced.replace(ext, '.webp')
                    
                if content != content_replaced:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content_replaced)
                    print(f"Updated references in: {filepath}")
                    updated_count += 1
                    
    print(f"Updated {updated_count} codebase files.")

if __name__ == '__main__':
    process_assets()
    update_codebase()
    print("Optimization complete!")
