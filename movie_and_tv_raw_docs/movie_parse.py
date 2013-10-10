#!/usr/bin/python

import html_manipulator
import re

MOVIE_NAME_REGEX = re.compile("<li><i>(.+?)</i>.*?(\(.*?\d\d\d\d.*?\))</li>")
MOVIE_SERIES_REGEX = re.compile("<li><i>(.+?)</i> series:")
HTML_FILE_LIST = [
  '1.html',
  'a.html',
  'b.html',
  'c.html',
  'd.html',
  'e.html',
  'f.html',
  'g.html',
  'h.html',
  'i.html',
  'j.html',
  'l.html',
  'm.html',
  'n.html',
  'p.html',
  'q.html',
  's.html',
  't.html',
  'u.html',
  'x.html',
]

MOVIE_YEARS_REGEX = re.compile("(\d\d\d\d)")

for html_filename in HTML_FILE_LIST:

    f = open(html_filename, 'r')
    html_lines = f.readlines()
    f.close()

    series_name = False
    series_list = []
    for line in html_lines:
        m = MOVIE_NAME_REGEX.search(line)
        if m:
            title = html_manipulator.remove_html_tags(m.groups()[0])
            year_str = html_manipulator.remove_html_tags(m.groups()[1])
            year_list = MOVIE_YEARS_REGEX.findall(year_str)
            title_list = ["%s (%s)" %(title, year) for year in year_list]
            for name in title_list:
                if series_name: 
                    series_list.append(name)
                else:
                    print name

        series = html_manipulator.use_regex(MOVIE_SERIES_REGEX, line, True)
        if series:
            series_name = html_manipulator.remove_html_tags(series)

        if (series_name) and (line.strip() == "</li>"):
            print "&&&&& %s &&&&& %s" %(series_name, series_list)
            series_name = False
            series_list = []
