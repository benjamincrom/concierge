#!/usr/bin/python


import imdb_scraper
import metacritic_scraper
import roger_ebert_scraper
import rottentomatoes_scraper

import json
import webapp2

from google.appengine.ext import db
from google.appengine.api import users


class NameOccupation(db.Model):
    name = db.StringProperty()
    occupation = db.StringProperty()


class Review(db.Model):
    review_content = db.TextProperty()
    review_score = db.StringProperty()
    review_author = db.StringProperty()
    review_source = db.StringProperty()
    review_date = db.DateProperty()


class Series(db.Model):
    series_name = db.StringProperty()
    total_episodes_in_series = db.IntegerProperty()
    total_seasons_in_series = db.IntegerProperty()
    genre_list = db.StringListProperty()
    creator = db.ReferenceProperty(NameOccupation)
    season_key_list = db.ListProperty(db.Key)


class Season(db.Model):
    season_number = db.IntegerProperty()
    total_episodes_in_season = db.IntegerProperty()
    series = db.ReferenceProperty(Series)
    review_key_list = db.ListProperty(db.Key)


class Video(db.Model):
    title = db.StringProperty()
    poster_url = db.StringProperty()
    plot = db.TextProperty()
    tagline = db.StringProperty()
    gross = db.StringProperty()
    imdb_id = db.StringProperty()
    budget = db.StringProperty()
    video_type = db.StringProperty()
    rating = db.StringProperty()
    genre_list = db.StringListProperty()
    aspect_ratio = db.FloatProperty()
    score = db.FloatProperty()
    episode_number_in_season = db.IntegerProperty()
    episode_number_in_total = db.IntegerProperty()
    year = db.IntegerProperty()
    length = db.IntegerProperty()
    name_occupation_key_list = db.ListProperty(db.Key)
    review_key_list = db.ListProperty(db.Key)
    season = db.ReferenceProperty(Season)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')
        
        json_str_list = open('json_titles.txt','r').readlines()
        json_obj_list = [json.loads(this_str) for this_str in json_str_list]
        for obj_dict in json_obj_list:

            # Print IMDB data
            director_role_list = [(director, "Director") for director in obj_dict["director_list"]]
            writer_role_list = [(writer, "Writer") for writer in obj_dict["writer_list"]]
            star_role_list = [(star, "Star") for star in obj_dict["star_list"]]
            person_role_list = director_role_list + writer_role_list + star_role_list
            person_role_key_list = []

            for (person,role) in person_role_list:
                n = NameOccupation(
                    name=person,
                    occupation=role,
                    )
                key = n.put()
                person_role_key_list.append(key)

            v = Video(
                title=imdb_title_obj_dict["title"],
                score=imdb_title_obj_dict["score"],
                year=imdb_title_obj_dict["year"],
                length=imdb_title_obj_dict["length"],
                rating=imdb_title_obj_dict["rating"],
                imdb_id=imdb_title_obj_dict["imdb_id"],
                poster_url=imdb_title_obj_dict["imdb_poster_url"],
                plot=imdb_title_obj_dict["plot"],
                tagline=imdb_title_obj_dict["tagline"],
                gross=imdb_title_obj_dict["gross"],
                budget=imdb_title_obj_dict["budget"],
                video_type=imdb_title_obj_dict["video_type"],
                aspect_ratio=imdb_title_obj_dict["aspect_ratio"],
                genre_list=imdb_title_obj_dict["genre_list"],
                name_occupation_key_list=person_role_key_list,
            )
            v.put()


application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
