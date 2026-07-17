import os
import unicodedata
import re

directories = ['./src/sections', './src/components/projects', '.']

def normalize_match(match):
    # match.group(0) is like src="./asset/voice/Dịch Live.mp4"
    # match.group(1) is the quote type (" or ')
    # match.group(2) is the path
    attr = match.group(0).split('=')[0]
    quote = match.group(1)
    path = match.group(2)
    
    # Normalize to NFC
    normalized_path = unicodedata.normalize('NFC', path)
    return f'{attr}={quote}{normalized_path}{quote}'

for d in directories:
    if not os.path.isdir(d): continue
    for root, _, files in os.walk(d):
        for file in files:
            if file.endswith('.html') or file.endswith('.js') or file.endswith('.css'):
                filepath = os.path.join(root, file)
                # Ignore this python script itself and python scripts
                if 'normalize' in filepath or filepath.endswith('.py'):
                    continue
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original = content
                
                # Replace src="", data-video-src="", poster="", data-poster="", url("")
                # Match src="...", src='...'
                content = re.sub(r'\bsrc=(["\'])([^"\']+)\1', normalize_match, content)
                content = re.sub(r'\bdata-video-src=(["\'])([^"\']+)\1', normalize_match, content)
                content = re.sub(r'\bposter=(["\'])([^"\']+)\1', normalize_match, content)
                content = re.sub(r'\bdata-poster=(["\'])([^"\']+)\1', normalize_match, content)
                
                # For url(...) in CSS
                def normalize_url(match):
                    path = match.group(1)
                    normalized_path = unicodedata.normalize('NFC', path)
                    return f'url({normalized_path})'
                content = re.sub(r'\burl\(([^)]+)\)', normalize_url, content)
                
                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Normalized paths in {filepath}")

print("Normalization complete.")
