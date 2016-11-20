#!/usr/bin/python3
from tqdm import tqdm
import mmap


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


def main():
	# source = "../../res/head_safebooru.xml"
	source = "../../res/safebooru.xml"
	sample_every_nth_line(source, dest="../../res/sample_safebooru.xml", n=100)

if __name__ == "__main__":
	main()

