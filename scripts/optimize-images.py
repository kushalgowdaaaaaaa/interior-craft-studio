#!/usr/bin/env python3
"""
Interior Craft Studio - Image Optimization Utility
Optimizes images for ultra-fast loading and minimal bandwidth on Vercel Free Tier.
Converts any image (PNG, JPG, TIFF) to compressed, high-fidelity WebP format with exact dimensions.
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageOps

# Preset configurations matching index.html layout & CSS grid
PRESETS = {
    "hero": {
        "width": 1000,
        "height": 1250,
        "target": "images/hero.webp",
        "quality": 82,
        "description": "Hero section (portrait 4:5)",
    },
    "work-living": {
        "width": 800,
        "height": 1100,
        "target": "images/work-living.webp",
        "quality": 80,
        "description": "Living room project (portrait 8:11)",
    },
    "work-kitchen": {
        "width": 1200,
        "height": 800,
        "target": "images/work-kitchen.webp",
        "quality": 80,
        "description": "Kitchen project (landscape 3:2)",
    },
    "work-wardrobe": {
        "width": 900,
        "height": 900,
        "target": "images/work-wardrobe.webp",
        "quality": 80,
        "description": "Bedroom/Wardrobe project (square 1:1)",
    },
    "work-entrance": {
        "width": 900,
        "height": 900,
        "target": "images/work-entrance.webp",
        "quality": 80,
        "description": "Entrance/Foyer project (square 1:1)",
    },
}

def crop_and_resize(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """Center-crops and resizes image using high-quality Lanczos resampling."""
    img = ImageOps.exif_transpose(img)
    target_aspect = target_w / target_h
    current_aspect = img.width / img.height

    if abs(current_aspect - target_aspect) > 0.01:
        # Crop to target aspect ratio
        if current_aspect > target_aspect:
            # Source is wider than target: crop left & right
            new_w = int(img.height * target_aspect)
            offset = (img.width - new_w) // 2
            img = img.crop((offset, 0, offset + new_w, img.height))
        else:
            # Source is taller than target: crop top & bottom
            new_h = int(img.width / target_aspect)
            offset = (img.height - new_h) // 2
            img = img.crop((0, offset, img.width, offset + new_h))

    # Resize to exact dimensions
    return img.resize((target_w, target_h), Image.Resampling.LANCZOS)

def optimize_file(src_path: str, dest_path: str, target_w: int, target_h: int, quality: int = 80):
    """Compresses and saves image as WebP."""
    src = Path(src_path)
    dest = Path(dest_path)
    dest.parent.mkdir(parents=True, exist_ok=True)

    initial_size = src.stat().st_size
    with Image.open(src) as img:
        # Handle RGBA vs RGB
        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            processed = crop_and_resize(img.convert("RGBA"), target_w, target_h)
            processed.save(dest, "WEBP", quality=quality, method=6)
        else:
            processed = crop_and_resize(img.convert("RGB"), target_w, target_h)
            processed.save(dest, "WEBP", quality=quality, method=6)

    final_size = dest.stat().st_size
    pct_saved = ((initial_size - final_size) / initial_size) * 100 if initial_size > 0 else 0
    print(f"[OK] Saved: {dest} ({target_w}x{target_h}) | {initial_size // 1024} KB -> {final_size // 1024} KB (-{pct_saved:.1f}%)")

def process_input_folder(input_dir: str = "images-raw"):
    """Scans images-raw folder for preset names or matching filenames."""
    in_path = Path(input_dir)
    if not in_path.exists():
        in_path.mkdir(parents=True, exist_ok=True)
        print(f"Created '{input_dir}' folder. Drop your original photos here (e.g. hero.jpg, work-living.png).")
        return

    files = [f for f in in_path.iterdir() if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff")]
    if not files:
        print(f"No image files found in '{input_dir}'.")
        print("Tip: Drop your photos into this folder with any of these names:")
        for key in PRESETS:
            print(f"  - {key}.jpg  ({PRESETS[key]['description']})")
        return

    print(f"\nProcessing {len(files)} image(s) from '{input_dir}'...")
    for f in files:
        stem = f.stem.lower()
        # Find matching preset
        matched_preset = None
        for key, config in PRESETS.items():
            if stem == key or stem.replace("-", "_") == key.replace("-", "_"):
                matched_preset = (key, config)
                break

        if matched_preset:
            key, cfg = matched_preset
            optimize_file(str(f), cfg["target"], cfg["width"], cfg["height"], cfg["quality"])
        else:
            print(f"⚠ Skipping '{f.name}': Name did not match any preset ({', '.join(PRESETS.keys())}).")

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print("Usage:")
        print("  python scripts/optimize-images.py                # Batch process images in 'images-raw/'")
        print("  python scripts/optimize-images.py <src> <preset> # Process a specific file with a preset")
        print("Presets:", ", ".join(PRESETS.keys()))
        return

    if len(sys.argv) == 3:
        src = sys.argv[1]
        preset_name = sys.argv[2]
        if preset_name not in PRESETS:
            print(f"Error: Unknown preset '{preset_name}'. Choose from: {list(PRESETS.keys())}")
            sys.exit(1)
        cfg = PRESETS[preset_name]
        optimize_file(src, cfg["target"], cfg["width"], cfg["height"], cfg["quality"])
        return

    process_input_folder()

if __name__ == "__main__":
    main()
