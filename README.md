Proof of Concept Checklist

- [x] backend: 
  - [x] implement in json
  - [x] Static: The entire data set will be version controlled and served statically
  - [x] Voidpet data:
    - [x] Each voidpet has 5 levels and thus 5 images in SVG format
    - [x] There are 50 void pets in total
    - [x] Classes are: Fighter, Tank, Healer
    - [x] Elements are: Wood, Earth, Water, Fire, Metal
- [x] web frontend: 
  - [x] include SVG for the classes (fighter, tank, healer)
  - [x] include SVG for the elements
  - [x] make a custom looking card with name, image, class and element
  - [ ] optional filtering is done clientside (-> dynamic endpoints possible!)
  - [ ] filter by class (fighter, tank, support, ..) or type (wood, fire, ..)


```
voidpet-spa/
├── src/
│   ├── lib/
│   │   ├── components/
│   │   │   ├── ui/
│   │   │   ├── filters/
│   │   │   └── voidpets/
│   │   ├── data/            # Helper modules to load static data
│   │   ├── stores/          # Svelte stores (filters, voidpet data cache)
│   │   └── utils/
│   │
│   ├── routes/              # SvelteKit routing (SPA-friendly)
│   │   ├── +layout.svelte
│   │   ├── +page.svelte
│   │   │
│   │   ├── api/voidpets/    # (Optional) dynamic endpoints using static data
│   │   │   ├── +server.ts   # e.g., return list of voidpets
│   │   │   ├── [id]/+server.ts
│   │   │   └── filters/+server.ts
│   │   │
│   │   └── voidpet/
│   │       └── [id]/+page.svelte
│   │
│   └── app.css
│
├── static/                  # Served as-is (no processing)
│   ├── data/                # Fully version-controlled backend data
│   │   ├── voidpets.json    # Master dataset (all pets)
│   │   └── voidpets/        # Individual pet directories
│   │       ├── 00/
│   │       │   └── ...
│   │       ├── 01/
│   │       │   ├── meta.json
│   │       ├── 02/
│   │       │   ├── meta.json
│   │       │   └── ...
│   │       └── ...
│   │
│   └── assets/              # Global SVGs, logos, backgrounds
│
├── scripts/                 # Generators, validators (optional)
│   ├── generate-voidpet-index.js
│   └── validate-data.js
│
├── .gitignore
├── package.json
├── svelte.config.js
└── README.md
```