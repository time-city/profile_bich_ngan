import os
import glob
import re
import unicodedata

event_dir = '/Users/admin/Documents/profile_bich_ngan/asset/event'
projects_dir = '/Users/admin/Documents/profile_bich_ngan/src/components/projects'
index_file = '/Users/admin/Documents/profile_bich_ngan/index.html'

event_info_map = {
    "5_years_ani_ESCO_BEACH": {
        "title": "KỶ NIỆM 5 NĂM ESCO BEACH",
        "client": "ESCO BEACH",
        "venue": "Esco Beach, Đà Nẵng",
        "audience": "300 - 500+ Pax"
    },
    "ACV - ẢNH VÀ CLIP": {
        "title": "ACV - CẢNG HÀNG KHÔNG QUỐC TẾ ĐÀ NẴNG",
        "client": "ACV",
        "venue": "Da Nang International Airport",
        "audience": "500+ Pax"
    },
    "AEON VIET NAM": {
        "title": "KHAI TRƯƠNG AEON MALL HUẾ",
        "client": "AEON VIET NAM",
        "venue": "AEON Mall Huế",
        "audience": "1000+ Pax"
    },
    "BĐS newtown diamon": {
        "title": "BĐS NEWTOWN DIAMOND",
        "client": "Đất Xanh Miền Trung",
        "venue": "Ngũ Hành Sơn, Đà Nẵng",
        "audience": "500 - 1000+ Pax"
    },
    "GALA_farm": {
        "title": "SỰ KIỆN GALA DINNER",
        "client": "GALA FARM",
        "venue": "Tình Tâm Farm",
        "audience": "100 - 300 Pax"
    },
    "Menarini - kỷ niệm thành lập - ảnh và clip": {
        "title": "MENARINI - KỶ NIỆM THÀNH LẬP",
        "client": "Menarini",
        "venue": "Resort 5 Sao",
        "audience": "200 - 500 Pax"
    },
    "PANASONIC ảnh - clip": {
        "title": "HỘI NGHỊ KHÁCH HÀNG PANASONIC",
        "client": "Panasonic",
        "venue": "Trung tâm hội nghị Đà Nẵng",
        "audience": "200 - 300+ Pax"
    },
    "RHB investment": {
        "title": "HỘI NGHỊ ĐẦU TƯ RHB INVESTMENT",
        "client": "RHB Investment",
        "venue": "Phòng Hội nghị Cao cấp",
        "audience": "50 - 200 Pax"
    },
    "TCL": {
        "title": "HỘI NGHỊ KHÁCH HÀNG TCL",
        "client": "TCL",
        "venue": "Vinpearl Resort & Spa",
        "audience": "500 - 800 Pax"
    },
    "TẤN HƯN - Hội nghị khách hàng": {
        "title": "TẤN HƯNG - HỘI NGHỊ KHÁCH HÀNG",
        "client": "Tấn Hưng",
        "venue": "InterContinental Danang",
        "audience": "300 - 500 Pax"
    },
    "golf_MU_athletes": {
        "title": "GIẢI GOLF MU ATHLETES",
        "client": "MU Athletes",
        "venue": "Montgomerie Links Golf Club",
        "audience": "150 - 200 Pax"
    },
    "Danalog": {
        "title": "SỰ KIỆN DANALOG",
        "client": "Danalog",
        "venue": "Updating...",
        "audience": "Updating..."
    },
    "LUMIA": {
        "title": "SỰ KIỆN LUMIA",
        "client": "LUMIA",
        "venue": "Updating...",
        "audience": "Updating..."
    },
    "viettel": {
        "title": "SỰ KIỆN VIETTEL",
        "client": "Viettel",
        "venue": "Updating...",
        "audience": "Updating..."
    },
    "VNPT": {
        "title": "SỰ KIỆN VNPT",
        "client": "VNPT",
        "venue": "Updating...",
        "audience": "Updating..."
    },
    "wedding": {
        "title": "TIỆC CƯỚI CAO CẤP",
        "client": "Wedding",
        "venue": "Updating...",
        "audience": "Updating..."
    },
    "wedding2": {
        "title": "TIỆC CƯỚI NGOÀI TRỜI",
        "client": "Wedding",
        "venue": "Updating...",
        "audience": "Updating..."
    },
    "wedding3": {
        "title": "TIỆC CƯỚI BÃI BIỂN",
        "client": "Wedding",
        "venue": "Updating...",
        "audience": "Updating..."
    },
    "MATRAX": {
        "title": "SỰ KIỆN MATRAX",
        "client": "Matrax",
        "venue": "Updating...",
        "audience": "Updating..."
    },
    "KJ group": {
        "title": "SỰ KIỆN KJ GROUP",
        "client": "KJ Group",
        "venue": "Updating...",
        "audience": "Updating..."
    },
    "abbott": {
        "title": "SỰ KIỆN ABBOTT",
        "client": "Abbott",
        "venue": "Updating...",
        "audience": "Updating..."
    }
}

model_map = {
    "5_years_ani_ESCO_BEACH": "ESCO.webp",
    "ACV - ẢNH VÀ CLIP": "ACV.webp",
    "AEON VIET NAM": "AEON.webp",
    "BĐS newtown diamon": "BDS.webp",
    "GALA_farm": "GALA_farrm.webp",
    "Menarini - kỷ niệm thành lập - ảnh và clip": "Menarini.webp",
    "PANASONIC ảnh - clip": "panasonic.webp",
    "RHB investment": "rhb.webp",
    "TCL": "TCL.webp",
    "TẤN HƯN - Hội nghị khách hàng": "tấn hưng.webp",
    "golf_MU_athletes": "golf.webp",
    "Danalog": "DANAlog.webp",
    "LUMIA": "LUMIA.webp",
    "viettel": "viettel.webp",
    "VNPT": "VNPT.webp",
    "wedding": "wedding.webp",
    "wedding2": "wedding1.webp",
    "wedding3": "wedding2.webp",
    "MATRAX": "matrax.webp",
    "KJ group": "KJgroup.webp",
    "abbott": "abbott.webp"
}

template_7 = """<div class="featured-project-card {reverse_class} cinematic-slide">
  <div class="project-info-bar">
    <div class="info-group"><span class="info-value">{title}</span></div>
    <div class="info-group"><span class="info-value">{client}</span></div>
    <div class="info-group"><span class="info-value">{venue}</span></div>
    <div class="info-group"><span class="info-value">{audience}</span></div>
  </div>

  <div class="gallery-and-model">
    <div class="project-gallery gallery-passepartout">
      <div class="bento-gallery-5">
{images_html}
      </div>
    </div>
    <div class="project-model">
      <img src="./asset/model/feature/{model_image}" alt="MC Bich Ngan">
    </div>
  </div>
</div>"""

def generate_html_images(images, count):
    html = ""
    max_img = min(count, 5) # Limit to max 5 gallery images
    
    if max_img == 5:
        # 5 images Bento Grid exact match to DANALOG
        html += f'        <div class="gallery-item bento-item" style="grid-column: 1; grid-row: 1;"><img src="{images[0]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item bento-item" style="grid-column: 1; grid-row: 2;"><img src="{images[1]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item bento-item" style="grid-column: 2; grid-row: 1;"><img src="{images[2]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item bento-item" style="grid-column: 3; grid-row: 1;"><img src="{images[3]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item bento-item" style="grid-column: 2 / span 2; grid-row: 2;"><img src="{images[4]}" alt="Event" class="gallery-img"></div>\n'
    elif max_img == 4:
        html += f'        <div class="gallery-item bento-item" style="grid-column: 1; grid-row: 1 / span 2;"><img src="{images[0]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item bento-item" style="grid-column: 2; grid-row: 1 / span 2;"><img src="{images[1]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item bento-item" style="grid-column: 3; grid-row: 1;"><img src="{images[2]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item bento-item" style="grid-column: 3; grid-row: 2;"><img src="{images[3]}" alt="Event" class="gallery-img"></div>\n'
    elif max_img == 3:
        html += f'        <div class="gallery-item bento-item" style="grid-column: 1 / span 2; grid-row: 1 / span 2;"><img src="{images[0]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item bento-item" style="grid-column: 3; grid-row: 1;"><img src="{images[1]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item bento-item" style="grid-column: 3; grid-row: 2;"><img src="{images[2]}" alt="Event" class="gallery-img"></div>\n'
    elif max_img == 2:
        html += f'        <div class="gallery-item bento-item" style="grid-column: 1 / span 2; grid-row: 1 / span 2;"><img src="{images[0]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item bento-item" style="grid-column: 3; grid-row: 1 / span 2;"><img src="{images[1]}" alt="Event" class="gallery-img"></div>\n'
    elif max_img == 1:
        html += f'        <div class="gallery-item bento-item" style="grid-column: 1 / span 3; grid-row: 1 / span 2;"><img src="{images[0]}" alt="Event" class="gallery-img"></div>\n'
    return html

os.makedirs(projects_dir, exist_ok=True)
for old_f in glob.glob(os.path.join(projects_dir, "project-*.html")):
    os.remove(old_f)

folders = sorted([f for f in os.listdir(event_dir) if os.path.isdir(os.path.join(event_dir, f))])

if "KJ group" in folders:
    folders.remove("KJ group")
    folders.insert(0, "KJ group")

generated_files = []

for i, folder in enumerate(folders):
    filename = f"project-{i+1:02d}.html"

    folder_path = os.path.join(event_dir, folder)
    images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.webp', '.webp', '.webp', '.webp', '.gif'))]
    images.sort()
    
    image_paths = [unicodedata.normalize("NFC", f"./asset/event/{folder}/{img}") for img in images]
    
    count = len(image_paths)
    if count == 0:
        continue
        
    images_html = generate_html_images(image_paths, count).rstrip()
    
    info = event_info_map.get(folder, {})
    title = info.get("title", folder.upper())
    client = info.get("client", folder.split('-')[0].strip())
    venue = info.get("venue", "Updating...")
    audience = info.get("audience", "Updating...")
    
    model_img = model_map.get(folder, "image-Photoroom (3).webp")
    reverse_class = "reverse" if i % 2 == 1 else ""
    
    html_content = unicodedata.normalize("NFC", template_7.format(
        title=title, client=client, venue=venue, audience=audience, 
        images_html=images_html, model_image=model_img, reverse_class=reverse_class
    ))
    
    out_file = os.path.join(projects_dir, filename)
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    generated_files.append(filename)

print(f"Created {len(generated_files)} project HTML files.")

with open(index_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace projectFiles array
project_files_str = ",\n        ".join([f"'{f}'" for f in generated_files])
new_array_str = f"const projectFiles = [\n        {project_files_str}\n      ];"

content = re.sub(r"const projectFiles = \[[\s\S]*?\];", new_array_str, content)

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html")
