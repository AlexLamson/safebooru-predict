#!/usr/bin/python3
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import datetime
import re
import urllib
import sys
from tqdm import tqdm
import os


# download the results of a single API call
def make_query(query, site="safebooru.org", images_per_page=10, page_id=0):
	tags = query.split(" ")
	html_doc = urlopen("http://{}/index.php?page=dapi&s=post&q=index&pid={}&tags=sort%3aid%3aasc+{}&limit={}".format(site, page_id, "+".join(tags), images_per_page))
	html_doc = html_doc.read()
	return html_doc


# get the number of images that match the query
def get_number_of_matches(query, site="safebooru.org"):
	html_doc = make_query(query, site=site, images_per_page=0)
	soup = BeautifulSoup(html_doc, "lxml")
	posts = soup.find("posts")
	if posts is not None:
		total_images = int(posts.get("count"))
		return total_images
	else:
		return -1


# download all the image metadata for a given query
def download_info(query, filemode="w", filename="query_results.xml", site="safebooru.org", limit=-1, images_per_page=40):
	with open(filename, filemode) as results_file:
		if limit == -1:
			limit = get_number_of_matches(query, site)

		page_id = 0
		images_downloaded = images_per_page*page_id#0

		with tqdm(total=limit) as pbar:

			while images_downloaded < limit:

				html_doc = make_query(query, site=site, images_per_page=images_per_page, page_id=page_id)

				soup = BeautifulSoup(html_doc, "lxml")

				every_post = soup.findAll("post")
				# print(every_post)
				for post in every_post:
					# print(post)
					results_file.write(str(post))
					results_file.write("\n")

				images_downloaded += len(every_post)
				page_id += 1
				pbar.update(len(every_post))

				# don't bombard the server
				time.sleep(0.5)

# download all the image metadata from a booru
def download_booru(filename, site="safebooru.org"):

	#http://stackoverflow.com/a/18603065/2230446
	def get_last_line_of_file(filename):
		with open(filename, "rb") as f:
			f.seek(-2, 2)
			while f.read(1) != b"\n":
				f.seek(-2, 1)
			last = f.readline()
		return last

	filemode = "w"
	query = "*"

	if os.path.isfile(filename):
		print("File already exists. Appending query results to file")

		last_line = get_last_line_of_file("safebooru.xml")
		soup = BeautifulSoup(last_line, "xml")
		last_id = soup.findAll()[0]["id"]

		filemode = "a"
		query = "id:>{}".format(last_id)

	download_info(query=query, filemode=filemode, filename=filename, site="safebooru.org", images_per_page=900)


def main():
	download_booru("../../res/safebooru.xml")

if __name__ == "__main__":
	main()

