#!/usr/bin/python3


# prepend the given string with the path to the data files
def booru_path(s):
	if s.startswith('/'):
		print("booru_path error '{}' shouldn't start with a '/'".format(s))
		return "../../res/safebooru{}".format(s)
	return "../../res/safebooru/{}".format(s)


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
