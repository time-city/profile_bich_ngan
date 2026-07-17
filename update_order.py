import re

order = [
    "project-01", "project-04", "project-02", "project-05", "project-03",
    "project-06", "project-08", "project-07", "project-09", "project-14",
    "project-10", "project-15", "project-11", "project-16", "project-12",
    "project-17", "project-13", "project-18", "project-21", "project-19",
    "project-22", "project-20", "project-23", "project-30", "project-24",
    "project-35", "project-25", "project-26", "project-27", "project-28",
    "project-29", "project-31", "project-32", "project-33", "project-34"
]

has_model = ["project-01", "project-02", "project-03", "project-08", "project-09", "project-10", "project-11", "project-13", "project-21", "project-22", "project-23", "project-24", "project-25", "project-26", "project-27", "project-28", "project-29", "project-31", "project-32", "project-33", "project-34"]
no_model = ["project-04", "project-05", "project-06", "project-07", "project-12", "project-14", "project-15", "project-16", "project-17", "project-18", "project-19", "project-20", "project-30", "project-35"]

# Generate new order
new_order = []
m_list = list(has_model)
n_list = list(no_model)

# Push the excess M to the top
excess_m = len(m_list) - len(n_list) # 7
for _ in range(excess_m):
    new_order.append(m_list.pop(0))

# Now alternate M and N
while m_list or n_list:
    if m_list:
        new_order.append(m_list.pop(0))
    if n_list:
        new_order.append(n_list.pop(0))

# format output
out_lines = []
for p in new_order:
    out_lines.append(f"        '{p}.html',")

# Now read index.html
with open("index.html", "r") as f:
    content = f.read()

# Replace the projectFiles array
pattern = re.compile(r"const projectFiles = \[.*?\];", re.DOTALL)
# join lines, removing the comma from the last element
all_lines = "\n".join(out_lines)
all_lines = all_lines[:-1] # remove last comma
replacement = "const projectFiles = [\n" + all_lines + "\n      ];"
new_content = pattern.sub(replacement, content)

with open("index.html", "w") as f:
    f.write(new_content)
print("Updated index.html")
