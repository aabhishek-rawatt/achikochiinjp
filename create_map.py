import folium
import os
import json
from pathlib import Path

# -----------------------------
# 1. Base map (reliable terrain)
# -----------------------------
map_center = [36.2048, 138.2529]  # center of Japan

m = folium.Map(
    location=map_center,
    zoom_start=6,
    tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
)

# -----------------------------
# 2. Paths
# -----------------------------
images_root = "Images"
data_file = "hikes_data.json"

if not os.path.exists(images_root):
    os.mkdir(images_root)

# -----------------------------
# 3. Load hikes
# -----------------------------
if not os.path.exists(data_file):
    print("❌ No hikes found. Run manage_hikes.py to add hikes first.")
    exit()

with open(data_file, "r", encoding="utf-8") as f:
    hikes = json.load(f)

# -----------------------------
# 4. Add markers with images (if any)
# -----------------------------
for hike in hikes:
    # Ensure folder exists
    folder_name = hike["name"].replace(" ", "_")
    folder_path = os.path.join(images_root, folder_name)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        print(f"📂 Created folder: {folder_path}")

    # Find images in folder
    images = list(Path(folder_path).glob("*.*"))  # all files
    image_html = ""
    for img in images:
        rel_path = os.path.join(folder_path, img.name).replace("\\", "/")
        image_html += f'<img src="{rel_path}" width="200"><br>'

    if not image_html:
        image_html = f"<i>Add images to {folder_path}</i>"

    popup_html = f"<b>{hike['name']}</b><br>{image_html}"

    folium.Marker(location=hike["coords"], popup=popup_html).add_to(m)

# -----------------------------
# 5. Save map
# -----------------------------
m.save("index.html")
print("✅ Map saved as index.html! Add images to each folder to display them in popups.")
