#!/usr/bin/python3


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


def csv_line_to_map(line):
	pass

def tags_to_vector(tags):
	pass

