import folium
import os
import json
from pathlib import Path

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
    # ---- Names (safe defaults) ----
    name_en = hike.get("name", "Unknown Hike")
    name_ja = hike.get("name_ja", "")
    prefecture = hike.get("prefecture", "")

    # ---- Folder name (English only, stable) ----
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

    # ---- Popup HTML ----
    popup_html = f"""
    <b>{name_en}</b><br>
    {name_ja}<br>
    <small>📍 {prefecture}</small><br><br>
    {image_html}
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
