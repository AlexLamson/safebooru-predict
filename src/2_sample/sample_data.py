#!/usr/bin/python3
import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils import *

from tqdm import tqdm
import mmap
from bs4 import BeautifulSoup
from random import random

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


def sample_every_nth_line(source, dest, n):
	num_samples = 0
	num_lines = get_num_lines(source)
	with open(dest, "w+") as sample:
		with open(source) as population:
			for i, line in tqdm(enumerate(population), total=num_lines):
				if i % n == 0:
					# print(line)
					num_samples += 1
					sample.write(line.strip())
					sample.write("\n")
	print("{} samples taken from a population of {} ({:.2f}%)".format(num_samples, num_lines, 100.0*num_samples/num_lines))


def sample_all_non_zero_scores(source, dest):
	num_samples = 0
	num_lines = get_num_lines(source)
	with open(dest, "w+") as sample:
		with open(source) as population:
			for i, line in tqdm(enumerate(population), total=num_lines):
				soup = BeautifulSoup(line, "lxml")
				post = soup.find("post")
				if post is not None:
					score = int(post["score"])

					# sample ~20,000 with score 0 and ~20,000 with score 1, and sample all of the images with scores >1 or <0
					if (score < 0 or score > 1) or (score == 0 and random() < 20000/1374164) or (score == 1 and random() < 20000/369619):
						# print(line)
						num_samples += 1
						sample.write(line.strip())
						sample.write("\n")
	print("{} samples taken from a population of {} ({:.2f}%)".format(num_samples, num_lines, 100.0*num_samples/num_lines))


def main():
	# source = booru_path("data/head_safebooru.xml")
	source = booru_path("data/safebooru.xml")
	# sample_every_nth_line(source, dest=booru_path("data/sample_safebooru.xml"), n=100)
	sample_all_non_zero_scores(source, dest=booru_path("data/sample_safebooru.xml"))

if __name__ == "__main__":
	main()

