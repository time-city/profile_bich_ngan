import glob
import re
import os

all_files = glob.glob('src/components/projects/project-*.html')
all_files = [os.path.basename(f) for f in all_files]

video_files = []
has_model_files = []
no_model_files = []

for f in all_files:
    with open(os.path.join('src/components/projects', f), 'r') as file_obj:
        content = file_obj.read()
        if 'vid-thumbnail' in content or '<video' in content:
            video_files.append(f)
        elif 'bento-gallery-6' in content:
            has_model_files.append(f)
        else:
            no_model_files.append(f)

# Sort them just to be deterministic
video_files.sort()
has_model_files.sort()
no_model_files.sort()

# Build the photo array by interleaving has_model and no_model
photo_files = []
max_len = max(len(has_model_files), len(no_model_files))
for i in range(max_len):
    if i < len(has_model_files):
        photo_files.append(has_model_files[i])
    if i < len(no_model_files):
        photo_files.append(no_model_files[i])

# Now interleave videos into photo_files
new_list = []
interval = len(photo_files) / float(len(video_files)) if len(video_files) > 0 else 1

vid_idx = 0
for i, p in enumerate(photo_files):
    new_list.append(p)
    expected_vids = int((i + 1) / interval)
    while vid_idx < expected_vids and vid_idx < len(video_files):
        new_list.append(video_files[vid_idx])
        vid_idx += 1

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
new_content = new_content.replace("?v=17", "?v=18")

with open("index.html", "w") as f:
    f.write(new_content)

print(f"Total files: {len(new_list)}")
print(f"Videos: {len(video_files)}, Has Model: {len(has_model_files)}, No Model: {len(no_model_files)}")
