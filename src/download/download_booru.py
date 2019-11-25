#!/usr/bin/python3
import sys
sys.path.append('..')
from utils import *

import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
from tqdm import tqdm
from socket import timeout
from urllib.error import HTTPError
from urllib.error import URLError
from ssl import SSLWantReadError


'''
Note:
I was getting 134 image/sec on average, which is about 2 hours for 1 million images.
'''

max_images_per_page = 900  # don't set higher than 900 due to server limits
seconds_between_batches = 10.0  # seconds to wait until making another query (to give the server a rest)
default_timeout_seconds = 7.0  # amount of time in seconds until query is considered "timed out"
throttle_pause_seconds = 3*60  # seconds to wait when the server throttles the connection
throttle_limit_images = 20000  # 200000  # number of images that can be downloaded until server throttles (varies)
print_debug = True


# download the results of a single API call
def make_query(query, site, images_per_page=10, page_id=0):
    tags = query.split(" ")

    timeout_time = default_timeout_seconds
    while True:
        url = "http://{}/index.php?page=dapi&s=post&q=index&pid={}&tags=sort%3aid%3aasc+{}&limit={}".format(site, page_id, "+".join(tags), images_per_page)
        try:
            html_doc = urlopen(url, timeout=timeout_time)

            html_doc = html_doc.read()
            return html_doc
        except HTTPError as ex:
            if ex.code == 403:
                print("The booru is blocking mass downloads of this sort. Exiting.")
                sys.exit()
            else:
                print(ex)
                continue
        except (timeout, SSLWantReadError, URLError, OSError, TimeoutError) as ex:
            # increase the amount we'll wait for it to timeout
            delta = timeout_time * 0.2
            delta = max(delta, 1.0)
            timeout_time += delta
            timeout_time = min(timeout_time, 120.0)
            if print_debug:
                print("Connection failed with exception {}. Trying again with timeout of {} seconds".format(ex, int(timeout_time)))
            continue
        else:
            print(" Access successful.")


# get the number of images that match the query
# returns -1 if there was an error
def get_number_of_matches(query, site):
    html_doc = make_query(query, site=site, images_per_page=0)

    soup = BeautifulSoup(html_doc, "lxml")

    posts = soup.find("posts")
    if posts is not None:
        total_images = int(posts.get("count"))
        return total_images
    else:
        return -1


# download all the image metadata for a given query
def download_info(query, site, filename, filemode="w", limit=-1, images_per_page=40):
    try:
        with open(filename, filemode, encoding="utf-8") as results_file:
            if limit == -1:
                limit = get_number_of_matches(query, site)
                if limit == 0:
                    print("All images already downloaded - exiting")
                    sys.exit()

            page_id = 0
            images_downloaded = images_per_page*page_id

            with tqdm(total=limit) as pbar:

                while images_downloaded < limit:

                    # server throttles after 200K images
                    throttle_limit = int(throttle_limit_images/max_images_per_page)*max_images_per_page
                    if images_downloaded > 0 and images_downloaded % throttle_limit == 0:
                        if print_debug:
                            print("\npausing for {} seconds to avoid server timeout (throttle)".format(throttle_pause_seconds))
                        time.sleep(throttle_pause_seconds)

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
                    time.sleep(seconds_between_batches)
    except KeyboardInterrupt:
        print("User keyboard interrupt")
        sys.exit()


# download all the image metadata from a booru
# if the file already exists, it'll try to resume the download
def download_booru(filename, site):
    filemode = "w"
    query = "*"

    if os.path.isfile(filename) and get_num_lines(filename) > 0:
        last_line = get_last_line(filename)
        soup = BeautifulSoup(last_line, "xml")
        last_id = soup.findAll()[0]["id"]

        print("Resuming download from id {}".format(last_id))
        # print("File already exists. Appending query results to file")

        filemode = "a"
        query = "id:>{}".format(last_id)
    else:
        print("Starting download from id 1")

    download_info(query, site, filename, filemode, images_per_page=max_images_per_page)


if __name__ == "__main__":
    print("URL: {}".format(booru_url()))
    print("Batch size: {}".format(max_images_per_page))
    print("Seconds between batches: {}".format(seconds_between_batches))
    download_booru(booru_path("data/all_data.xml"), booru_url())
    print("Download complete")
    main()
