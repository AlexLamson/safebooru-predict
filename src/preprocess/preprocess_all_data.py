#!/usr/bin/python3
import sys
sys.path.append('..')
from utils import *

import time
import pandas as pd
from tqdm import tqdm

from duplicate_checker import DuplicateChecker
from sampler import Sampler
from statistics_recorder import StatisticsRecorder


'''
Note:
All three - 20 minutes
Just the sampler - 5 minutes
'''


def main():
    # TODO merge deduper and stats flags into one flag, they rely on each other
    run_deduplicator = True
    run_statistics_recorder = True
    run_sampler = True

    print("Starting preprocessor")
    print("  Deduplicator: {}".format(run_deduplicator))
    print("  Statistics: {}".format(run_statistics_recorder))
    print("  Sampler: {}".format(run_sampler))

    # load the csv in to RAM
    print("loading csv into RAM (should take about 30 seconds)")
    start = time.time()
    # df = pd.read_csv(booru_path("data/all_data.csv"), header=0, names=get_csv_header().split(","), nrows=10)
    df = pd.read_csv(booru_path("data/all_data.csv"), header=0, names=get_csv_header().split(","), encoding="utf-8")
    end = time.time()
    print("It took {:.2f} seconds for pd.read_csv to complete".format(end - start))

    # deduper needs to be enabled if the stats recorder is running
    if run_statistics_recorder:
        run_deduplicator = True

    # initialize the row processors
    if run_deduplicator:
        max_id = df["id"].max()
        duplicate_checker = DuplicateChecker(total_images=max_id+1)
    if run_statistics_recorder:
        statistics_recorder = StatisticsRecorder()

    # process all the rows
    if run_deduplicator or run_statistics_recorder:
        for index, row in tqdm(df.iterrows(), total=df.shape[0], ascii=True):
            if run_deduplicator:
                is_dupe = duplicate_checker.process_row(row, index)
            if run_statistics_recorder:
                statistics_recorder.process_row(row, is_dupe)
        if run_deduplicator:
            duplicate_checker.write_results()
        if run_statistics_recorder:
            statistics_recorder.write_results()

    # write deduped data to file
    if run_deduplicator:
        print("Running deduper. Will finish at {} iterations. ETA 5 minutes to process and save".format(df.shape[0]))
        deduped_df = df[df.progress_apply(func=lambda row: not duplicate_checker.all_duplicates[row["id"]], axis=1)]

        print("Saving deduped data to csv")
        deduped_df.to_csv(booru_path("data/deduped_data.csv"), header=get_csv_header(), encoding='utf-8')

    # select samples
    if run_sampler:
        print("Running sampler. Will finish at {} iterations".format(df.shape[0]))
        sampler = Sampler()
        sampled_df = df[df.progress_apply(func=lambda x: sampler.process_row(x), axis=1)]

        print("Saving sampled data to csv")
        sampled_df.to_csv(booru_path("data/sample_data.csv"), header=get_csv_header(), encoding='utf-8')


if __name__ == "__main__":
    main()
