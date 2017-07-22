#!/usr/bin/python3
import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils import get_num_lines

import numpy as np
import pandas as pd
from scipy.sparse import lil_matrix
import time
from tqdm import tqdm
from math import sqrt



'''
load the and_table into memory
load the tags file into memory
	should be able to map between index, tag string and frequency

initialize a correlation_table

for all non-reflexive tag pairs
	get the variables needed to compute the alex_phi_coefficient
	compute the alex_phi_coefficient
	add alex_phi_coefficient to the correlation_table

write the correlation_table to a file
'''

# this number was determined in the "correlate_make_and_table.py" file
num_tags_to_keep = 10000
# num_tags_to_keep = 100


# open the tags file to get a list of most frequent tags
print("reading tags file")
tags_file = "../../res/safebooru/tags.csv"
tag_counts = pd.read_csv(tags_file, nrows=num_tags_to_keep, header=0, names=['occurrences', 'tag'])


# make a map from locations in the array to tags
print("creating index->tag map")
index_to_tag_map = dict()
for index, row in tag_counts.iterrows():
	tag = row['tag']
	index_to_tag_map[index] = tag

# make a map from tag name to number of times tag has occurred
print("creating tag->freq map")
tag_to_freq_map = dict()
for index, row in tag_counts.iterrows():
	freq = row['occurrences']
	tag = row['tag']
	tag_to_freq_map[tag] = freq


# load the and_table into memory
print("loading and_table into memory")
filename = '../../res/safebooru/and_table.npy'
and_table = np.load(filename)

print("counting total number of images")
total_num_images = get_num_lines("../../res/safebooru/data/safebooru.csv")-1


# initialize the table to store the feature-feature correlation scores
print("initializing correlation_table")
correlation_table = np.zeros(shape=(num_tags_to_keep, num_tags_to_keep), dtype=np.float32)


# iterate over the half of the and_table
number_of_updates = (num_tags_to_keep-1)*((num_tags_to_keep-1)+1)/2 #nth triangular number
with tqdm(total=number_of_updates) as pbar:
	for i1 in range(num_tags_to_keep):
		for i2 in range(i1+1, num_tags_to_keep):
			
			tag1 = index_to_tag_map[i1]
			tag2 = index_to_tag_map[i2]

			# a = int(and_table[i1, i2])
			# c = int(tag_to_freq_map[tag2])
			# b = c-a
			# g = int(tag_to_freq_map[tag1])
			# d = g-a
			# e = 3000000
			# # e = a # "The Alex assumption"
			# f = d+e
			# h = b+e
			# i = total_num_images

			a = int(and_table[i1, i2])
			c = int(tag_to_freq_map[tag2])
			g = int(tag_to_freq_map[tag1])
			i = total_num_images

			# print("tag1: {}".format(tag1))
			# print("tag2: {}".format(tag2))

			# print(" X &  Y: {}".format(a))
			# print("!X &  Y: {}".format(b))
			# print("      Y: {}".format(c))
			# print(" X & !Y: {}".format(d))
			# print(" X     : {}".format(g))

			# phi_coefficient = (a*e-b*d)/sqrt( c*f*h*g )
			phi_coefficient = (i*a-c*g)/sqrt( c*g*(i-c)*(i-g) )


			alex_phi_coefficient = phi_coefficient
			# alex_phi_coefficient = ((a*a)-(b*d)) / sqrt( (a+b)*(c+a)*(a+c)*(b+a) )

			correlation_table[i1, i2] = alex_phi_coefficient
			pbar.update(1)


# save the correlation table to a file
filename = '../../res/safebooru/correlation_table.npy'
print("saving correlation table to {}".format(filename))
np.save(filename, correlation_table)

