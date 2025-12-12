#!/usr/bin/python3
# -*- coding=utf-8 -*-

#===================================
# @Filename: human_sample.py
# @Author: Longwei Zhang
# @Create Time: 2025-12-11 19:12:47
# @Email: longwei2@illinois.edu
# @Description: 
#===================================


import pandas as pd

CSV = "../labels_film.csv"
SPLIT = "test"
PER_CLASS = 10
SEED = 42
OUT = "../human_sample_filenames.txt"

df = pd.read_csv(CSV)


df = df[df["split"] == SPLIT]

sampled = (
    df.groupby("film_label", group_keys=False)
      .apply(lambda x: x.sample(n=PER_CLASS, random_state=SEED))
)


sampled = sampled.sample(frac=1, random_state=SEED)


sampled["filename"].to_csv(OUT, index=False, header=False)

print(f"Saved {len(sampled)} filenames to {OUT}")