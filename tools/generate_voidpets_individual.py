import json
import subprocess
import os

with open("static/data/voidpets.json", "r", encoding="utf-8") as f:
    pets = json.load(f)

TEMPLATE = ".\\tools\\cookiecutter-voidpet"
OUTPUT_DIR = ".\\static\\data\\voidpets"

for pet in pets:
    subprocess.run([
        ".venv\\Scripts\\cookiecutter",
        TEMPLATE,
        "--no-input",
        "--output-dir", OUTPUT_DIR,
        f"id={pet['id']}",
        f"name={pet['name']}",
        f"class={pet['class']}",
        f"element={pet['element']}",
        f"rarity={pet['rarity']}",
        f"description={pet['description']}"
    ])
