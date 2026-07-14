import os
import glob

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

feature_dir = "/Users/admin/Documents/profile_bich_ngan/asset/model/feature"
feature_files = [f.lower() for f in os.listdir(feature_dir) if os.path.isfile(os.path.join(feature_dir, f))]
feature_files_orig = os.listdir(feature_dir)

def find_feature_model(title, folder):
    # Try multiple heuristic matches
    # e.g., if title contains 'ACV', look for 'acv' in filename
    words = title.lower().split() + folder.lower().split()
    for f_idx, f in enumerate(feature_files):
        # some exact substring match
        f_no_ext = os.path.splitext(f)[0]
        if f_no_ext in title.lower() or f_no_ext in folder.lower():
            return feature_files_orig[f_idx]
        if title.lower() in f_no_ext or folder.lower() in f_no_ext:
            return feature_files_orig[f_idx]
            
    # Try matching first word
    if words:
        first_word = words[0]
        if len(first_word) > 2:
            for f_idx, f in enumerate(feature_files):
                if first_word in f:
                    return feature_files_orig[f_idx]
                    
    return None

missing = []
print("--- FEATURE MODEL MATCHING ---")
for line in lines:
    if ':' not in line: continue
    title, folder = line.split(':', 1)
    title = title.strip()
    folder = folder.strip()
    
    if title == "Hội Nghị Phẫu Thuật Thần Kinh Việt Nam 2":
        title = "Hội Nghị Phẫu Thuật Thần Kinh Việt Nam"
        
    m = find_feature_model(title, folder)
    if m:
        print(f"[OK] {title} -> {m}")
    else:
        print(f"[MISSING] {title}")
        missing.append(title)
        
print(f"\nTotal missing feature models: {len(missing)}")
