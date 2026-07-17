import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove muted from the template
content = re.sub(
    r'autoplay controls muted playsinline loop',
    'autoplay controls playsinline loop',
    content
)

# 2. Update the play catch block
old_catch = r'// Attempt to play\s*video\.play\(\)\.catch\(e => \{\s*console\.log\(\"Autoplay prevented:\", e\);\s*video\.muted = true;\s*video\.play\(\)\.catch\(err => console\.log\(\"Even muted autoplay failed:\", err\)\);\s*\}\);'
new_catch = r'''// Attempt to play with sound
          video.muted = false;
          video.play().catch(e => {
            console.log("Unmuted autoplay prevented:", e);
            // Leave it paused so user can tap to play with sound
          });'''
content = re.sub(old_catch, new_catch, content)

# 3. Add .vid-wrapper to the querySelectorAll
content = re.sub(
    r"document\.querySelectorAll\('\.vid-thumbnail'\)",
    r"document.querySelectorAll('.vid-thumbnail, .vid-wrapper')",
    content
)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated script.js successfully')
