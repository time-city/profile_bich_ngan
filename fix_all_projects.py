import glob
import re
import os

all_files = glob.glob('src/components/projects/project-*.html')
all_files = [os.path.basename(f) for f in all_files]

video_files = []
photo_files = []

for f in all_files:
    with open(os.path.join('src/components/projects', f), 'r') as file_obj:
        content = file_obj.read()
        if 'vid-thumbnail' in content or '<video' in content:
            video_files.append(f)
        else:
            photo_files.append(f)

# Sort them just to be deterministic
video_files.sort()
photo_files.sort()

# Interleave
# We want to distribute video_files evenly across photo_files
new_list = []
interval = len(photo_files) / float(len(video_files))

vid_idx = 0
for i, p in enumerate(photo_files):
    new_list.append(p)
    # Whenever the current index crosses the interval threshold, insert a video
    expected_vids = int((i + 1) / interval)
    while vid_idx < expected_vids and vid_idx < len(video_files):
        new_list.append(video_files[vid_idx])
        vid_idx += 1

# Add any remaining videos
while vid_idx < len(video_files):
    new_list.append(video_files[vid_idx])
    vid_idx += 1

out_lines = [f"        '{x}'," for x in new_list]
all_lines = "\n".join(out_lines)
all_lines = all_lines[:-1] # remove last comma

with open("index.html", "r") as f:
    content = f.read()

pattern = re.compile(r"const projectFiles = \[.*?\];", re.DOTALL)
replacement = "const projectFiles = [\n" + all_lines + "\n      ];"
new_content = pattern.sub(replacement, content)

# update cache buster
new_content = new_content.replace("?v=15", "?v=16")

with open("index.html", "w") as f:
    f.write(new_content)

print(f"Total files: {len(new_list)}")
print(f"Videos: {len(video_files)}, Photos: {len(photo_files)}")
