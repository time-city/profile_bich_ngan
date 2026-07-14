import os
import glob
import re

user_list = """
MENARINI:Menarini - kỷ niệm 15 năm thành lập - Color Event - Viettravel
PANASONIC:Panasonic
TCL:Hội Nghị Khách Hàng TCL
AEON VIET NAM: AEON VIET NAM
Hội nghị khách hàng lốp Matrax: MATRAX
TẤN HƯNG - Hội nghị khách hàng: TẤN HƯN - Hội nghị khách hàng
ACV : ACV - Cảng Hàng Không Quốc Tế Đà Nẵng
Lễ ra mắt công ty TNHH SMART Logistic Đà Nẵng - Cảng Đà Nẵng - Đà Nẵng Port: DA NANG PORT
Hội Phẫu Thuật Thần Kinh Việt Nam: Hội Nghị Phẫu Thuật Thần Kinh Quốc tế lần thứ 9
Sự kiện ra mắt ip 17 :Mở bán 17 
Cuộc thi nữ hoàng trang sức: Nữ Hoàng Trang Sức
BĐS Newtown Diamond: Bất Động Sản - mở bán New Town Diamond
Mở bán BĐS Huế Heritage: Mở bán BĐS - Huế Heritage
Khánh thành Chợ Lăng Cô: Chợ Lăng cô
Dẫn cho đoàn khách Quốc tế MALAYSIA : Show đoàn khách Malaysia 
Farmtrip Indonesia agency: GALA_farm
RHS Investment: RHB investment
Good food: Good food 
Hội nghị khách hàng Monin Viet Nam: monin
Philip: Sự kiện ra mắt sản phẩm mới của Philips
YEAR END PARTY Fashion Garment Viet Nam: Song ngữ Anh Việt - FLG Viet Nam
Hội Nghị Phẫu Thuật Thần Kinh Việt Nam 2: Hội Nghị Phẫu Thuật Thần Kinh Quốc tế lần thứ 9
5 Year Anniversary Esco Beach Đà Nẵng: 5 Years anniversary of ESCO BEACH ĐÀ NẴNG
SHB ĐÀ NẴNG: SHB
LG Electronic: Yep của Lg electonic Viet Nam
Giải Golf cùng tuyển CLB MU: golf_MU_athletes
Giải Golf Họ Phan: giải golf họ Phan toàn quốc
Giải golf các CLB: golf clb
Giải Golf DSEZA: Dseza
Viettel:viettel
KJ group: KJ group
Danalog : Danalog
Sabeco: Sabeco
Aboot 1 : abbott
Aboot 2: abbott
Gala Sai Gon Tourist: gala saigon tour
"""

lines = [line.strip() for line in user_list.strip().split('\n') if line.strip()]

asset_dir = "/Users/admin/Documents/profile_bich_ngan/asset"
components_dir = "/Users/admin/Documents/profile_bich_ngan/src/components/projects"

if not os.path.exists(components_dir):
    os.makedirs(components_dir)

# Clean existing projects
for f in glob.glob(os.path.join(components_dir, "project-*.html")):
    os.remove(f)

# Load all directories
all_dirs = []
for root, dirs, files in os.walk(asset_dir):
    for d in dirs:
        all_dirs.append(os.path.join(root, d))

def find_folder(folder_name):
    for d in all_dirs:
        if folder_name.lower() in os.path.basename(d).lower():
            return d
    return None

def get_best_image(folder_path, used_images):
    images = glob.glob(os.path.join(folder_path, '*.[jJ][pP]*[gG]')) + \
             glob.glob(os.path.join(folder_path, '*.[pP][nN][gG]')) + \
             glob.glob(os.path.join(folder_path, '*.[wW][eE][bB][pP]'))
    
    available = [img for img in images if img not in used_images]
    if not available and images:
        return images[0] # fallback if all used
    if available:
        # Sort to get a consistent one, maybe pick a landscape looking name if possible, or just the first
        available.sort()
        used_images.append(available[0])
        return available[0]
    return ""

html_template = """<div class="featured-project-card animate-on-scroll">
  <div class="project-image">
    <img src="{img_src}" alt="{title}">
    <div class="project-overlay">
      <span class="view-project-btn">Xem chi tiết</span>
    </div>
  </div>
  <div class="project-info">
    <h4 class="project-title">{title}</h4>
    <p class="project-category">Sự Kiện Nổi Bật</p>
  </div>
</div>
"""

generated_files = []
used_images = []

for idx, line in enumerate(lines):
    if ':' not in line: continue
    title, folder = line.split(':', 1)
    title = title.strip()
    folder = folder.strip()
    
    # 22 is duplicate of 9, named slightly different to avoid dict key collision
    if title == "Hội Nghị Phẫu Thuật Thần Kinh Việt Nam 2":
        title = "Hội Nghị Phẫu Thuật Thần Kinh Việt Nam"
        
    matched_dir = find_folder(folder)
    img_src = ""
    if matched_dir:
        img_path = get_best_image(matched_dir, used_images)
        if img_path:
            # Convert absolute path to relative path for web
            rel_path = "./" + os.path.relpath(img_path, "/Users/admin/Documents/profile_bich_ngan")
            img_src = rel_path
            
    if not img_src:
        img_src = "./asset/event/placeholder.jpg"
        
    file_name = f"project-{idx+1:02d}.html"
    file_path = os.path.join(components_dir, file_name)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_template.format(img_src=img_src, title=title))
        
    generated_files.append(file_name)
    print(f"Generated {file_name} for {title}")

# Now update index.html to load these 36 projects
index_path = "/Users/admin/Documents/profile_bich_ngan/index.html"
with open(index_path, "r", encoding="utf-8") as f:
    index_content = f.read()

# Replace the projectFiles array in index.html
project_files_str = ",\n        ".join([f"'{name}'" for name in generated_files])
new_array = f"const projectFiles = [\n        {project_files_str}\n      ];"

# Find the array block and replace it
import re
pattern = re.compile(r"const projectFiles = \[.*?\];", re.DOTALL)
index_content = pattern.sub(new_array, index_content)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(index_content)

print("Updated index.html successfully!")
