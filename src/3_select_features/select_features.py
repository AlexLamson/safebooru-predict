#!/usr/bin/python3
import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils import *

import re
from collections import defaultdict
import pickle


def get_frequent_tags(filename):
	selected_tags = []
	# read the tags file
	with open(filename) as f:
		next(f) # skip header line
		for i, line in enumerate(f):
			match = re.compile(r"^(\d+),(.*)$").match(line)
			freq, tag = int(match.group(1)), match.group(2)

			# don't use more than this many features
			if i > 1000:
				break

			# exclude the tagme tag
			if tag == "tagme":
				continue

			# don't include tags that occur less than 100 times
			if freq < 100:
				break

			selected_tags.append(tag)
	return selected_tags


# make dict with tags as keys and indicies as values
def make_tag_index_map(tags):
	tag_index_map = defaultdict()
	for i, tag in enumerate(tags):
		tag_index_map[tag] = i
	return tag_index_map

def save_tag_index_map(filename, tag_index_map):
	pickle.dump(tag_index_map, open(filename, "wb"))

def load_tag_index_map(filename):
	tag_index_map = pickle.load(open(filename, "rb"))
	return tag_index_map


def main():
	# select features
	filename = booru_path("tags.csv")
	selected_tags = get_frequent_tags(filename)

	# create tag->index map
	tag_index_map = make_tag_index_map(selected_tags)

	# save tag->index map to file
	save_tag_index_map(booru_path("tag_index_map.p"), tag_index_map)

	# notify how many tags were selected to use as features
	print(len(selected_tags), "tags selected")

if __name__ == "__main__":
	main()
