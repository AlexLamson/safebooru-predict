#!/usr/bin/python3
import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils import get_num_lines

from tqdm import tqdm
from bs4 import BeautifulSoup
import time
import datetime

# #http://stackoverflow.com/a/27518377/2230446
# def get_num_lines(filename):
# 	f = open(filename, "rb")
# 	num_lines = 0
# 	buf_size = 1024 * 1024
# 	read_f = f.raw.read

# 	buf = read_f(buf_size)
# 	while buf:
# 		num_lines += buf.count(b"\n")
# 		buf = read_f(buf_size)

# 	return num_lines

# source = "../../res/safebooru/data/head_safebooru.xml"
# dest = "../../res/safebooru/data/head_safebooru.csv"
source = "../../res/safebooru/data/safebooru.xml"
dest = "../../res/safebooru/data/safebooru.csv"

num_lines = get_num_lines(source)
with open(dest, "w") as csv:
	# header = "id,created_at,rating,score,sample_url,sample_width,sample_height,preview_url,preview_width,preview_height,tags"
	header = "id,created_at,rating,score,sample_url,sample_width,sample_height,preview_url,tags"
	csv.write(header)
	csv.write("\n")

	with open(source) as xml:
		for i, line in tqdm(enumerate(xml), total=num_lines):
			soup = BeautifulSoup(line, "lxml")
			post = soup.find("post")
			if post is not None:

				# post_id = post["id"]
				# rating = post["rating"]
				# score = post["score"]
				# md5 = post["md5"]
				# created_at = post["created_at"]
				# file_url = post["file_url"]
				# width = post["width"]
				# height = post["height"]
				# sample_url = post["sample_url"]
				# sample_width = post["sample_width"]
				# sample_height = post["sample_height"]
				# preview_url = post["preview_url"]
				# preview_width = post["preview_width"]
				# preview_height = post["preview_height"]
				# has_children = post["has_children"]
				# has_comments = post["has_comments"]
				# has_notes = post["has_notes"]
				# change = post["change"]
				# creator_id = post["creator_id"]
				# parent_id = post["parent_id"]
				# source = '"'+post["source"].replace('"','""')+'"'
				# status = post["status"]
				# tags = '"'+post["tags"].replace('"','""')+'"'

				# attributes = [post_id,rating,score,md5,created_at,file_url,width,height,preview_url,preview_width,preview_height,sample_url,sample_width,sample_height,has_children,has_comments,has_notes,change,creator_id,parent_id,source,status,tags]

				status = post["status"]
				if status != "active":
					continue

				post_id = post["id"]

				created_at = str(int( time.mktime(datetime.datetime.strptime(post["created_at"], "%a %b %d %H:%M:%S %z %Y").timetuple()) ))

				rating = post["rating"]
				score = post["score"]

				sample_url = post["sample_url"]
				sample_width = post["sample_width"]
				sample_height = post["sample_height"]

				preview_url = post["preview_url"]
				preview_width = post["preview_width"]
				preview_height = post["preview_height"]

				tags = '"'+post["tags"].strip().replace('"','""')+'"'

				attributes = [post_id,created_at,rating,score,sample_url,sample_width,sample_height,preview_url,preview_width,preview_height,tags]
				# attributes = [post_id,created_at,rating,score,sample_width,sample_height,preview_url,tags]


				csv.write(",".join(attributes))

				csv.write("\n")
