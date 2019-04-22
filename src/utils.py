#!/usr/bin/python3
import pickle
from tqdm import tqdm
import os.path

# enable tqdm-pandas integration
tqdm.pandas()


booru_domain, booru_name = "safebooru.org", "safebooru"


# say which booru is being used
print("Using {}".format(booru_name))


# return url to booru
def booru_url():
    return booru_domain


# modify abbreviated file path string to refer to full booru resource path
def booru_path(local_path):
    directory = "../../res/{}/".format(booru_name)

    if local_path.startswith('/'):
        print("booru_path error '{}' shouldn't start with a '/'".format(local_path))
        return booru_path(local_path[1:])
    return directory+local_path


# return string denoting subset of attributes used in csv format
def get_csv_header():
    return "id,created_at,rating,score,sample_url,sample_width,sample_height,preview_url,tags"


# http://stackoverflow.com/a/27518377/2230446
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


# http://stackoverflow.com/a/18603065/2230446
def get_last_line(filename):
    with open(filename, "rb") as f:
        f.seek(-2, 2)
        while f.read(1) != b"\n":
            f.seek(-2, 1)
        last = f.readline()
    return last


# save a pickle file
def save_obj(obj, name, print_debug_info=True):
    sanitized_name = name.replace('.pkl', '')
    if print_debug_info:
        print('Saving {}'.format(sanitized_name + '.pkl'))
    with open(sanitized_name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


# load a pickle file
def load_obj(name, print_debug_info=True):
    sanitized_name = name.replace('.pkl', '')
    if print_debug_info:
        print('Loading {}'.format(sanitized_name + '.pkl'))
    with open(sanitized_name + '.pkl', 'rb') as f:
        obj = pickle.load(f)
        return obj


def file_exists(filename):
    return os.path.isfile(filename)
