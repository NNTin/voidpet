import json
import os
import sys
import re

VOIDPETS_DIR = os.path.join("static", "data", "voidpets")

REQUIRED_FIELDS = ["id", "name", "class", "element", "rarity", "description", "levels"]
ALLOWED_CLASSES = ["Fighter", "Tank", "Healer"]
ALLOWED_ELEMENTS = ["Wood", "Earth", "Water", "Fire", "Metal"]
ALLOWED_RARITIES = ["Rare", "Epic", "Legendary"]
LEVEL_KEYS = ["1", "2", "3", "4", "5"]

# Regex to match valid asset paths like /assets/voidpets/anxious/1.svg
ASSET_PATH_REGEX = re.compile(r"^/assets/voidpets/[a-z0-9_-]+/[1-5]\.svg$")

def validate_meta(meta, dir_name):
    valid = True

    # Required fields
    for field in REQUIRED_FIELDS:
        if field not in meta:
            print(f"{dir_name}: Missing required field '{field}'")
            valid = False

    # Choices
    if "class" in meta and meta["class"] not in ALLOWED_CLASSES:
        print(f"{dir_name}: Invalid class '{meta['class']}'")
        valid = False

    if "element" in meta and meta["element"] not in ALLOWED_ELEMENTS:
        print(f"{dir_name}: Invalid element '{meta['element']}'")
        valid = False

    if "rarity" in meta and meta["rarity"] not in ALLOWED_RARITIES:
        print(f"{dir_name}: Invalid rarity '{meta['rarity']}'")
        valid = False

    # Levels
    if "levels" in meta:
        for key in LEVEL_KEYS:
            if key not in meta["levels"]:
                print(f"{dir_name}: Missing level '{key}'")
                valid = False
                continue

            path = meta["levels"][key]
            # Check path format
            if not ASSET_PATH_REGEX.match(path):
                print(f"{dir_name}: Invalid asset path '{path}' (should be /assets/voidpets/<name-lowercase>/N.svg)")
                valid = False

            # check if file exists
            # file_path = path.lstrip("/").replace("/", os.sep)
            # if not os.path.exists(file_path):
            #     print(f"{dir_name}: Asset file does not exist '{file_path}'")
            #     valid = False

    return valid

def validate_all():
    all_valid = True
    for dir_name in os.listdir(VOIDPETS_DIR):
        dir_path = os.path.join(VOIDPETS_DIR, dir_name)
        if not os.path.isdir(dir_path):
            continue

        meta_file = os.path.join(dir_path, "meta.json")
        if not os.path.exists(meta_file):
            print(f"{dir_name}: meta.json not found")
            all_valid = False
            continue

        with open(meta_file, "r", encoding="utf-8") as f:
            try:
                meta = json.load(f)
            except json.JSONDecodeError as e:
                print(f"{dir_name}: Invalid JSON ({e})")
                all_valid = False
                continue

            if not validate_meta(meta, dir_name):
                all_valid = False

    if all_valid:
        print("All voidpets passed validation ✅")
        sys.exit(0)
    else:
        print("Validation failed ❌")
        sys.exit(1)

if __name__ == "__main__":
    validate_all()
