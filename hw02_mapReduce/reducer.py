#!/usr/bin/python
import sys


LASTKEY = None
IDS = []
for line in sys.stdin:
    (key, value) = line.strip().split("\t")
    if (LASTKEY is not None and LASTKEY != key) or (len(IDS) == 5):
        print(','.join(IDS))
        IDS = []
    LASTKEY = key
    IDS.append(value)
if LASTKEY is not None:
    print(','.join(IDS))
