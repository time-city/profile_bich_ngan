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
        "venue": "Updating...",
        "audience": "Updating..."
    },
    "TẤN HƯN - Hội nghị khách hàng": {
        "title": "TẤN HƯNG - HỘI NGHỊ KHÁCH HÀNG",
        "client": "Tấn Hưng",
        "venue": "Updating...",
        "audience": "Updating..."
    },
    "golf_MU_athletes": {
        "title": "GIẢI GOLF MU ATHLETES",
        "client": "MU Athletes",
        "venue": "Updating...",
        "audience": "Updating..."
    }
}

template_7 = """<div class="featured-project-card">
  <div class="decor-text decor-top-left">✦ English Hosting</div>
  <div class="decor-text decor-top-right">VIP Reception ✦</div>
  <div class="decor-text decor-bottom-left">✦ Interactive Session</div>
  <div class="decor-text decor-bottom-right">Award Ceremony ✦</div>

  <div class="project-info">
    <h4 class="project-title">{title}</h4>
    <div class="project-details">
      <div class="detail-item">
        <span class="detail-label">Role | Vai trò</span>
        <span class="detail-value">Master of Ceremonies</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Client | Khách hàng</span>
        <span class="detail-value">{client}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Venue | Địa điểm</span>
        <span class="detail-value">{venue}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Audience | Quy mô</span>
        <span class="detail-value">{audience}</span>
      </div>
    </div>
  </div>

  <div class="gallery-and-model">
    <div class="project-gallery gallery-passepartout">
      <div class="project-gallery-grid">
{images_html}
      </div>
    </div>
    <div class="project-model">
      <img src="./asset/model/image-Photoroom (3).png" alt="MC Bich Ngan">
    </div>
  </div>
</div>"""

def generate_html_images(images, count):
    html = ""
    if count >= 7:
        html += f'        <div class="gallery-item"><img src="{images[0]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item"><img src="{images[1]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item"><img src="{images[2]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item"><img src="{images[3]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item"><img src="{images[4]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item"><img src="{images[5]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item"><img src="{images[6]}" alt="Event" class="gallery-img"></div>\n'
    elif count == 6:
        html += f'        <div class="gallery-item" style="grid-column: span 3; aspect-ratio: 4/3;"><img src="{images[0]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item" style="grid-column: span 3; aspect-ratio: 4/3;"><img src="{images[1]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item" style="grid-column: span 2; aspect-ratio: 1;"><img src="{images[2]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item" style="grid-column: span 2; aspect-ratio: 1;"><img src="{images[3]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item" style="grid-column: span 2; aspect-ratio: 1;"><img src="{images[4]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item" style="grid-column: span 6; aspect-ratio: 21/9;"><img src="{images[5]}" alt="Event" class="gallery-img"></div>\n'
    elif count >= 3:
        html += f'        <div class="gallery-item" style="grid-column: span 6; aspect-ratio: 21/9;"><img src="{images[0]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item" style="grid-column: span 3; aspect-ratio: 4/3;"><img src="{images[1]}" alt="Event" class="gallery-img"></div>\n'
        html += f'        <div class="gallery-item" style="grid-column: span 3; aspect-ratio: 4/3;"><img src="{images[2]}" alt="Event" class="gallery-img"></div>\n'
    else:
        for img in images:
            html += f'        <div class="gallery-item" style="grid-column: span 6;"><img src="{img}" alt="Event" class="gallery-img"></div>\n'
    return html

os.makedirs(projects_dir, exist_ok=True)
for old_f in glob.glob(os.path.join(projects_dir, "project-*.html")):
    os.remove(old_f)

folders = sorted([f for f in os.listdir(event_dir) if os.path.isdir(os.path.join(event_dir, f))])

generated_files = []

for i, folder in enumerate(folders):
    folder_path = os.path.join(event_dir, folder)
    images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))]
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
    
    html_content = template_7.format(title=title, client=client, venue=venue, audience=audience, images_html=images_html)
    
    filename = f"project-{i+1:02d}.html"
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
