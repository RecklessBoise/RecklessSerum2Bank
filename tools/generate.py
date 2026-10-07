"""Generate the RecklessSerum2Bank_1 preset bank.

Usage: python tools/generate.py [--out RecklessSerum2Bank_1] [--seed 1312]
"""
import argparse
import json
import os
import random
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))

from serum2_codec import write_preset  # noqa: E402
from sounds import CATEGORIES, STYLES, STYLE_TAGS, make  # noqa: E402

BANK = "RecklessSerum2Bank_1"

WORDS = {
    "hollis": (
        ["Glass", "Neon", "Halo", "Chrome", "Angel", "Sugar", "Laser", "Prism", "Mirror", "Glitter",
         "Gloss", "Fever", "Heart", "Candy", "Silver", "Satin", "Velour", "Star", "Ultra", "Hyper"],
        ["Rush", "Bloom", "Kiss", "Drive", "Tears", "Rain", "Flash", "Dream", "Wings", "Pulse",
         "Love", "Shine", "Ride", "Burn", "Night", "Sky", "Daze", "Crush", "Lights", "Static"],
    ),
    "mink": (
        ["Cold", "Basement", "Tape", "Rust", "Smoke", "Concrete", "Fog", "Low", "Ghost", "Dirty",
         "Blur", "Damp", "Hollow", "Bruise", "Gutter", "Grain", "Muddy", "Sour", "Numb", "Grey"],
        ["Block", "Room", "Hum", "Floor", "Corner", "Alley", "Wax", "Cough", "Stain", "Static",
         "Ritual", "Tunnel", "Ward", "Drip", "Hood", "Signal", "Trap", "Scar", "Ash", "Fade"],
    ),
    "castles": (
        ["Chip", "Cartridge", "Pixel", "Arcade", "Strobe", "Hex", "Cathode", "LoRes", "Bit", "Shard",
         "Bleach", "Fracture", "Void", "Witch", "Ruin", "Coven", "Glitch", "Cursed", "Broken", "Black"],
        ["Siren", "Ghost", "Scream", "Mask", "Spell", "Gate", "Prayer", "Sprite", "Static", "Teeth",
         "Halo", "Crown", "Tomb", "Mirror", "Flood", "Candle", "Veil", "Error", "Doll", "Ritual"],
    ),
    "electro": (
        ["Aqua", "Hydro", "Circuit", "Voltage", "Orbit", "Grid", "Robot", "Sonar", "Vector", "Bunker",
         "Data", "Deep", "Chrome", "Mainframe", "Polar", "Delta", "Nitro", "Turbo", "Dark", "Trans"],
        ["Drift", "Current", "Pressure", "Machine", "System", "Transit", "Signal", "Beacon", "Zone", "Sector",
         "Wave", "Engine", "Rhythm", "Code", "Probe", "Unit", "Abyss", "Matrix", "Station", "Funk"],
    ),
}


def unique_name(rng, style, prefix, used):
    first, second = WORDS[style]
    for _ in range(500):
        name = f"{prefix} - {rng.choice(first)} {rng.choice(second)}"
        if name.lower() not in used:
            used.add(name.lower())
            return name
    raise RuntimeError("name space exhausted")


def build(out_dir, seed):
    rng = random.Random(seed)
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    used, manifest = set(), []
    tables, noises = set(), set()
    for category, prefix, _fn, _tags, count in CATEGORIES:
        folder = os.path.join(out_dir, category)
        os.makedirs(folder)
        for i in range(count):
            style = STYLES[i % len(STYLES)]
            name = unique_name(rng, style, prefix, used)
            p = make(category, style, random.Random(rng.random()), name)
            meta, state = p.build()
            write_preset(os.path.join(folder, name + ".SerumPreset"), meta, state)
            tables |= p.tables_used
            noises |= p.noises_used
            manifest.append({"name": name, "category": category, "style": STYLE_TAGS[style]})
    with open(os.path.join(os.path.dirname(out_dir) or ".", "manifest.json"), "w") as f:
        json.dump({"bank": BANK, "seed": seed, "count": len(manifest), "presets": manifest,
                   "factory_tables": sorted(tables), "factory_noises": sorted(noises)}, f, indent=1)
    return manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=BANK)
    ap.add_argument("--seed", type=int, default=1312)
    args = ap.parse_args()
    manifest = build(args.out, args.seed)
    print(f"wrote {len(manifest)} presets to {args.out}")


if __name__ == "__main__":
    main()
