#!/usr/bin/python3
# -*- coding=utf-8 -*-

#===================================
# @Filename: split_by_yimeng.py
# @Author: Longwei Zhang
# @Create Time: 2025-12-02 13:31:40
# @Email: longwei2@illinois.edu
# @Description: 
#===================================

from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split 

ROOT = Path("..") 
CSV_PATH = ROOT / "labels.csv"

OUTPUT_ALL = ROOT / "labels_split_by_yimeng.csv"
SPLIT_DIR = ROOT / "splits_by_yimeng"

RANDOM_SEED = 42
TRAIN_RATIO = 0.7
VAL_RATIO = 0.15 
# =========================


def make_gf_label(persons: str) -> int:
    if persons == 'none':
        return 0
    elif 'yimeng' in persons:
        return 1
    else:
        return 0


def main():
    if not CSV_PATH.is_file():
        raise FileNotFoundError(f"CSV Not Found: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)
    print(f"Reading {CSV_PATH}, {len(df)} rows found.")


    df["gf_label"] = df["person"].apply(make_gf_label)

    print("gf_label distribution:")
    print(df["gf_label"].value_counts())

    test_ratio = 1.0 - TRAIN_RATIO - VAL_RATIO
    if test_ratio <= 0:
        raise ValueError("TRAIN_RATIO + VAL_RATIO must be < 1.0")

    df_train_val, df_test = train_test_split(
        df,
        test_size=test_ratio,
        stratify=df["gf_label"],
        random_state=RANDOM_SEED,
    )


    val_fraction = VAL_RATIO / (TRAIN_RATIO + VAL_RATIO)

    df_train, df_val = train_test_split(
        df_train_val,
        test_size=val_fraction,
        stratify=df_train_val["gf_label"],
        random_state=RANDOM_SEED,
    )

    print("\nresults after split:")
    for name, sub_df in [("train", df_train), ("val", df_val), ("test", df_test)]:
        counts = sub_df["gf_label"].value_counts().to_dict()
        print(f"{name}: {len(sub_df)} rows, label : {counts}")

    df_train = df_train.copy()
    df_val = df_val.copy()
    df_test = df_test.copy()

    df_train["split"] = "train"
    df_val["split"] = "val"
    df_test["split"] = "test"

    df_all = pd.concat([df_train, df_val, df_test], ignore_index=True)

    SPLIT_DIR.mkdir(parents=True, exist_ok=True)
    df_all.to_csv(OUTPUT_ALL, index=False)
    df_train.to_csv(SPLIT_DIR / "gf_binary_train.csv", index=False)
    df_val.to_csv(SPLIT_DIR / "gf_binary_val.csv", index=False)
    df_test.to_csv(SPLIT_DIR / "gf_binary_test.csv", index=False)

    print(f"\n✅ OUTPUT: {OUTPUT_ALL}")
    print(f"✅ SPLIT: {SPLIT_DIR.resolve()}")


if __name__ == "__main__":
    main()
