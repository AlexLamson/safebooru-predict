#!/usr/bin/python3
import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils import *

import time
from collections import defaultdict
from tqdm import tqdm
import pandas as pd


def open_with_pandas_read_csv(filename):
	start = time.time()
	# df = pd.read_csv(filename, index_col=['id'], header=0, usecols=['id','tags'], names=['id','created_at','rating','score','sample_url','sample_width','sample_height','preview_url','preview_width','preview_height','tags'])
	df = pd.read_csv(filename, header=0, usecols=['tags'], names=['id','created_at','rating','score','sample_url','sample_width','sample_height','preview_url','preview_width','preview_height','tags'])
	end = time.time()
	print("{} seconds elapsed".format(end - start))
	return df


# tag_counts is a dictionary with the keys being tags and the values being the number of times that tag has been seen
def get_tag_counts(filename):
	tag_counts = defaultdict(int)

	df = open_with_pandas_read_csv(filename)

	for index, row in tqdm(df.iterrows(), total=df.shape[0]):
		if type(row[0])==float:
			print("index: {}".format(index))
		else:
			tags = row[0].split()
			for tag in tags:
				tag_counts[tag] += 1

	return tag_counts


def write_tag_counts(tag_counts, filename):
	tags_file = open(filename,"w")
	tags_file.write("occurrences,tag\n")

	# sorted by count
	for tag in sorted(tag_counts, key=tag_counts.get, reverse=True):
		num_occurrences = tag_counts[tag]

		tag = '"'+tag.strip().replace('"','""')+'"' # make it csv friendly

		tags_file.write("{},{}\n".format(num_occurrences, tag))

	tags_file.close()


def main():
	# filename = booru_path("data/head_all_images.csv")
	filename = booru_path("data/all_images.csv")

	tag_counts = get_tag_counts(filename)
	write_tag_counts(tag_counts, filename=booru_path("tags.csv"))

if __name__ == "__main__":
	main()
