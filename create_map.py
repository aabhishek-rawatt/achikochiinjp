import folium
import os

# -----------------------------
# 1. Create the base map
# -----------------------------
# Center of Japan
map_center = [34.7, 135.5]  # Centralized for your hikes
m = folium.Map(
    location=map_center,
    zoom_start=8,
    tiles='Stamen Terrain',
    attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'
)

# -----------------------------
# 2. List of hikes
# -----------------------------
hikes = [
    {"name": "Mount Rokko", "coords": [34.77778, 135.26389], "images": []},
    {"name": "Uma Nose", "coords": [34.97250, 135.41417], "images": []},
    {"name": "Fukuchiyama", "coords": [35.300, 135.133], "images": []},
    {"name": "Mount Kongou", "coords": [34.41944, 135.67306], "images": []},
    {"name": "Takatori", "coords": [34.44944, 135.79333], "images": []},
    {"name": "Katano-Kumini", "coords": [34.78794, 135.67995], "images": []},
    {"name": "Mount Maya", "coords": [34.73292, 135.20444], "images": []},
    {"name": "Mount Iwawaki", "coords": [34.37387, 135.55110], "images": []},
    {"name": "Mount Hiei", "coords": [35.03139, 135.86139], "images": []},
    {"name": "Nakayama dera (Hyogo)", "coords": [34.78583, 135.29222], "images": []},
    {"name": "Suma Rikyu Park", "coords": [34.65222, 135.21139], "images": []},
    {"name": "Awaji Island", "coords": [34.38333, 134.88333], "images": []},
    {"name": "Mount Shigi", "coords": [34.61667, 135.75000], "images": []},
    {"name": "Himeji - Acko", "coords": [34.81667, 134.68333], "images": []},
    {"name": "Nunobiki Falls", "coords": [34.72222, 135.19583], "images": []},
    {"name": "Yoshinoyama Nara", "coords": [34.36667, 135.76722], "images": []}
]

# -----------------------------
# 3. Create folders for each hike
# -----------------------------
images_root = "Images"
if not os.path.exists(images_root):
    os.mkdir(images_root)

for hike in hikes:
    folder_name = hike["name"].replace(" ", "_")
    folder_path = os.path.join(images_root, folder_name)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        print(f"📂 Created folder: {folder_path}")
    else:
        print(f"📂 Folder already exists: {folder_path}")

# -----------------------------
# 4. Add markers (popups empty for now)
# -----------------------------
for hike in hikes:
    popup_html = f"<b>{hike['name']}</b><br><i>Add images to {images_root}/{hike['name'].replace(' ', '_')}</i>"
    folium.Marker(location=hike["coords"], popup=popup_html).add_to(m)

# -----------------------------
# 5. Save map as index.html
# -----------------------------
m.save("index.html")
print("✅ Map saved as index.html! Add images to each folder and rerun the script to display them.")
