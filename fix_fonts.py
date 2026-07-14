import os
import glob
import re

sections_dir = '/Users/admin/Documents/profile_bich_ngan/src/sections'
for filepath in glob.glob(os.path.join(sections_dir, '*.html')):
    with open(filepath, 'r') as f:
        content = f.read()

    # Decrease h2 clamp sizes
    content = re.sub(r'font-size:\s*clamp\(2rem,\s*5vw,\s*4rem\)', 'font-size: clamp(1.6rem, 3.5vw, 2.8rem)', content)
    content = re.sub(r'font-size:\s*clamp\(2rem,\s*5vw,\s*3rem\)', 'font-size: clamp(1.6rem, 3.5vw, 2.5rem)', content)
    content = re.sub(r'font-size:\s*clamp\(1\.8rem,\s*4vw,\s*3\.5rem\)', 'font-size: clamp(1.4rem, 3vw, 2.5rem)', content)
    content = re.sub(r'font-size:\s*clamp\(1\.8rem,\s*5vw,\s*4rem\)', 'font-size: clamp(1.4rem, 3vw, 2.5rem)', content)
    content = re.sub(r'font-size:\s*clamp\(1\.8rem,\s*4vw,\s*2\.8rem\)', 'font-size: clamp(1.4rem, 3vw, 2.2rem)', content)
    content = re.sub(r'font-size:\s*clamp\(2rem,\s*4vw,\s*3rem\)', 'font-size: clamp(1.5rem, 3vw, 2.5rem)', content)
    
    # Also adjust subtitles if they are 1rem
    # Only for section-subtitle-light
    content = re.sub(r'(class="section-subtitle-light"[\s\S]*?font-size:\s*)1rem', r'\1 0.85rem', content)
    content = re.sub(r'(class="section-subtitle-light"[\s\S]*?font-size:\s*)0\.8rem', r'\1 0.75rem', content)

    with open(filepath, 'w') as f:
        f.write(content)

print("Done replacing fonts.")
