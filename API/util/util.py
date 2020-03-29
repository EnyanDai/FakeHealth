import csv
import errno
import os
import sys
from multiprocessing.pool import Pool

from tqdm import tqdm

from util.TwythonConnector import TwythonConnector


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def is_folder_exists(folder_name):
    return os.path.exists(folder_name)


def equal_chunks(list, chunk_size):
    """return successive n-sized chunks from l."""
    chunks = []
    for i in range(0, len(list), chunk_size):
        chunks.append(list[i:i + chunk_size])

    return chunks
