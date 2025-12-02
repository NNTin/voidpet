from bs4 import BeautifulSoup
import os
import json

# Paths
html_file_path = "./static/data/voidpets.html"
output_base_path = "./static/assets/voidpets"  # Base folder to save SVGs
os.makedirs(output_base_path, exist_ok=True)

# Read the HTML
with open(html_file_path, "r", encoding="utf-8") as f:
    html = f.read()

# Parse HTML
soup = BeautifulSoup(html, "html.parser")

# Find the main container
container = soup.find("div", class_="mt-4 gap-8 px-4 w-full")

voidpets_data = []

# Iterate over each card
for idx, card in enumerate(container.find_all("div", class_="w-full flex px-0 p-4 rounded-md relative")):
    # Extract title text: "#0: Envy"
    title_div = card.find(
        "div",
        class_="absolute top-0 left-0 mono-font py-0 sm:py-1 px-2 sm:px-3 text-black text-xs sm:text-sm font-bold"
    )
    title_text = title_div.get_text(strip=True) if title_div else "Unknown"

    # Split number and name
    if ":" in title_text:
        num_str, name = title_text.split(":", 1)
        num_str = num_str.strip().replace("#", "")
        name = name.strip()
    else:
        num_str = str(idx).zfill(2)
        name = title_text

    # Extract link slug for folder naming
    link_tag = card.find("a")
    pet_slug = link_tag['href'].split("/")[-1] if link_tag else f"pet{idx}"

    # Create folder for this pet
    pet_folder = os.path.join(output_base_path, pet_slug)
    os.makedirs(pet_folder, exist_ok=True)

    # Find all SVGs inside the card
    svgs = card.find_all("svg")
    svg_paths = {}
    svg_counter = 1

    for svg in svgs:
        # Skip empty SVGs
        if not svg.find():  # No child elements
            continue

        # Ensure xmlns attribute is present
        svg['xmlns'] = "http://www.w3.org/2000/svg"

        svg_filename = f"{svg_counter}.svg"
        svg_path = os.path.join(pet_folder, svg_filename)
        svg_paths[str(svg_counter)] = f"/assets/voidpets/{pet_slug}/{svg_filename}"

        # Save SVG content
        with open(svg_path, "w", encoding="utf-8") as svg_file:
            svg_file.write(str(svg))

        svg_counter += 1

    # Build JSON object for this voidpet
    voidpet_json = {
        "id": num_str.zfill(2),
        "name": name,
        "class": "Unknown",
        "element": "Metal",
        "rarity": "Unknown",
        "description": f"Describe this voidpet {name}...",
        "levels": svg_paths
    }

    voidpets_data.append(voidpet_json)

# Save metadata JSON
# with open("voidpets.json", "w", encoding="utf-8") as json_file:
#     json.dump(voidpets_data, json_file, indent=2)

print(f"Saved {len(voidpets_data)} voidpets and their SVGs to {output_base_path}")