import os

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
all_models = os.listdir(feature_dir)
all_models = [m for m in all_models if not m.startswith('.')]

mapping = {
    "DA NANG PORT": "DANANGPORT.webp",
    "Bất Động Sản - mở bán New Town Diamond": "BDS.webp",
    "Mở bán BĐS - Huế Heritage": "BDS_huế.webp",
    "Chợ Lăng cô": "lang_co.webp",
    "GALA_farm": "GALA_farrm.webp",
    "KJ group": "KJgroup.webp",
    "5 Years anniversary of ESCO BEACH ĐÀ NẴNG": "esco_beach_danang.webp",
    "gala saigon tour": "gala_saigon_tour.webp",
    "Yep của Lg electonic Viet Nam": "NONE", # Checking if this has a real model
    "Hội Nghị Phẫu Thuật Thần Kinh Quốc tế lần thứ 9": "thần kinh.webp",
    "Mở bán 17": "mở bán 17.webp",
    "Nữ Hoàng Trang Sức": "nữ hoàng trang sức.webp",
    "Show đoàn khách Malaysia": "malaysia.webp",
    "RHB investment": "RHS.webp",
    "Good food ": "goodfood.webp",
    "monin": "monin.webp",
    "Sự kiện ra mắt sản phẩm mới của Philips": "sự kiện ra mắt sản phẩm philips.webp",
    "Song ngữ Anh Việt - FLG Viet Nam": "song ngữ anh việt.webp",
    "SHB": "SHB.webp",
    "golf_MU_athletes": "golf.webp",
    "giải golf họ Phan toàn quốc": "golf họ phan toàn quốc.webp",
    "golf clb": "golf clb.webp",
    "Dseza": "Desza.webp",
    "viettel": "viettel.webp",
    "Danalog": "DANAlog.webp",
    "Sabeco": "sabeco.webp",
    "abbott": "abbott.webp",
    "Menarini - kỷ niệm 15 năm thành lập - Color Event - Viettravel": "Menarini.webp",
    "Panasonic": "panasonic.webp",
    "Hội Nghị Khách Hàng TCL": "TCL.webp",
    "AEON VIET NAM": "AEON.webp",
    "MATRAX": "matrax.webp",
    "TẤN HƯN - Hội nghị khách hàng": "tấn hưng.webp",
    "ACV - Cảng Hàng Không Quốc Tế Đà Nẵng": "ACV.webp"
}

used_models = []
missing_events = []

for line in lines:
    title, folder = line.split(':', 1)
    title = title.strip()
    folder = folder.strip()
    
    m = mapping.get(folder, "NONE")
    if m != "NONE" and m in all_models:
        used_models.append(m)
    else:
        missing_events.append(f"{title} (Folder: {folder})")

used_models = set(used_models)
unused_models = [m for m in all_models if m not in used_models]

print("--- EVENTS WITHOUT A SPECIFIC MODEL ---")
for e in missing_events:
    print(e)
    
print("\n--- EXTRA MODELS IN ASSET/MODEL/FEATURE ---")
for u in unused_models:
    print(u)
