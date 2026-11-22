# Raw Images Folder

Drop your high-resolution original photos here (JPG, PNG, WebP, etc.).

Name them according to where they belong on the website:
- `hero.jpg` (or `.png`) -> Hero Section (Portrait, 1000x1250)
- `work-living.jpg` -> Recent Work: Living Room (Portrait, 800x1100)
- `work-kitchen.jpg` -> Recent Work: Kitchen (Landscape, 1200x800)
- `work-wardrobe.jpg` -> Recent Work: Bedroom Wardrobe (Square, 900x900)
- `work-entrance.jpg` -> Recent Work: Entrance / Foyer (Square, 900x900)

Then run in your terminal:
```bash
python scripts/optimize-images.py
```

The script will automatically crop them to the ideal aspect ratios, compress them using high-efficiency WebP, and write them directly into `images/` ready for Vercel deployment!
