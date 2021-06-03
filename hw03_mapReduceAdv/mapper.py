#!/usr/bin/python
import sys
import re


def contains_row_id(text):
    """
    the function finds 'row Id' in the string
    return bool
    :param text: a string from stdin
    """
    return bool(re.match(r'\s*<row', text))


def get_year(text):
    """
    the fuction extracts some years from the text
    return substring or None
    :param text: a string from stdin
    """
    substring = re.search(r'CreationDate="\d{4}', text)
    if substring:
        return substring.group(0).split('="')[1]
    else:
        return None


def get_tags(text):
    """
    the function extracts some tags
    return a list od tags
    :param text: a string from stdin
    """
    try:
        result = text.split('Tags="')[1].split('"')[0]
        return re.sub('&lt;|&gt|\s*', '', result).split(sep=";")
    except:
        return None


for line in sys.stdin:
    if contains_row_id(line):
        year = get_year(line)
        tags = get_tags(line)
        if tags and year in ('2010', '2016'):
            for tag in tags:
                if tag != '':
                    print(year, tag, 1, sep = "\t", end = "\n")
