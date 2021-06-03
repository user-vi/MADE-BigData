#!/usr/bin/python

import sys
import random


for line in sys.stdin:
    fields = line.split("\t")
    key = random.randint(0, 30000)
    print(str(key) + "\t" + str(fields[0]), end = '')
