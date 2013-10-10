#!/usr/bin/python

import html_manipulator
import re

TV_NAME_REGEX = re.compile("<li><i><a href=.*? title=.*?>(.+?)</li>")

f = open('list.html', 'r')
html_lines = f.readlines()
f.close()

for line in html_lines:
    name = html_manipulator.use_regex(TV_NAME_REGEX, line, True)
    if name:
        sanitized_name = html_manipulator.remove_html_tags(name)
        print sanitized_name

