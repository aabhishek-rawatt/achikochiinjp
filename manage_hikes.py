import json
import os

data_file = "hikes_data.json"
images_root = "Images"

# Ensure hikes data exists
if not os.path.exists(data_file):
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4)

# Load existing hikes
with open(data_file, "r", encoding="utf-8") as f:
    hikes = json.load(f)

def save_hikes():
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(hikes, f, indent=4)

def list_hikes():
    if not hikes:
        print("No hikes yet.")
        return
    print("\nCurrent hikes:")
    for i, hike in enumerate(hikes, 1):
        print(f"{i}. {hike['name']} - {hike['coords']}")

def add_hike():
    name = input("Enter hike name: ").strip()
    try:
        lat = float(input("Enter latitude: ").strip())
        lon = float(input("Enter longitude: ").strip())
    except ValueError:
        print("Invalid coordinates!")
        return
    hike = {"name": name, "coords": [lat, lon], "images": []}
    hikes.append(hike)
    save_hikes()

    # Create folder automatically
    folder_name = name.replace(" ", "_")
    folder_path = os.path.join(images_root, folder_name)
    if not os.path.exists(images_root):
        os.mkdir(images_root)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        print(f"📂 Created folder: {folder_path}")
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
    print(f"Modifying '{hike['name']}'")
    new_name = input(f"Enter new name (or press Enter to keep '{hike['name']}'): ").strip()
    if new_name:
        # Rename folder
        old_folder = os.path.join(images_root, hike['name'].replace(" ", "_"))
        new_folder = os.path.join(images_root, new_name.replace(" ", "_"))
        if os.path.exists(old_folder):
            os.rename(old_folder, new_folder)
            print(f"📂 Folder renamed to {new_folder}")
        hike['name'] = new_name

    try:
        lat = input(f"Enter new latitude (or press Enter to keep {hike['coords'][0]}): ").strip()
        lon = input(f"Enter new longitude (or press Enter to keep {hike['coords'][1]}): ").strip()
        if lat: hike['coords'][0] = float(lat)
        if lon: hike['coords'][1] = float(lon)
    except ValueError:
        print("Invalid coordinates! Keeping old values.")

    save_hikes()
    print(f"✅ Hike '{hike['name']}' modified!")

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
    folder_path = os.path.join(images_root, hike['name'].replace(" ", "_"))
    print(f"✅ Hike '{hike['name']}' deleted from data.")
    if os.path.exists(folder_path):
        print(f"Note: Folder '{folder_path}' still exists. You can delete it manually if you want.")


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
