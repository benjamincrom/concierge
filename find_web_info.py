#!/usr/bin/python

import urllib
import json

class GetMediaMetadata:
    """This class will pull down data and metadata for reviews and media and store it in the database"""
    def __init__(self, title):
        self.title = title
        self.imdb_json_str = self.get_imdb_json_str()
        self.imdb_json_dict = self.encode_json_str_into_dict()

    def get_imdb_json_str(self):
        quoted_title = urllib.quote(self.title)
        json_response = urllib.urlopen("http://www.omdbapi.com/?t=%s" %(quoted_title))
        return json_response.read()

    def encode_json_str_into_dict(self):
        return json.loads(self.imdb_json_str)

