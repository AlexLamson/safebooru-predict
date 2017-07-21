from bs4 import BeautifulSoup
import time, datetime
import numpy as np
import pickle
from collections import defaultdict
from tqdm import tqdm
import matplotlib.pyplot as plt


#http://stackoverflow.com/a/27518377/2230446
def get_num_lines(filename):
    f = open(filename, "rb")
    num_lines = 0
    buf_size = 1024 * 1024
    read_f = f.raw.read

    buf = read_f(buf_size)
    while buf:
        num_lines += buf.count(b"\n")
        buf = read_f(buf_size)

    return num_lines

# score_counts is a dictionary with the keys being scores and the values being the number of times that score has been seen
def get_score_counts(filename):
	score_counts = defaultdict(int)

	with open(filename, "r") as f:
		for line in tqdm(f, total=get_num_lines(filename)):
			soup = BeautifulSoup(line, "lxml")
			post = soup.find("post")
			if post is not None:
				score = int(post["score"])
				score_counts[score] += 1

	return score_counts


def write_score_counts(score_counts, filename="../../res/safebooru/scores.csv"):
	scores_file = open(filename,"w")
	scores_file.write("score,occurrences\n")

	# sorted by score
	score_range = range(min(score_counts), max(score_counts)+1)
	for score in score_range:
		num_occurrences = score_counts[score]
		scores_file.write("{: >3},{}\n".format(score, num_occurrences))

	scores_file.close()


def graph_score_counts(score_counts):
	score_range = range(min(score_counts), max(score_counts)+1)
	occurrences = [score_counts[score] for score in score_range]

	plt.clf()
	plt.bar(left=score_range, height=occurrences)
	plt.title("Score frequencies of {} safebooru images".format(sum(occurrences)+1))
	plt.xlabel("Score")
	plt.ylabel("Number of Occurrences")
	plt.savefig("../../figures/Score frequencies.png")
	# plt.show()

	plt.clf()
	plt.bar(left=score_range, height=occurrences, log=True)
	plt.title("Score frequencies of {} safebooru images (log scale)".format(sum(occurrences)+1))
	plt.xlabel("Score")
	plt.ylabel("Number of Occurrences")
	plt.savefig("../../figures/Score frequencies (log scale).png")
	plt.show()


def main():
	# filename = "../../res/safebooru/data/head_safebooru.xml"
	filename = "../../res/safebooru/data/safebooru.xml"
	score_counts = get_score_counts(filename)
	write_score_counts(score_counts, filename="../../res/safebooru/scores.csv")
	graph_score_counts(score_counts)

if __name__ == "__main__":
	main()

