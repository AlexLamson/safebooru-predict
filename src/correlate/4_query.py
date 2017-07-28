#!/usr/bin/python3
import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils import get_num_lines, booru_path

import numpy as np
import pandas as pd
from tqdm import tqdm
import operator


'''
load the correlation table
load the tags list
	make the tag_to_index_map

initialize an empty list of 2-tuples to store correlation_results

query correlation values in valid column elements
query correlation values in valid row elements

add each (tag, correlation_value) to correlation_results
sort correlation_results by correlation_value in descending order
cast correlation_results to numpy array to better visualize the beginning and end
print the correlation_results
'''

show_first_n = 13 #show the first n tags
show_last_n = 5 #show last n tags

num_tags_to_keep = 10000 #don't change this value unless you re-run the other scripts with the new value


# open the tags file to get a list of most frequent tags
print("reading tags file")
tags_file = booru_path("tags.csv")
tag_counts = pd.read_csv(tags_file, nrows=num_tags_to_keep, header=0, names=['occurrences', 'tag'])


# make a map from tags to (int) locations in the array
print("creating tag->index map")
tag_to_index_map = dict()
for index, row in tag_counts.iterrows():
	tag = row['tag']
	tag_to_index_map[tag] = index

# make a map from locations in the array to tags
print("creating index->tag map")
index_to_tag_map = dict()
for index, row in tag_counts.iterrows():
	tag = row['tag']
	index_to_tag_map[index] = tag


print("loading correlation_table into memory")
filename = booru_path('correlation_table.npy')
correlation_table = np.load(filename)


def get_correlations(query_tag):
	correlation_results = []
	
	# check that the tag is one that has correlations calculated
	if query_tag not in tag_to_index_map:
		print("ERROR '{}' not in the {} available tags".format(query_tag, num_tags_to_keep))
		return []

	# print("gathering correlated tags")
	query_index = tag_to_index_map[query_tag]
	# print("query_index: {}".format(query_index))
	# print("the tag really is {}, right?".format(index_to_tag_map[query_index]))

	elements_in_query_column = query_index
	elements_in_query_row = num_tags_to_keep-1-query_index
	# NOTE: syntax here is:  correlation_table[row, col]

	# query correlation values in valid column elements
	for row in range(elements_in_query_column):
		correlation_value = correlation_table[row, query_index]
		other_tag = index_to_tag_map[row]
		correlation_results.append( (other_tag, correlation_value) )

	# query correlation values in valid row elements
	for col in range(elements_in_query_row):
		correlation_value = correlation_table[query_index, col]
		other_tag = index_to_tag_map[col]
		correlation_results.append( (other_tag, correlation_value) )

	# sort the results by their correlation in descending order
	correlation_results.sort(key=operator.itemgetter(1), reverse=True)

	return correlation_results


correlation_strings = []
print("="*20)
should_keep_running = True
while should_keep_running:
	# receive the user input
	query_tag = input("enter a query tag (ex. coffee) or 'quit' or 'tofile': ")

	# quit the program
	if query_tag in ["quit", "exit", "q"]:
		should_keep_running = False
		continue

	# write previous results to a file
	if query_tag == "tofile":
		# write the results to a file
		print("writing query results to file")
		with open(booru_path("query_results.csv"), 'w') as fp:
			fp.write("\n".join(correlation_strings))
		continue

	# use a space at the start or end like a wildcard to find tags
	if " " in query_tag:
		a = query_tag.startswith(" ")
		b = query_tag.endswith(" ")
		def is_match(tag):
			return (a and tag.endswith(query_tag.strip())) or (b and tag.startswith(query_tag.strip()))

		possible_tags = [tag for tag in tag_to_index_map if is_match(tag)]

		if len(possible_tags) == 0:
			print("Couldn't find any matches for {}".format(query_tag))
		elif len(possible_tags) == 1:
			query_tag = possible_tags[0]
		else:
			print("Matches:")
			print("="*20)
			print("\n".join(possible_tags))
			continue

	# query_tag = query_tag.replace(" ","_")
	correlation_results = get_correlations(query_tag)
	
	if len(correlation_results) == 0:
		continue

	# print the most and least correlated items
	# correlation_strings = ["{},{:.4f}".format(a,b) for a,b in correlation_results]
	correlation_strings = ["{: .4f} {}".format(b,a) for a,b in correlation_results]
	print("="*20)
	# print("QUERY: {}".format(query_tag))
	print("\n".join(correlation_strings[:show_first_n]))
	print("...")
	print("\n".join(correlation_strings[-show_last_n:]))
	print("="*20)
