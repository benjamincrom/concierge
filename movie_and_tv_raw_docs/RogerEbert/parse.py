#!/usr/bin/python
import re

review_blocks = open('Reviews_Roger_Ebert.html').read().split('<figure class="movie review">')

BLOCK_REGEX = re.compile(
    "</a><h5 class=\"title\">.*?>(.+?)</a>.*?<span class=\"release-year\">\((\d\d\d\d)\)</span>",
    re.DOTALL
)

for block in review_blocks:
    m = BLOCK_REGEX.search(block)
    if m:
        film_str = "%s (%s)" %(m.groups()[0].strip(), m.groups()[1].strip())
        print film_str
   
