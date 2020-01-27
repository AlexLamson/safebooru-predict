#!/usr/bin/python3
import sys
sys.path.append('..')
from utils import *

from math import sqrt
import random


show_first_n = 19  # show the first n tags



all_stats = load_obj(booru_path("pickle_files/statistics"))
tag_to_index = load_obj(booru_path("pickle_files/tag_to_index"))
index_to_tag = load_obj(booru_path("pickle_files/index_to_tag"))
tag_intersection_counts = load_obj(booru_path("pickle_files/tag_intersection_counts"))


common_tag = max(tag_to_index.keys(), key=lambda x: all_stats["times_tag_occurred"][x])
print("Total tags {}".format(len(tag_to_index)))
print("Most common tag: '{}'".format(common_tag))

def get_correlations(query_tag):
    correlation_results = []
    subset_results = []
    superset_results = []

    # check that the tag is one that has correlations calculated
    if query_tag not in tag_to_index:
        print("ERROR '{}' not in the {} available tags".format(query_tag, len(tag_to_index)))
        return [], [], []

    query_tagid = tag_to_index[query_tag]

    for tagid1, tagid2 in tag_intersection_counts:
        if query_tagid == tagid1:
            nonquery_tagid = tagid2
        elif query_tagid == tagid2:
            nonquery_tagid = tagid1
        else:
            continue

        nonquery_tag = index_to_tag[nonquery_tagid]

        percent_intersection = tag_intersection_counts[(tagid1, tagid2)] / all_stats["times_tag_occurred"][query_tag]
        # if percent_intersection <= 0.01:
        #     continue

        # compute the phi coefficient
        a = tag_intersection_counts[(tagid1, tagid2)]
        b = all_stats["times_tag_occurred"][query_tag]
        c = all_stats["times_tag_occurred"][nonquery_tag]
        d = all_stats["total_images"]
        phi_coefficient = (d*a-b*c)/sqrt( b*c*(d-b)*(d-c) )
        correlation_results.append( (phi_coefficient, a, nonquery_tag) )

        # if this is high, nonquery is a subset of query
        p_query_given_nonquery = a / c
        subset_results.append( (p_query_given_nonquery, a, nonquery_tag) )

        # if this is high, nonquery is a superset of query
        p_nonquery_given_query = a / b
        superset_results.append( (p_nonquery_given_query, a, nonquery_tag) )

    # sort the results by their correlation in descending order
    correlation_results = sorted(correlation_results, reverse=True)
    subset_results = sorted(subset_results, reverse=True)
    superset_results = sorted(superset_results, reverse=True)

    return correlation_results, subset_results, superset_results




correlation_strings = []
all_strings = []
print("="*20)
should_keep_running = True
while should_keep_running:
    # receive the user input
    query_tag = input("enter a query tag (ex. coffee) or 'quit' or 'tofile': ")

    if query_tag == '':
        continue

    # quit the program
    if query_tag in ["quit", "exit", "q"]:
        should_keep_running = False
        continue

    # write previous results to a file
    if query_tag == "tofile":
        # write the results to a file
        print("writing query results to file")
        with open(booru_path("query_results.csv"), 'w') as fp:
            fp.write("|{:-^40}|{:-^40}|{:-^40}|\n".format("CORRELATED (PHI)", "SUBSETS", "SUPERSETS"))
            fp.write("\n".join(all_strings))
        continue

    # use a space at the start or end like a wildcard to find tags
    if query_tag == " "*len(query_tag):
        query_tag = random.choice([x for x in tag_to_index.keys() if all_stats["times_tag_occurred"][x] >= 10])
        print("tag: "+query_tag)
    elif query_tag.startswith(" ") or query_tag.endswith(" "):
        query_starts_with_space = query_tag.startswith(" ")
        query_ends_with_space = query_tag.endswith(" ")
        trimmed_query = query_tag.strip()

        def is_match(tag):
            if query_starts_with_space and tag.endswith(trimmed_query):
                return True
            elif query_ends_with_space and tag.startswith(trimmed_query):
                return True
            else:
                return False

        possible_tags = filter(is_match, tag_to_index)
        possible_tags = sorted(possible_tags, key=lambda x: all_stats["times_tag_occurred"][x], reverse=False)

        if len(possible_tags) == 0:
            print("Couldn't find any matches for {}".format(query_tag.strip()))
        elif len(possible_tags) == 1:
            query_tag = possible_tags[0]
        else:
            print("Matches:")
            print("="*20)
            print("\n".join(possible_tags))
            continue

    correlation_results, subset_results, superset_results = get_correlations(query_tag)

    if len(correlation_results) == 0:
        continue


    correlation_strings = ["{: .4f} {: >6} {: <25}".format(a,b,c[:25]) for a,b,c in correlation_results]
    subset_strings = ["{: .4f} {: >6} {: <25}".format(a,b,c[:25]) for a,b,c in subset_results]
    superset_strings = ["{: .4f} {: >6} {: <25}".format(a,b,c[:25]) for a,b,c in superset_results]
    all_strings = ["{} {} {}".format(a,b,c) for a,b,c in zip(correlation_strings, subset_strings, superset_strings)]
    print("="*20)
    print("|{:-^40}|{:-^40}|{:-^40}|".format("CORRELATED (PHI)", "SUBSETS", "SUPERSETS"))
    print("\n".join(all_strings[:show_first_n]))
    print("="*20)
