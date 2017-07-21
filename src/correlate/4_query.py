#!/usr/bin/python3
import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils import get_num_lines

import numpy as np
import pandas as pd
from tqdm import tqdm
import operator



query_tag = "coffee" #note: no longer used


num_tags_to_keep = 10000 #don't change this value unless you re-run the other scripts with the new value


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

# open the tags file to get a list of most frequent tags
print("reading tags file")
tags_file = "../../res/safebooru/tags.csv"
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
filename = '../../res/correlation_table.npy'
correlation_table = np.load(filename)

# highly_correlated_tags = []

# n = len(tag_to_index_map)
# with tqdm(total=n*n/2-n) as pbar:
# 	for i1 in range(len(tag_to_index_map)):
# 		for i2 in range(i1+1, len(tag_to_index_map)):
# 			x = correlation_table[i1, i2]
# 			# if x < -0.07:
# 			# if x > 0.32:
# 			if x > 0.9:
# 				tag1 = index_to_tag_map[i1]
# 				tag2 = index_to_tag_map[i2]
# 				s = "{: .8f} - {} & {}".format(x, tag1, tag2)
# 				highly_correlated_tags.append(s)

# 			pbar.update(1)

# print("\n".join(sorted(highly_correlated_tags, reverse=True)))

# exit()





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

print("="*20)
should_keep_running = True
while should_keep_running:
	query_tag = input("enter a query tag (ex. coffee) ('q' to quit): ")
	query_tag = query_tag.replace(" ","_")

	if query_tag in ["quit", "exit", "q"]:
		should_keep_running = False
		continue

	correlation_results = get_correlations(query_tag)
	
	if len(correlation_results) == 0:
		continue

	# print the most and least correlated items
	# correlation_strings = ["{},{:.4f}".format(a,b) for a,b in correlation_results]
	correlation_strings = ["{: .4f},{}".format(b,a) for a,b in correlation_results]
	print("="*20)
	# print("QUERY: {}".format(query_tag))
	print("\n".join(correlation_strings[:10]))
	print("."*3)
	print("\n".join(correlation_strings[-5:]))
	print("="*20)

# # write the results to a file
# print("writing query results to file")
# with open("../../res/query_results.csv", 'w') as fp:
#     fp.write('\n'.join('"{}",{}'.format(tag,score) for tag,score in correlation_results))
