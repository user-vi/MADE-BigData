#!/usr/bin/python

import sys

i = 0
last_year = 0
for line in sys.stdin:
    year, counts, word = line.split("\t", 2)
    if year != last_year:
        i = 0
    if i < 10:
        print(year, word.split("\n")[0], counts, sep = "\t")
    i += 1
    last_year = year
