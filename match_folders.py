import os
import glob
import re

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

all_dirs = []
with open('all_folders.txt', 'r') as f:
    all_dirs = [line.strip() for line in f.read().splitlines()]

print("MATCHING RESULTS:")
for idx, line in enumerate(lines):
    if ':' not in line: continue
    title, folder = line.split(':', 1)
    title = title.strip()
    folder = folder.strip()
    
    # Try to find folder
    matched_dir = None
    for d in all_dirs:
        # Simple case insensitive match
        if folder.lower() in d.lower():
            matched_dir = d
            break
            
    if matched_dir:
        # Find images inside
        images = glob.glob(os.path.join(matched_dir, '*.[jJ][pP]*[gG]')) + glob.glob(os.path.join(matched_dir, '*.[pP][nN][gG]')) + glob.glob(os.path.join(matched_dir, '*.[wW][eE][bB][pP]'))
        if images:
            print(f"[OK] {idx+1}. {title} -> {matched_dir} (Found {len(images)} images)")
        else:
            print(f"[WARNING] {idx+1}. {title} -> {matched_dir} (NO IMAGES FOUND)")
    else:
        print(f"[MISSING] {idx+1}. {title} -> Cannot find folder matching '{folder}'")

