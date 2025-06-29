#! /usr/bin/env python3
# Write a Python script that processes a log file and outputs the count of each unique error code found in the file.
# Sample File
# 2025-06-17 12:00:01 INFO User logged in
# 2025-06-17 12:01:45 ERROR_404 Page not found
# 2025-06-17 12:02:03 ERROR_500 Internal server error
# 2025-06-17 12:03:20 ERROR_404 Resource missing
# 2025-06-17 12:05:00 INFO Scheduled job started
# 2025-06-17 12:06:11 ERROR_403 Unauthorized access attempt
# 2025-06-17 12:07:25 WARNING Low disk space
# 2025-06-17 12:08:45 ERROR_500 Database connection failed

import re
from collections import Counter
def parse_log_file(file_path):
    error_arr = []
    error_pattern = re.compile(r'ERROR_(\d{3})')
    try:
        with open(file_path, 'r') as f:
            for line in f:
                matched = error_pattern.findall(line)   # error_pattern.search(line)
                if matched:
                    error_arr.append(matched[0])
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return
    errCodeCount = Counter(error_arr) # {'404:'2'}
    print("Error Code Count:"+str(errCodeCount.items()))


if __name__ == "__main__":
    parse_log_file('test_log1.txt')