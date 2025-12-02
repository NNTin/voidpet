import json
import os

VOIDPETS_DIR = os.path.join("static", "data", "voidpets")
OUTPUT_FILE = os.path.join("static", "data", "voidpets.json")

def is_directory(path):
    return os.path.exists(path) and os.path.isdir(path)

def generate_voidpets():
    pets = []
    for dir_name in os.listdir(VOIDPETS_DIR):
        dir_path = os.path.join(VOIDPETS_DIR, dir_name)
        if not is_directory(dir_path):
            continue

        meta_file = os.path.join(dir_path, "meta.json")
        if not os.path.exists(meta_file):
            print(f"Skipping {dir_name}: meta.json not found")
            continue

        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
            pets.append(meta)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(pets, f, indent=2)
    print(f"Generated {OUTPUT_FILE} with {len(pets)} voidpets.")

if __name__ == "__main__":
    generate_voidpets()
