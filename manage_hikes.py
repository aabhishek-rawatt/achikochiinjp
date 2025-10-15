import os
import json
import shutil

images_root = "Images"
data_file = "hikes_data.json"

# Ensure Images folder exists
if not os.path.exists(images_root):
    os.mkdir(images_root)

# Load hikes
if os.path.exists(data_file):
    with open(data_file, "r", encoding="utf-8") as f:
        hikes = json.load(f)
else:
    hikes = []

# -----------------------------
# Helper functions
# -----------------------------
def save_hikes():
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(hikes, f, indent=4)

def create_hike_folder(name):
    folder_path = os.path.join(images_root, name.replace(" ", "_"))
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        print(f"📂 Folder created: {folder_path}")
    return folder_path

def list_hikes():
    if not hikes:
        print("❌ No hikes found.")
        return
    print("Current hikes:")
    for i, hike in enumerate(hikes, start=1):
        print(f"{i}. {hike['name']} - {hike['coords']}")

# -----------------------------
# Main menu
# -----------------------------
while True:
    print("\n--- Hike Manager ---")
    print("1. Add a hike")
    print("2. Delete a hike")
    print("3. Modify a hike")
    print("4. List all hikes")
    print("5. Exit")
    choice = input("Enter choice (1-5): ").strip()

    if choice == "1":  # Add
        name = input("Enter hike name: ").strip()
        lat = float(input("Enter latitude: ").strip())
        lon = float(input("Enter longitude: ").strip())
        hike_entry = {"name": name, "coords": [lat, lon], "images": []}
        hikes.append(hike_entry)
        create_hike_folder(name)
        save_hikes()
        print(f"✅ Hike '{name}' added.")

    elif choice == "2":  # Delete
        list_hikes()
        name_to_remove = input("Enter hike name to delete: ").strip()
        found = False
        for hike in hikes:
            if hike["name"].lower() == name_to_remove.lower():
                hikes.remove(hike)
                # Remove folder
                folder_path = os.path.join(images_root, hike["name"].replace(" ", "_"))
                if os.path.exists(folder_path):
                    shutil.rmtree(folder_path)
                    print(f"📂 Folder deleted: {folder_path}")
                found = True
                save_hikes()
                print(f"✅ Hike '{hike['name']}' removed.")
                break
        if not found:
            print(f"❌ Hike '{name_to_remove}' not found.")

    elif choice == "3":  # Modify
        list_hikes()
        name_to_modify = input("Enter hike name to modify: ").strip()
        found = False
        for hike in hikes:
            if hike["name"].lower() == name_to_modify.lower():
                found = True
                print(f"Current: {hike['name']} - {hike['coords']}")
                new_name = input("Enter new name (leave blank to keep same): ").strip()
                new_lat = input("Enter new latitude (leave blank to keep same): ").strip()
                new_lon = input("Enter new longitude (leave blank to keep same): ").strip()

                # Rename folder if name changes
                if new_name:
                    old_folder = os.path.join(images_root, hike["name"].replace(" ", "_"))
                    new_folder = os.path.join(images_root, new_name.replace(" ", "_"))
                    if os.path.exists(old_folder):
                        os.rename(old_folder, new_folder)
                        print(f"📂 Folder renamed: {old_folder} -> {new_folder}")
                    hike["name"] = new_name

                if new_lat:
                    hike["coords"][0] = float(new_lat)
                if new_lon:
                    hike["coords"][1] = float(new_lon)

                save_hikes()
                print(f"✅ Hike updated: {hike['name']} - {hike['coords']}")
                break
        if not found:
            print(f"❌ Hike '{name_to_modify}' not found.")

    elif choice == "4":  # List
        list_hikes()

    elif choice == "5":  # Exit
        print("Exiting Hike Manager.")
        break

    else:
        print("❌ Invalid choice. Enter 1-5.")
