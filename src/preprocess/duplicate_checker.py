#!/usr/bin/python3
import sys
sys.path.append('..')
from utils import *

# from bitarray import bitarray
import numpy as np


class DuplicateChecker:
    def __init__(self, total_images):
        self.previous_tags = set("this_tag_will_never_occur")
        # self.all_duplicates = bitarray(total_images)
        self.all_duplicates = np.full(total_images, False)
        print("initializing all_duplicates array with size {}".format(total_images))

    def process_row(self, row, index):
        # extract the set of tags from the row
        tags = set(row["tags"].split())

        # use Jaccard similarity to find duplicates
        intersection_size = len(tags.intersection(self.previous_tags))
        union_size = len(tags.union(self.previous_tags))
        similarity_with_last_image = 1.0 * intersection_size / union_size

        # hold on to the tag to check the next image
        self.previous_tags = tags

        # if the tags are very similar to the previous image's tags, consider that a duplicate image
        if len(tags) >= 8 and similarity_with_last_image >= 0.8:
            self.all_duplicates[row["id"]] = True
            return True
        else:
            self.all_duplicates[row["id"]] = False
            return False

    def write_results(self):
        save_obj(self.all_duplicates, booru_path("pickle_files/duplicates"))
