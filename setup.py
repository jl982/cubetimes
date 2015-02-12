#!/usr/bin/env python

import os, sys
import time
import re

time_keyword = "for "
time_keyword_len = len(time_keyword)
time_len = 28
timezone_start = 20
timezone_end = 24

dir_name = sys.argv[1]
filenames = os.listdir(dir_name)
filenames.sort(key=lambda filename: os.lstat(os.path.join(dir_name, filename)).st_mtime)
for filename in filenames:
    path = os.path.join(dir_name, filename)
    f = open(path, 'r')

    # Construct time
    first_line = f.readline()
    offset = first_line.find(time_keyword) + time_keyword_len
    time_str = first_line[offset:offset+time_len]
    time_str_stripped = time_str[:timezone_start] + time_str[timezone_end:]
    time_parsed = time.strptime(time_str_stripped, "%a %b %d %H:%M:%S %Y")
    record_datetime = time.strftime("%Y-%m-%d %H:%M:%S", time_parsed)

    # Cube type
    record_cube = ""
    match = re.search(" ([A-Z0-9]+)-[0-9]", filename)
    if match:
        record_cube = match.group(1)

    # Average
    record_average = ""
    while True:
        line = f.readline()
        match = re.search("Average: ([0-9.]+)", line)
        if match:
            record_average = match.group(1)
            break

    # Standard deviation
    record_std = ""
    while True:
        line = f.readline()
        match = re.search("Standard Deviation: ([0-9.]+)", line)
        if match:
            record_std = match.group(1)
            break

    # Num solves
    while True:
        line = f.readline()
        if (line.find("Individual Times:") >= 0):
            break
    record_num_solves = 0;
    while True:
        line = f.readline()
        if not line:
            break
        record_num_solves += 1
    

    f.close()
    print ",".join([record_datetime, record_cube, str(record_num_solves), record_average, record_std])

