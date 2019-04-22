#!/usr/bin/python3
import sys
sys.path.append('..')
from utils import *

from tqdm import tqdm
from bs4 import BeautifulSoup
import time
from datetime import datetime

'''
Note:
It takes about 10 minutes to process 1 million lines
'''

'''
| Column name   | Type   | Description                              |
| -------------:|:------ | ---------------------------------------- |
| id            | int    | unique id for each image                 |
| created_at    | int    | time in seconds since epoch              |
| rating        | char   | 's' safe, 'q' questionable, 'e' explicit |
| score         | int    | net upvote / downvote score for image    |
| sample_url    | string | url for medium-size version of image     |
| sample_width  | int    | width of medium-size version of image    |
| sample_height | int    | height of medium-size version of image   |
| preview_url   | string | url for thumbnail version of image       |
| tags          | string | space-separated list of tags             |
'''


def xml_line_to_dict(xml):

    # print(xml)

    if not xml.has_attr("created_at"):
        print(" missing 'created_at' attribute - id:", xml["id"])
        # change this later to record the broken data's id to a file

        with open(booru_path("corrupted_image_ids.txt"), "a", encoding="utf-8") as error_file:
            error_file.write(xml["id"]+" missing created_at"+"\n")

        return {"status":"inactive"}

    if not xml.has_attr("width"):
        print(" missing 'width' attribute - id:", xml["id"])
        # change this later to record the broken data's id to a file

        with open(booru_path("corrupted_image_ids.txt"), "a", encoding="utf-8") as error_file:
            error_file.write(xml["id"]+" missing width"+"\n")

        return {"status":"inactive"}

    def parse_url(url):
        return '"'+url.replace('"','""')+'"'

    d = dict()
    d["id"] = int(xml["id"])
    d["rating"] = xml["rating"]
    d["score"] = int(xml["score"])
    d["md5"] = xml["md5"]

    created_datetime = datetime.strptime(xml["created_at"], "%a %b %d %H:%M:%S %z %Y")
    if created_datetime.year == 1969:
        print("id has created_by in 1969:", xml["id"])
        with open(booru_path("corrupted_image_ids.txt"), "a", encoding="utf-8") as error_file:
            error_file.write(xml["id"]+" created_by in 1969"+"\n")
        d["created_at"] = 0
    else:
        d["created_at"] = int(time.mktime(created_datetime.timetuple()))

    d["file_url"] = parse_url(xml["file_url"])
    d["width"] = int(xml["width"])
    d["height"] = int(xml["height"])
    d["sample_url"] = parse_url(xml["sample_url"])
    d["sample_width"] = int(xml["sample_width"])
    d["sample_height"] = int(xml["sample_height"])
    d["preview_url"] = parse_url(xml["preview_url"])
    d["preview_width"] = int(xml["preview_width"])
    d["preview_height"] = int(xml["preview_height"])
    d["has_children"] = 1 if xml["has_children"] == 'true' else 0
    d["has_comments"] = 1 if xml["has_comments"] == 'true' else 0
    d["has_notes"] = 1 if xml["has_notes"] == 'true' else 0
    d["change"] = int(xml["change"])
    d["creator_id"] = xml["creator_id"]
    d["parent_id"] = xml["parent_id"]
    d["source"] = parse_url(xml["source"])
    d["status"] = xml["status"]
    d["tags"] = '"'+xml["tags"].strip().replace('"','""')+'"'

    return d


def dict_and_header_to_csv_line(image_info_dict, header):
    csv_line = ",".join([str(image_info_dict[attribute]) for attribute in header.split(",")])
    csv_line += "\n"
    return csv_line


def convert_file(src, dest):
    # clear out the old error log
    with open(booru_path("corrupted_image_ids.txt"), "w", encoding="utf-8") as error_file:
        error_file.write("")

    header = get_csv_header()

    # get the total number of lines so a progress bar can be shown
    print("counting lines in source xml file to prepare loading bar (~30 seconds)")
    # num_lines = 3820569
    num_lines = get_num_lines(src)

    with open(dest, "w", encoding="utf-8") as csv:
        csv.write(header)
        csv.write("\n")

        with open(src, encoding="utf-8") as xml:
            for i, line in tqdm(enumerate(xml), total=num_lines):

                soup = BeautifulSoup(line, "lxml")
                post = soup.find("post")
                if post is not None:
                    image_info_dict = xml_line_to_dict(post)

                    # if the image was deleted, don't include it in the csv
                    if "status" not in image_info_dict.keys():
                        print("failed with", image_info_dict)
                        exit()
                    if image_info_dict["status"] != "active":
                        continue

                    csv_line = dict_and_header_to_csv_line(image_info_dict, header)
                    csv.write(csv_line)


def main():
    convert_file(src=booru_path("data/all_data.xml"), dest=booru_path("data/all_data.csv"))


if __name__ == "__main__":
    main()
