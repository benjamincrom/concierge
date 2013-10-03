#!/usr/bin/python


import json
import re
import string
import urllib

from datetime import datetime


class Video:
    def __init__(self, title):
        self.review_obj_list = []
        # set IMDB data
        # set rogerebert data


if __name__ == '__main__':
    g = Video('Rocky')
    print g.title
    print g.video_type
    print g.year
    print g.length
    print g.poster_url
    print g.rating
    print g.budget
    print g.gross
    print g.aspect_ratio
    print g.tagline
    print g.genre_list
    print g.writer_list
    print g.director_list
    print g.actor_list
    print g.plot
    # print g.collection_obj (if exists--properties: name, season, episode, index)
    print "=============================="
    for review_obj in g.review_obj_list:
        print "Review: "
        print review_obj.content
        f = open('test.html','w')
        f.write(review_obj.content)
        f.close()
        print review_obj.source
        print review_obj.author
        print review_obj.percent_score
        print review_obj.date
    print "=============================="
