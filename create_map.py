import folium
import os
import json
from pathlib import Path
from folium import Element

# -----------------------------
# 1. Base map (Carto Voyager)
# -----------------------------
map_center = [36.2048, 138.2529]
m = folium.Map(location=map_center, zoom_start=6, tiles=None)

folium.TileLayer(
    tiles='https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
    attr='&copy; OpenStreetMap & CARTO',
    name='Carto Voyager',
    control=True
).add_to(m)

# -----------------------------
# 1.1 Instruction banner
# -----------------------------
instruction_html = """
<div style="
  position: fixed;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(255,255,255,0.95);
  padding: 8px 14px;
  border-radius: 6px;
  font-size: 14px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.25);
  z-index: 9999;
">
  🗺️ Click on a marker to see hike details & photos
</div>
"""
m.get_root().html.add_child(Element(instruction_html))

# -----------------------------
# 1.2 Instagram profile link
# -----------------------------
instagram_profile_html = """
<a href="https://www.instagram.com/achikochiinjp/"
   target="_blank"
   style="
     position: fixed;
     top: 12px;
     right: 12px;
     background: white;
     padding: 6px 12px;
     border-radius: 20px;
     box-shadow: 0 2px 6px rgba(0,0,0,0.3);
     text-decoration: none;
     font-size: 14px;
     z-index: 9999;
   ">
  📷 Hiking Instagram
</a>
"""
m.get_root().html.add_child(Element(instagram_profile_html))

# -----------------------------
# 2. Paths
# -----------------------------
images_root = "Images"
data_file = "hikes_data.json"
os.makedirs(images_root, exist_ok=True)

# -----------------------------
# 3. Load hikes
# -----------------------------
if not os.path.exists(data_file):
    print("❌ No hikes found. Run manage_hikes.py first.")
    exit()

with open(data_file, "r", encoding="utf-8") as f:
    hikes = json.load(f)

# -----------------------------
# 4. Add markers
# -----------------------------
for hike in hikes:
    # ---- Fields (safe defaults) ----
    name_en = hike.get("name", "Unknown Hike")
    name_ja = hike.get("name_ja", "")
    prefecture = hike.get("prefecture", "")
    instagram = hike.get("instagram", "")

    # ---- Folder name ----
    folder_name = name_en.replace(" ", "_")
    folder_path = os.path.join(images_root, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # ---- Images ----
    images = list(Path(folder_path).glob("*.*"))
    image_html = ""

    for img in images:
        rel_path = os.path.join(folder_path, img.name).replace("\\", "/")
        image_html += f'<img src="{rel_path}" width="200"><br>'

    if not image_html:
        image_html = f"<i>Add images to {folder_path}</i>"

    # ---- Instagram link (per hike) ----
    instagram_html = ""
    if instagram:
        instagram_html = f"""
        <br>
        <a href="{instagram}" target="_blank" style="text-decoration:none;">
        📷 View this hike on Instagram
        </a>
        """

    # ---- Popup HTML ----
    popup_html = f"""
    <b>{name_ja} ({name_en})</b><br>
    <small>📍 {prefecture}</small><br><br>
    {image_html}
    {instagram_html}
    """

    folium.Marker(
        location=hike["coords"],
        popup=popup_html
    ).add_to(m)

# -----------------------------
# 5. Save map
# -----------------------------
m.save("index.html")
print("✅ Map saved as index.html!")
