import json
import os
import sys
from jsonschema import validate, ValidationError

# Paths
VOIDPETS_DIR = os.path.join("static", "data", "voidpets")
SCHEMA_FILE = os.path.join("tools", "schema.json")  # Adjust if schema.json is elsewhere

# Load schema
with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
    schema = json.load(f)


def validate_file_exists(level_path):
    """Check if the SVG asset exists on disk."""
    file_path = os.path.join("static", level_path.lstrip("/").replace("/", os.sep))
    if not os.path.exists(file_path):
        return False, file_path
    return True, file_path


def validate_meta_file(meta_file, dir_name):
    """Validate a single meta.json file against schema and assets."""
    try:
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
    except json.JSONDecodeError as e:
        print(f"{dir_name}: Invalid JSON ({e})")
        return False

    valid = True

    # JSON Schema validation
    try:
        validate(instance=meta, schema=schema)
    except ValidationError as e:
        print(f"{dir_name}: Schema validation error: {e.message}")
        valid = False

    # Check if level asset files exist
    if "levels" in meta:
        for key, path in meta["levels"].items():
            exists, file_path = validate_file_exists(path)
            if not exists:
                print(f"{dir_name}: Asset file does not exist: '{file_path}'")
                valid = False

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

        if not validate_meta_file(meta_file, dir_name):
            all_valid = False

    if all_valid:
        print("All voidpets passed validation ✅")
        sys.exit(0)
    else:
        print("Validation failed ❌")
        sys.exit(1)


if __name__ == "__main__":
    validate_all()
