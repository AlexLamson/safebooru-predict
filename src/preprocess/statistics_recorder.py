#!/usr/bin/python3
import sys
sys.path.append('..')
from utils import *

from collections import defaultdict
import numpy as np


class StatisticsRecorder:
    def __init__(self):
        self.total_images = 0

        self.total_tags = 0
        self.all_unique_tags = set()
        self.times_tag_occurred = defaultdict(int)
        self.number_of_images_with_this_many_tags = defaultdict(int)
        self.all_scores_for_tag = dict()

        self.times_tag_was_safe = defaultdict(int)
        self.times_tag_was_questionable = defaultdict(int)
        self.times_tag_was_explicit = defaultdict(int)

        self.number_of_safe_images = 0
        self.number_of_questionable_images = 0
        self.number_of_explicit_images = 0

        self.all_scores = []
        self.times_score_occurred = defaultdict(int)

        self.number_of_duplicates = 0

    def process_row(self, row, is_dupe):
        # initialize variables
        tags = row["tags"].split()
        score = row["score"]

        is_s = row["rating"] == 's'
        is_q = row["rating"] == 'q'
        is_e = row["rating"] == 'e'

        # record counts
        self.total_images += 1
        self.total_tags = self.total_tags + len(tags)
        self.all_unique_tags.update(tags)
        for tag in tags:
            self.times_tag_occurred[tag] += 1
        self.number_of_images_with_this_many_tags[len(tags)] += 1
        for tag in tags:
            if tag in self.all_scores_for_tag:
                # self.all_scores_for_tag[tag] = np.append(self.all_scores_for_tag[tag], score)
                if score in self.all_scores_for_tag[tag]:
                    self.all_scores_for_tag[tag][score] += 1
                else:
                    self.all_scores_for_tag[tag][score] = 1
            else:
                # self.all_scores_for_tag[tag] = np.array([score], dtype='i2')
                self.all_scores_for_tag[tag] = dict()
                self.all_scores_for_tag[tag][score] = 1

        # record rating information
        if is_s:
            self.number_of_safe_images += 1
            for tag in tags:
                self.times_tag_was_safe[tag] += 1
        elif is_q:
            self.number_of_questionable_images += 1
            for tag in tags:
                self.times_tag_was_questionable[tag] += 1
        elif is_e:
            self.number_of_explicit_images += 1
            for tag in tags:
                self.times_tag_was_explicit[tag] += 1

        # record score information
        # self.all_scores.append(score)
        self.times_score_occurred[score] += 1

        # record duplicates information
        if is_dupe:
            self.number_of_duplicates += 1

    def write_results(self):
        # reconstruct the raw score counts from the score frequencies
        val, freq = np.array(list(self.times_score_occurred.items())).T
        self.all_scores = np.repeat(val, freq)

        score_average = np.mean(self.all_scores)
        score_std_dev = np.std(self.all_scores)

        all_stats = {
            "total_images": self.total_images,

            "total_tags": self.total_tags,
            "all_unique_tags": self.all_unique_tags,
            "times_tag_occurred": self.times_tag_occurred,
            "number_of_images_with_this_many_tags": self.number_of_images_with_this_many_tags,
            "all_scores_for_tag": self.all_scores_for_tag,

            "times_tag_was_safe": self.times_tag_was_safe,
            "times_tag_was_questionable": self.times_tag_was_questionable,
            "times_tag_was_explicit": self.times_tag_was_explicit,

            "number_of_safe_images": self.number_of_safe_images,
            "number_of_questionable_images": self.number_of_questionable_images,
            "number_of_explicit_images": self.number_of_explicit_images,

            "score_average": score_average,
            "score_std_dev": score_std_dev,
            "times_score_occurred": self.times_score_occurred,

            "number_of_duplicates": self.number_of_duplicates
        }

        save_obj(all_stats, booru_path("pickle_files/statistics"))
