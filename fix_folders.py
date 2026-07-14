import os
import glob
import shutil

user_list = """
MENARINI:Menarini - kỷ niệm 15 năm thành lập - Color Event - Viettravel
PANASONIC:Panasonic
TCL:Hội Nghị Khách Hàng TCL
AEON VIET NAM: AEON
Hội nghị khách hàng lốp Matrax: MATRAX
TẤN HƯNG - Hội nghị khách hàng: Tấn Hưng
ACV : ACV - Cảng Hàng Không Quốc Tế Đà Nẵng
Lễ ra mắt công ty TNHH SMART Logistic Đà Nẵng - Cảng Đà Nẵng - Đà Nẵng Port: DA NANG PORT
Hội Phẫu Thuật Thần Kinh Việt Nam: Hội Nghị Phẫu Thuật Thần Kinh Quốc tế lần thứ 9
Sự kiện ra mắt ip 17 :Mở bán 17 
Cuộc thi nữ hoàng trang sức: Nữ Hoàng Trang Sức
BĐS Newtown Diamond: Bất Động Sản - mở bán New Town Diamond
Mở bán BĐS Huế Heritage: Mở bán BĐS - Huế Heritage
Khánh thành Chợ Lăng Cô: Chợ Lăng cô
Dẫn cho đoàn khách Quốc tế MALAYSIA : Show đoàn khách Malaysia 
Farmtrip Indonesia agency: GALA ĐOÀN FARM TRIP INDONESIA
RHS Investment: RHS INVESTMENT
Good food: Good food 
Hội nghị khách hàng Monin Viet Nam: monin
Philip: Sự kiện ra mắt sản phẩm mới của Philips
YEAR END PARTY Fashion Garment Viet Nam: Song ngữ Anh Việt - FLG Viet Nam
Hội Nghị Phẫu Thuật Thần Kinh Việt Nam: Hội Nghị Phẫu Thuật Thần Kinh Quốc tế lần thứ 9
5 Year Anniversary Esco Beach Đà Nẵng: 5 Years anniversary of ESCO BEACH ĐÀ NẴNG
SHB ĐÀ NẴNG: SHB
LG Electronic: Yep của Lg electonic Viet Nam
Giải Golf cùng tuyển CLB MU: Giải golf cùng các cực DANH THỦ đội tuyển MU
Giải Golf Họ Phan: giải golf họ Phan toàn quốc
Giải golf các CLB: golf clb
Giải Golf DSEZA: Dseza
Viettel:Viettel
KJ group: KJ GROUP
Danalog : Yep Danalog
Sabeco: Sabeco
Aboot 1 : ABOOT
Aboot 2: abbott
Gala Sai Gon Tourist: gala saigon tour
20 năm thành lập TẬP ĐOÀN Á ÂU: gala saigon tour
"""

lines = [line.strip() for line in user_list.strip().split('\n') if line.strip()]
asset_dir = "/Users/admin/Documents/profile_bich_ngan/asset"
event_dir = os.path.join(asset_dir, "event")

# 1. Delete all empty folders in asset/event
for root, dirs, files in os.walk(event_dir, topdown=False):
    for name in dirs:
        folder_path = os.path.join(root, name)
        if not os.listdir(folder_path):
            os.rmdir(folder_path)
            print(f"Deleted empty folder: {folder_path}")

# Load all directories
all_dirs = []
for root, dirs, files in os.walk(asset_dir):
    for d in dirs:
        all_dirs.append(os.path.join(root, d))

# 2. Check which events are TRULY missing photos anywhere
missing_folders = []

# Mappings for slightly differently named folders the user already has photos in:
# (From previous analysis)
mapping = {
    "Tấn Hưng": "TẤN HƯN - Hội nghị khách hàng",
    "RHS INVESTMENT": "RHB investment",
    "Giải golf cùng các cực DANH THỦ đội tuyển MU": "golf_MU_athletes",
    "GALA ĐOÀN FARM TRIP INDONESIA": "GALA_farm",
    "Yep Danalog": "Danalog",
    "ABOOT": "abbott",
    "Menarini - kỷ niệm 15 năm thành lập - Color Event - Viettravel": "Menarini - kỷ niệm 15 năm thành lập - Color Event - Viettravel",
    # good food is actually "Good food " in "Show tiếng anh"
}

for line in lines:
    if ':' not in line: continue
    title, folder = line.split(':', 1)
    folder = folder.strip()
    
    search_folder = mapping.get(folder, folder)
    
    # Try to find if this folder exists anywhere with photos
    found_images = False
    for d in all_dirs:
        if search_folder.lower() in os.path.basename(d).lower() or folder.lower() in os.path.basename(d).lower():
            # check images
            images = glob.glob(os.path.join(d, '*.[jJ][pP]*[gG]')) + glob.glob(os.path.join(d, '*.[pP][nN][gG]')) + glob.glob(os.path.join(d, '*.[wW][eE][bB][pP]'))
            if len(images) > 0:
                found_images = True
                break
                
    if not found_images:
        missing_folders.append(folder)

print("\n--- TRULY MISSING FOLDERS ---")
for f in missing_folders:
    print(f)
    # 3. Create only the TRULY missing folders in asset/event
    new_path = os.path.join(event_dir, f)
    if not os.path.exists(new_path):
        os.makedirs(new_path)
        print(f"-> Created {new_path}")
