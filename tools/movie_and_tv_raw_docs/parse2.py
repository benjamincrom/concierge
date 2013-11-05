#!/usr/bin/python

import re
import html_manipulator
REGEX = re.compile("(.*?) \(\d\d\d\d\).*?")

total_movies = open('movie_list.txt', 'r').read().decode('latin-1').encode('ascii')

ebert_movies = open('ebert_movies.txt', 'r').readlines()
ebert_movies = [ html_manipulator.remove_html_tags(x.strip()) for x in ebert_movies ]

for m in ebert_movies:
    match = REGEX.search(m)
    if match:
        ebert_title = match.groups()[0]
        if not re.search(ebert_title, total_movies):
            print m

        

