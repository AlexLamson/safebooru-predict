#!/usr/bin/python3
import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils import get_num_lines

import numpy as np
import pandas as pd
from scipy.sparse import lil_matrix
import time
from tqdm import tqdm



col_names = ['id','created_at','rating','score','sample_url','sample_width','sample_height','preview_url','preview_width','preview_height','tags']

num_tags_to_keep = 10000
# num_tags_to_keep = 40000 # OSError: 1600000000 requested and 0 written
'''
This number is how many of the top tags will be used when calculating correlations.
I have to limit the number of tags because it costs O(D^2) space, which blows up fast.
I chose the number using the following formula:
5 GB = 4 bytes * (x table width)^2 / 1000000000 bytes per GB
'''


# open the tags file to get a list of most frequent tags
print("reading tags file")
tags_file = "../../res/safebooru/tags.csv"
tag_counts = pd.read_csv(tags_file, nrows=num_tags_to_keep, header=0, names=['occurrences', 'tag'])


# make a map from tags to (int) indices in the table
print("creating tag->index map")
from collections import defaultdict
tag_index_map = defaultdict(lambda: -1)
for index, row in tag_counts.iterrows():
	tag = row['tag']
	tag_index_map[tag] = index


# make the more frequently used tag come first in the pair
def tag_pair_to_cell_coords(tag1, tag2):
	tag1_rank = tag_index_map[tag1]
	tag2_rank = tag_index_map[tag2]
	if tag1_rank < tag2_rank:
		return (tag1_rank, tag2_rank)
	else:
		return (tag2_rank, tag1_rank)


# table of counts representing number of times each pair of tags occurred together
# the index->tag is represented in the tag_index_map dict
and_table = np.zeros(shape=(num_tags_to_keep, num_tags_to_keep), dtype=np.uint32)
# and_table = lil_matrix((num_tags_to_keep, num_tags_to_keep), dtype=np.uint32) #maybe improve space efficiency in the future?


# filename = "../../res/safebooru/data/head_safebooru.csv"
filename = "../../res/safebooru/data/safebooru.csv"

print("reading chunks from {}".format(filename))
num_lines = get_num_lines(filename)
chunksize = 50
# for chunk in tqdm(pd.read_csv(filename, chunksize=chunksize, header=0, usecols=['tags'], names=col_names), total=num_lines/chunksize+1):
for chunk in tqdm(pd.read_csv(filename, chunksize=chunksize, header=0, index_col='id', usecols=['id','tags'], names=col_names), total=num_lines/chunksize+1):
	for index, line in chunk.iterrows():
		if type(line['tags'])==float:
			print("float error on image with id {}".format(index))
		else:
			s = line['tags']
			tags = s.split()
			for i1 in range(len(tags)):
				for i2 in range(i1+1, len(tags)):
					tag1 = tags[i1]
					tag2 = tags[i2]

					tag1_rank, tag2_rank = tag_pair_to_cell_coords(tag1, tag2)
					and_table[tag1_rank, tag2_rank] += 1


print("saving and_table to {}".format(filename))
filename = '../../res/safebooru/and_table.npy'
np.save(filename, and_table)
# d = np.load(filename)
# print(np.all(d == and_table))


print("program done!")

