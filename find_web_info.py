#!/usr/bin/python

import urllib
import json
import re

class Video:
    """This class will pull metadata from remote sources and store it in a video object"""
    def __init__(self, title):
        # Pull down JSON from IMDB keyed on title
        imdb_json_str = self.get_imdb_json_str(title)
        imdb_json_dict = self.encode_json_str_into_dict(imdb_json_str)

        # Store IMDB metadata in video object
        self.title = imdb_json_dict['Title']
        self.rating = imdb_json_dict['Rated']
        self.plot = imdb_json_dict['Plot']
        self.poster_url = imdb_json_dict['Poster']
        self.year = imdb_json_dict['Year']
        self.video_type = imdb_json_dict['Type']

        # Split comma separated fields into python lists
        self.writer_list = [str(writer_name.strip()) for writer_name in imdb_json_dict['Writer'].split(',')]
        self.director_list = [str(director_name.strip()) for director_name in imdb_json_dict['Director'].split(',')]
        self.actor_list = [str(actor_name.strip()) for actor_name in imdb_json_dict['Actors'].split(',')]
        self.genre_list = [str(genre_name.strip()) for genre_name in imdb_json_dict['Genre'].split(',')]

        # Calculate runtime in minutes and store in object
        runtime = imdb_json_dict['Runtime']
        m = re.match("(\d+) h (\d+) min", runtime) 
        hours, minutes = m.groups()
        self.length = int(hours)*60 + int(minutes)

    @classmethod
    def get_imdb_json_str(cls, title):
        quoted_title = urllib.quote(title)
        json_response = urllib.urlopen("http://www.omdbapi.com/?t=%s" %(quoted_title))
        return json_response.read()

    @classmethod
    def encode_json_str_into_dict(cls, json_str):
        return json.loads(json_str)

if __name__ == '__main__':
    g = Video('The Terminal')
    print g.title
    print g.rating
    print g.plot
    print g.poster_url
    print g.writer_list
    print g.director_list
    print g.actor_list
    print g.genre_list
    print g.year
    print g.length
    print g.video_type
