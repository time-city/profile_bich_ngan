import os

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
Hội Nghị Phẫu Thuật Thần Kinh Việt Nam 2: Hội Nghị Phẫu Thuật Thần Kinh Quốc tế lần thứ 9
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
"""
lines = [line.strip() for line in user_list.strip().split('\n') if line.strip()]
asset_dir = "/Users/admin/Documents/profile_bich_ngan/asset"

# Mappings for slightly differently named folders the user already has photos in:
mapping = {
    "Tấn Hưng": "TẤN HƯN - Hội nghị khách hàng",
    "RHS INVESTMENT": "RHB investment",
    "Giải golf cùng các cực DANH THỦ đội tuyển MU": "golf_MU_athletes",
    "GALA ĐOÀN FARM TRIP INDONESIA": "GALA_farm",
    "Yep Danalog": "Danalog",
    "ABOOT": "abbott",
    "Menarini - kỷ niệm 15 năm thành lập - Color Event - Viettravel": "Menarini - kỷ niệm 15 năm thành lập - Color Event - Viettravel",
    "Good food": "Good food ",
    "AEON": "AEON VIET NAM",
    "Hội Nghị Phẫu Thuật Thần Kinh Quốc tế lần thứ 9": "Hội Nghị Phẫu Thuật Thần Kinh Quốc tế lần thứ 9"
}

# The folders the user actually requested (resolved to actual folder names)
requested_folders = set()
for line in lines:
    if ':' not in line: continue
    title, folder = line.split(':', 1)
    folder = folder.strip()
    actual_folder = mapping.get(folder, folder)
    requested_folders.add(actual_folder.lower())

# Get all folders in event, Show tieng anh, Show dan tieng viet
target_dirs = [
    os.path.join(asset_dir, "event"),
    os.path.join(asset_dir, "Show tiếng anh"),
    os.path.join(asset_dir, "Show dẫn tiếng việt")
]

all_actual_folders = []
for td in target_dirs:
    if os.path.exists(td):
        for item in os.listdir(td):
            full_path = os.path.join(td, item)
            if os.path.isdir(full_path):
                # Only consider directories
                all_actual_folders.append(item)

extra_events = []
for folder in all_actual_folders:
    if folder.lower() not in requested_folders:
        extra_events.append(folder)

print("--- EXTRA EVENT FOLDERS ---")
for e in extra_events:
    print(e)

