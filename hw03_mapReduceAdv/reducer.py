#!/usr/bin/python
import sys

current_word = None
current_year = None
word_count = 0

for line in sys.stdin:
    test = line.split("\t", 2)
    year, word, counts = line.split("\t", 2)
    counts = int(counts)
    if (word == current_word) & (year == current_year):
        word_count += counts
    else:
        if current_word and current_year:
            print(current_year, current_word, word_count, sep="\t", end = "\n")
        current_year = year
        current_word = word
        word_count = counts

if current_word and current_year:
    print(current_year, current_word, word_count, sep="\t", end = "\n")
