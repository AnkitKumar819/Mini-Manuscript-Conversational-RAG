# src/utils.py

import os
import re


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_page_number(filename):
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())
    return 0
