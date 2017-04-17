#!/usr/bin/python3
from bs4 import BeautifulSoup
from tqdm import tqdm
import numpy as np
import pickle


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


def load_tag_index_map(filename):
	print("loading tag index map")
	tag_index_map = pickle.load(open(filename, "rb"))
	return tag_index_map


# map list of tags to boolean vector
def vectorize(tags, tag_index_map):
	vector = np.zeros(len(tag_index_map))
	for tag in tags:
		if tag in tag_index_map.keys():
			index = tag_index_map[tag]
			vector[index] = True
	return vector


# convert a single line of the xml file to an input vector and output value
def line_to_x_y(line, tag_index_map):
	soup = BeautifulSoup(line, "lxml")
	post = soup.find("post")
	if post is not None:
		tags = post["tags"].strip().split(" ")
		# print(tags)

		x = vectorize(tags, tag_index_map)
		y = score = int(post["score"])
		return x, y

	print("~~~ERROR~~~")
	print("line:", line)
	print("~~~ERROR~~~")


# convert entire xml file into list of input vectors and list of output values
def file_to_xs_ys(filename, tag_index_map):
	num_lines = get_num_lines(filename)
	num_dimensions = len(tag_index_map)

	xs = np.zeros((num_lines, num_dimensions), dtype=bool)
	ys = np.zeros((num_lines,1))

	with open(filename, "r") as f:
		for i, line in tqdm(enumerate(f), total=num_lines):
			x, y = line_to_x_y(line, tag_index_map)
			xs[i] = x
			ys[i] = y

	return xs, ys


def main():
	tag_index_map = load_tag_index_map("../../res/tag_index_map.p")
	# print(tag_index_map)

	filename = "../../res/head_safebooru.xml"
	# filename = "../../res/sample_safebooru.xml"
	xs, ys = file_to_xs_ys(filename, tag_index_map)

	print(xs[0], ys[0])
	print(xs[1], ys[1])

if __name__ == "__main__":
	main()