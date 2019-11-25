#!/usr/bin/python3
import sys
sys.path.append('..')
from utils import *

import time
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
from math import sqrt
# from scipy.sparse import dok_matrix
# import numpy as np
import gc
from multiprocessing import Pool
from numpy import uint16


# have at most this many tags in the intersection matrix
goal_tags_total = 40e3


should_compute_intersections = not file_exists(booru_path("pickle_files/tag_intersection_counts.pkl"))
if not should_compute_intersections:
    print("tag_intersection_counts pickle file already exists")
    exit()

all_stats = load_obj(booru_path("pickle_files/statistics"))
total_images = all_stats["total_images"] - all_stats['number_of_duplicates']
total_tags = len(all_stats['all_unique_tags'])


print("computing minimum tag count requirement that uses the most space without exceeding RAM")
minimum_tag_count = 0
reasonable_tag_count = 1e20
while reasonable_tag_count > goal_tags_total:
    minimum_tag_count += 1
    all_reasonable_tags = [tag for tag in all_stats["all_unique_tags"] if all_stats["times_tag_occurred"][tag] >= minimum_tag_count]
    reasonable_tag_count = len(all_reasonable_tags)
all_reasonable_tags = [tag for tag in all_stats["all_unique_tags"] if all_stats["times_tag_occurred"][tag] >= minimum_tag_count]
print("A tag must occur at least {} times in the dataset in order to be counted".format(minimum_tag_count))
# all_reasonable_tags = [tag for tag in all_stats["all_unique_tags"] if all_stats["times_tag_occurred"][tag] >= 20]


print("making tag->index map & index->tag map")
tag_to_index = dict()
index_to_tag = dict()
for i, tag in enumerate(all_reasonable_tags):
    tag_to_index[tag] = i
    index_to_tag[i] = tag


if not should_compute_intersections:
    tag_to_index = load_obj(booru_path("pickle_files/tag_to_index"))
    index_to_tag = load_obj(booru_path("pickle_files/index_to_tag"))
    tag_intersection_counts = load_obj(booru_path("pickle_files/tag_intersection_counts"))
else:
    print("manually freeing up RAM")
    del all_stats
    gc.collect()

    print("processing rows of tags")
    tag_intersection_counts = defaultdict(int)
    with tqdm(total=total_images) as pbar:
        # df_iterator = pd.read_csv(booru_path("data/deduped_data.csv"), header=0, names=get_csv_header().split(","), encoding="utf-8", chunksize=10**2, nrows=10000)
        df_iterator = pd.read_csv(booru_path("data/deduped_data.csv"), header=0, names=get_csv_header().split(","), encoding="utf-8", chunksize=10**2)
        for df in df_iterator:
            for index, row in df.iterrows():
                pbar.update(1)

                # get the tags for one image
                tags = row["tags"].split()

                # all combinations of those tags
                for i in range(len(tags)):
                    for j in range(i+1,len(tags)):

                        # ignore infrequent tags
                        if tags[i] not in tag_to_index:
                            continue
                        if tags[j] not in tag_to_index:
                            continue

                        # record the co-occurrence of the two tags
                        tagid1 = tag_to_index[tags[i]]
                        tagid2 = tag_to_index[tags[j]]
                        smaller_index = min(tagid1, tagid2)
                        bigger_index = max(tagid1, tagid2)
                        tag_intersection_counts[(smaller_index, bigger_index)] += 1

                # end of df loop
            # end of df_iterator loop
        # end of tqdm with statement


    print("freeing up RAM again")
    del df
    gc.collect()

    print("saving results to files")
    save_obj(tag_to_index, booru_path("pickle_files/tag_to_index"))
    save_obj(index_to_tag, booru_path("pickle_files/index_to_tag"))
    save_obj(tag_intersection_counts, booru_path("pickle_files/tag_intersection_counts"))

    print("num of unique tags in sample :", reasonable_tag_count)
    print("(num of unique tags in sample)^2 :", reasonable_tag_count*reasonable_tag_count)
    print("number of intersecting pairs of tags :", len(tag_intersection_counts.keys()))
    print("sparsity (% non-zero entries) : {:.10f}%".format(len(tag_intersection_counts.keys())/(reasonable_tag_count*reasonable_tag_count)*100))

print("done computing sparse intersections")
