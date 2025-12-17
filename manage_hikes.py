import json
import os

data_file = "hikes_data.json"
images_root = "Images"

# Ensure hikes data exists
if not os.path.exists(data_file):
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4, ensure_ascii=False)

# Load existing hikes
with open(data_file, "r", encoding="utf-8") as f:
    hikes = json.load(f)

def save_hikes():
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(hikes, f, indent=4, ensure_ascii=False)

def list_hikes():
    if not hikes:
        print("No hikes yet.")
        return
    print("\nCurrent hikes:")
    for i, hike in enumerate(hikes, 1):
        name_en = hike.get("name", "")
        name_ja = hike.get("name_ja", "")
        prefecture = hike.get("prefecture", "")
        print(f"{i}. {name_en} / {name_ja} [{prefecture}] - {hike['coords']}")

def add_hike():
    name = input("Enter hike name (English): ").strip()
    name_ja = input("Enter hike name (Japanese, optional): ").strip()
    prefecture = input("Enter prefecture (optional): ").strip()

    try:
        lat = float(input("Enter latitude: ").strip())
        lon = float(input("Enter longitude: ").strip())
    except ValueError:
        print("Invalid coordinates!")
        return

    hike = {
        "name": name,
        "name_ja": name_ja,
        "prefecture": prefecture,
        "coords": [lat, lon]
    }

    hikes.append(hike)
    save_hikes()

    # Create folder automatically (English name only)
    os.makedirs(images_root, exist_ok=True)
    folder_name = name.replace(" ", "_")
    folder_path = os.path.join(images_root, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    print(f"📂 Folder ensured: {folder_path}")
    print(f"✅ Hike '{name}' added!")

def modify_hike():
    list_hikes()
    try:
        idx = int(input("Enter the number of hike to modify: ").strip()) - 1
        if idx < 0 or idx >= len(hikes):
            print("Invalid selection!")
            return
    except ValueError:
        print("Invalid input!")
        return

    hike = hikes[idx]

    print(f"\nModifying '{hike.get('name', '')}'")

    # ---- Names ----
    new_name = input(
        f"New English name (Enter to keep '{hike.get('name', '')}'): "
    ).strip()

    if new_name:
        old_folder = os.path.join(images_root, hike["name"].replace(" ", "_"))
        new_folder = os.path.join(images_root, new_name.replace(" ", "_"))
        if os.path.exists(old_folder):
            os.rename(old_folder, new_folder)
            print(f"📂 Folder renamed to {new_folder}")
        hike["name"] = new_name

    hike["name_ja"] = input(
        f"New Japanese name (Enter to keep '{hike.get('name_ja', '')}'): "
    ).strip() or hike.get("name_ja", "")

    hike["prefecture"] = input(
        f"New prefecture (Enter to keep '{hike.get('prefecture', '')}'): "
    ).strip() or hike.get("prefecture", "")

    # ---- Coordinates ----
    try:
        lat = input(f"Latitude (Enter to keep {hike['coords'][0]}): ").strip()
        lon = input(f"Longitude (Enter to keep {hike['coords'][1]}): ").strip()
        if lat:
            hike["coords"][0] = float(lat)
        if lon:
            hike["coords"][1] = float(lon)
    except ValueError:
        print("Invalid coordinates! Keeping old values.")

    save_hikes()
    print("✅ Hike modified!")

def delete_hike():
    list_hikes()
    try:
        idx = int(input("Enter the number of hike to delete: ").strip()) - 1
        if idx < 0 or idx >= len(hikes):
            print("Invalid selection!")
            return
    except ValueError:
        print("Invalid input!")
        return

    hike = hikes.pop(idx)
    save_hikes()

    folder_path = os.path.join(images_root, hike["name"].replace(" ", "_"))
    print(f"✅ Hike '{hike['name']}' deleted from data.")
    if os.path.exists(folder_path):
        print(f"Note: Folder '{folder_path}' still exists.")

# -----------------------------
# Main menu
# -----------------------------
while True:
    print("\n--- Manage Hikes ---")
    print("1. List hikes")
    print("2. Add hike")
    print("3. Modify hike")
    print("4. Delete hike")
    print("5. Exit")

    choice = input("Enter choice: ").strip()
    if choice == "1":
        list_hikes()
    elif choice == "2":
        add_hike()
    elif choice == "3":
        modify_hike()
    elif choice == "4":
        delete_hike()
    elif choice == "5":
        print("Exiting.")
        break
    else:
        print("Invalid choice!")
