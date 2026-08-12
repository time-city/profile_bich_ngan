import re

old_list = [
    'project-01.html',
    'project-02.html',
    'project-03.html',
    'project-08.html',
    'project-09.html',
    'project-10.html',
    'project-11.html',
    'project-13.html',
    'project-vid-1.html',
    'project-04.html',
    'project-22.html',
    'project-06.html',
    'project-23.html',
    'project-07.html',
    'project-24.html',
    'project-12.html',
    'project-25.html',
    'project-14.html',
    'project-26.html',
    'project-15.html',
    'project-45.html',
    'project-vid-2.html',
    'project-27.html',
    'project-16.html',
    'project-28.html',
    'project-29.html',
    'project-18.html',
    'project-31.html',
    'project-19.html',
    'project-32.html',
    'project-20.html',
    'project-33.html',
    'project-30.html',
    'project-34.html',
    'project-35.html',
    'project-36.html',
    'project-37.html',
    'project-38.html',
    'project-39.html',
    'project-40.html'
]

# extract 36-40
videos = old_list[-5:]
base = old_list[:-5]

# calculate insertion intervals
interval = len(base) // len(videos)

new_list = []
vid_idx = 0
for i, p in enumerate(base):
    new_list.append(p)
    if (i + 1) % interval == 0 and vid_idx < len(videos):
        new_list.append(videos[vid_idx])
        vid_idx += 1

# append any remaining
while vid_idx < len(videos):
    new_list.append(videos[vid_idx])
    vid_idx += 1

out_lines = [f"        '{x}'," for x in new_list]
all_lines = "\n".join(out_lines)
all_lines = all_lines[:-1] # remove last comma

with open("index.html", "r") as f:
    content = f.read()

pattern = re.compile(r"const projectFiles = \[.*?\];", re.DOTALL)
replacement = "const projectFiles = [\n" + all_lines + "\n      ];"
new_content = pattern.sub(replacement, content)

# update cache buster to 15
new_content = new_content.replace("?v=14", "?v=15")

with open("index.html", "w") as f:
    f.write(new_content)

print("Done")
