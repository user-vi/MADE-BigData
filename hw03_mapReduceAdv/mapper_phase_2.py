#!/usr/bin/python

import sys


for line in sys.stdin:
    year, word, counts = line.split("\t", 2)
    count = counts.split("\n")[0]
    print(year, count, word, sep = "\t", end = "\n")
