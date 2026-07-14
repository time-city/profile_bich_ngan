import os
def find_feature_model(title, folder):
    mapping = {
        "Menarini - kỷ niệm thành lập - ảnh và clip": "Menarini.webp",
        "PANASONIC ảnh - clip": "panasonic.png",
        "TCL": "TCL.webp",
    }
    if folder in mapping: return mapping[folder]
    return "profile.png"

asset_dir = "/Users/admin/Documents/profile_bich_ngan/asset/event"
all_dirs = []
for root, dirs, files in os.walk(asset_dir):
    for d in dirs:
        if root == asset_dir:
            all_dirs.append(os.path.join(root, d))

def find_folder(folder_name):
    mapping = {
        "Menarini - kỷ niệm 15 năm thành lập - Color Event - Viettravel": "Menarini - kỷ niệm thành lập - ảnh và clip",
        "Panasonic": "PANASONIC ảnh - clip",
        "Hội Nghị Khách Hàng TCL": "TCL",
    }
    search_name = mapping.get(folder_name.strip(), folder_name.strip())
    for d in all_dirs:
        if search_name.lower() == os.path.basename(d).lower() or search_name.lower() in os.path.basename(d).lower():
            return d
    return None

lines = [
    "MENARINI:Menarini - kỷ niệm 15 năm thành lập - Color Event - Viettravel",
    "PANASONIC:Panasonic",
    "TCL:Hội Nghị Khách Hàng TCL"
]

for line in lines:
    parts = line.split(":", 1)
    title = parts[0].strip()
    folder_name = parts[1].strip()
    folder_path = find_folder(folder_name)
    if folder_path:
        folder_basename = os.path.basename(folder_path)
    else:
        folder_basename = folder_name
    model_src = find_feature_model(title, folder_basename)
    print(f"folder_basename = '{folder_basename}', model_src = '{model_src}'")
