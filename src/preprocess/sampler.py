#!/usr/bin/python3
import sys
sys.path.append('..')
from utils import *

from random import random


class Sampler:
    def __init__(self):
        self.debug = False
        self.min_tags = 16
        self.goal_samples_per_score = 20000

        self.all_stats = load_obj(booru_path("pickle_files/statistics"))
        self.all_duplicates = load_obj(booru_path("pickle_files/duplicates"))

    def process_row(self, row):
        # don't sample duplicates
        is_dupe = self.all_duplicates[row["id"]]
        if is_dupe:
            if self.debug:
                print("rejecting duplicate")
            return False

        # don't sample images with only a few tags
        if len(row["tags"]) < self.min_tags:
            if self.debug:
                print("Reject: {} is not enough tags (min: {})".format(len(row["tags"]), self.min_tags))
            return False

        # definitely sample images with uncommon scores (very high or very low)
        score = row["score"]
        if self.all_stats["times_score_occurred"][score] < self.goal_samples_per_score:
            if self.debug:
                print("Accept: score of {} happens infrequently".format(row["score"]))
            return True

        # use stratified sampling across rest of scores
        if (score == 0 and random() < self.goal_samples_per_score/self.all_stats["times_score_occurred"][score]):
            if self.debug:
                print("Accept: using stratified sampling on score of {}".format(row["score"]))
            return True

        return False
