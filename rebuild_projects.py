import os
import glob
import re
from PIL import Image

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
RHS Investment: rhs
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
Aboot 1: abbott
Gala Sai Gon Tourist: gala saigon tour
"""

lines = [line.strip() for line in user_list.strip().split('\n') if line.strip()]

asset_dir = "/Users/admin/Documents/profile_bich_ngan/asset/event"
components_dir = "/Users/admin/Documents/profile_bich_ngan/src/components/projects"

# Clean existing projects
for f in glob.glob(os.path.join(components_dir, "project-*.html")):
    os.remove(f)

# Load all directories inside asset/event ONLY
all_dirs = []
for root, dirs, files in os.walk(asset_dir):
    for d in dirs:
        all_dirs.append(os.path.join(root, d))

def find_folder(folder_name):
    # Try exact mapping first
    mapping = {
        "Menarini - kỷ niệm 15 năm thành lập - Color Event - Viettravel": "Menarini - kỷ niệm thành lập - ảnh và clip",
        "Panasonic": "PANASONIC ảnh - clip",
        "Hội Nghị Khách Hàng TCL": "TCL",
        "Bất Động Sản - mở bán New Town Diamond": "BĐS newtown diamon",
        "ACV - Cảng Hàng Không Quốc Tế Đà Nẵng": "ACV - ẢNH VÀ CLIP",
        "Song ngữ Anh Việt - FLG Viet Nam": "song ngữ anh việt",
        "Good food": "goodfood",
        "RHS INVESTMENT": "rhs",
        "Tấn Hưng": "TẤN HƯN - Hội nghị khách hàng",
        "Giải golf cùng các cực DANH THỦ đội tuyển MU": "golf_MU_athletes",
        "GALA ĐOÀN FARM TRIP INDONESIA": "GALA_farm",
        "Yep Danalog": "Danalog",
        "ABOOT": "abbott",
        "AEON": "AEON VIET NAM"
    }
    search_name = mapping.get(folder_name.strip(), folder_name.strip())
    
    for d in all_dirs:
        if search_name.lower() == os.path.basename(d).lower() or search_name.lower() in os.path.basename(d).lower():
            return d
    return None

def get_images(folder_path, count=5):
    images = glob.glob(os.path.join(folder_path, '*.[jJ][pP]*[gG]')) + \
             glob.glob(os.path.join(folder_path, '*.[pP][nN][gG]')) + \
             glob.glob(os.path.join(folder_path, '*.[wW][eE][bB][pP]'))
    images.sort()
    
    # If we have less than count, duplicate some to fill the grid (bento needs 5 slots)
    res = []
    if not images:
        res = ["./asset/event/placeholder.jpg"] * count
    else:
        for i in range(count):
            res.append(images[i % len(images)])
            
    def get_aspect(img_path):
        if "placeholder" in img_path: return 1.0
        try:
            with Image.open(img_path) as im:
                w, h = im.size
                return w / h
        except:
            return 1.0
            
    # Sort so the widest image is at the end (index 4) for the wide bento slot
    res = sorted(res, key=get_aspect)
    
    return ["./" + os.path.relpath(img, "/Users/admin/Documents/profile_bich_ngan") if not img.startswith("./") else img for img in res]

feature_dir = "/Users/admin/Documents/profile_bich_ngan/asset/model/feature"
feature_files = os.listdir(feature_dir)
feature_files_lower = [f.lower() for f in feature_files if os.path.isfile(os.path.join(feature_dir, f))]

def find_feature_model(title, folder):
    # Hardcoded mapping to fix the misses
    mapping = {
        "DA NANG PORT": "DANANGPORT.png",
        "Bất Động Sản - mở bán New Town Diamond": "bds_diamond.png",
        "Mở bán BĐS - Huế Heritage": "BDS_huế.png",
        "Chợ Lăng cô": "lang_co.png",
        "GALA_farm": "GALA_farrm.webp",
        "KJ group": "KJgroup.webp",
        "5 Years anniversary of ESCO BEACH ĐÀ NẴNG": "esco_beach_danang.png",
        "gala saigon tour": "gala_saigon_tour.png",
        "Yep của Lg electonic Viet Nam": "lg_electronic.png",
        "Hội Nghị Phẫu Thuật Thần Kinh Quốc tế lần thứ 9": "thần kinh.png",
        "Mở bán 17": "mở bán 17.png",
        "Nữ Hoàng Trang Sức": "nữ hoàng trang sức.png",
        "Show đoàn khách Malaysia": "malaysia.png",
        "rhs": "RHS.png",
        "Good food": "goodfood.png",
        "monin": "monin.png",
        "Sự kiện ra mắt sản phẩm mới của Philips": "sự kiện ra mắt sản phẩm philips.png",
        "Song ngữ Anh Việt - FLG Viet Nam": "song ngữ anh việt.png",
        "SHB": "SHB.png",
        "golf_MU_athletes": "golf.webp",
        "giải golf họ Phan toàn quốc": "golf họ phan toàn quốc.png",
        "golf clb": "golf clb.png",
        "Dseza": "Desza.png",
        "viettel": "viettel.webp",
        "Danalog": "DANAlog.webp",
        "Sabeco": "sabeco.png",
        "abbott": "abbott.webp",
        "Menarini - kỷ niệm 15 năm thành lập - Color Event - Viettravel": "Menarini.webp",
        "Panasonic": "panasonic.png",
        "Hội Nghị Khách Hàng TCL": "TCL.webp",
        "AEON VIET NAM": "AEON.webp",
        "MATRAX": "matrax.webp",
        "TẤN HƯN - Hội nghị khách hàng": "tấn hưng.webp",
        "ACV - Cảng Hàng Không Quốc Tế Đà Nẵng": "ACV.webp"
    }
    if folder in mapping:
        return mapping[folder]
    return "profile.png" # Safe fallback

html_template = """<div class="featured-project-card cinematic-slide {reverse_class}">
  <div class="project-info-bar">
    <div class="info-group"><span class="info-value">{title}</span></div>
    <div class="info-group"><span class="info-value">Song Ngữ / Tiếng Việt</span></div>
    <div class="info-group"><span class="info-value">Hoành Tráng</span></div>
  </div>

  <div class="gallery-and-model">
    <div class="project-gallery gallery-passepartout">
      <div class="bento-gallery-5">
        <div class="gallery-item bento-item" style="grid-column: 1; grid-row: 1;"><img src="{img0}" alt="{title}" class="gallery-img"></div>
        <div class="gallery-item bento-item" style="grid-column: 1; grid-row: 2;"><img src="{img1}" alt="{title}" class="gallery-img"></div>
        <div class="gallery-item bento-item" style="grid-column: 2; grid-row: 1;"><img src="{img2}" alt="{title}" class="gallery-img"></div>
        <div class="gallery-item bento-item" style="grid-column: 3; grid-row: 1;"><img src="{img3}" alt="{title}" class="gallery-img"></div>
        <div class="gallery-item bento-item" style="grid-column: 2 / span 2; grid-row: 2;"><img src="{img4}" alt="{title}" class="gallery-img"></div>
      </div>
    </div>
    <div class="project-model">
      <img src="./asset/model/feature/{model_src}" alt="MC Bich Ngan">
    </div>
  </div>
</div>
"""

for idx, line in enumerate(lines):
    if ':' not in line: continue
    title, folder = line.split(':', 1)
    title = title.strip()
    folder = folder.strip()
    
    if title == "Hội Nghị Phẫu Thuật Thần Kinh Việt Nam 2":
        title = "Hội Nghị Phẫu Thuật Thần Kinh Việt Nam"
        
    matched_dir = find_folder(folder)
    images = get_images(matched_dir, 5) if matched_dir else ["./asset/event/placeholder.jpg"] * 5
    
    model_src = find_feature_model(title, folder)
    
    # Alternate left/right model
    reverse_class = "reverse" if idx % 2 != 0 else ""
    
    file_name = f"project-{idx+1:02d}.html"
    file_path = os.path.join(components_dir, file_name)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_template.format(
            title=title, 
            reverse_class=reverse_class,
            img0=images[0], img1=images[1], img2=images[2], img3=images[3], img4=images[4],
            model_src=model_src
        ))
        
    print(f"Re-generated {file_name} with Bento Gallery + Feature Model")

# Update index.html
generated_files = [f"project-{i+1:02d}.html" for i in range(len(lines))]
index_path = "/Users/admin/Documents/profile_bich_ngan/index.html"
with open(index_path, "r", encoding="utf-8") as f:
    index_content = f.read()

project_files_str = ",\n        ".join([f"'{name}'" for name in generated_files])
new_array = f"const projectFiles = [\n        {project_files_str}\n      ];"

pattern = re.compile(r"const projectFiles = \[.*?\];", re.DOTALL)
index_content = pattern.sub(new_array, index_content)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(index_content)
    
print("Updated index.html successfully!")
