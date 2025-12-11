#!/usr/bin/python3
# -*- coding=utf-8 -*-

#===================================
# @Filename: label.py
# @Author: Longwei Zhang
# @Create Time: 2025-12-02 12:58:35
# @Email: longwei2@illinois.edu
# @Description: 
#===================================

from pathlib import Path
import csv

RAW_DIR = Path("../raw_photos")

PERSON_FOLDERS = {
    "yimeng": Path("../yimeng"),   
    "longwei": Path("../longwei"), 
    "parents": Path("../parents"),  
    'yu': Path("../yu"),
}

OUTPUT_CSV = Path("../labels.csv")

VALID_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}


def build_person_index() -> dict:

    index = {}
    for person_label, folder in PERSON_FOLDERS.items():
        if not folder.is_dir():
            print(f"[Warning] {folder} (label={person_label}), IGNORE")
            continue
        for f in folder.iterdir():
            if f.is_file() and f.suffix.lower() in VALID_EXTS:
                name = f.name 
                if name not in index:
                    index[name] = set()
                index[name].add(person_label)
    total_files = sum(len(v) > 0 for v in index.values())
    print(f"{total_files} files found in PERSON_FOLDERS.")
    return index


def parse_film_info(filename: str):
    stem = filename.rsplit(".", 1)[0]
    parts = stem.split("_")
    if len(parts) < 2:
        return "unknown", "unknown"
    brand = parts[0]
    film_type = parts[1]
    return brand, film_type


def main():
    if not RAW_DIR.is_dir():
        raise FileNotFoundError(f"[Warning]: {RAW_DIR}")

    person_index = build_person_index()

    rows = []
    for f in sorted(RAW_DIR.iterdir()):
        if not f.is_file():
            continue
        if f.suffix.lower() not in VALID_EXTS:
            continue

        filename = f.name
        person = person_index.get(filename, "none")
        film_brand, film_type = parse_film_info(filename)

        rows.append([filename, person, film_brand, film_type])

    print(f"[INFO] {len(rows)} pictures --> {OUTPUT_CSV}")

    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.writer(fp)
        writer.writerow(["filename", "person", "film_brand", "film_type"])
        writer.writerows(rows)

    print("✅ labels.csv completed.")


if __name__ == "__main__":
    main()
