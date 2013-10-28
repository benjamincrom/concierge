#!/usr/bin/python


import json
import webapp2

from google.appengine.ext import db


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
    gross = db.TextProperty()
    imdb_id = db.StringProperty()
    budget = db.TextProperty()
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
        
        json_str_list = open('json_titles.txt', 'r').readlines()
        json_obj_list = [json.loads(this_str) for this_str in json_str_list]
        for dict_obj in json_obj_list:
            # Print IMDB data
            director_role_list = [(director, "Director") for director in dict_obj["director_list"]]
            writer_role_list = [(writer, "Writer") for writer in dict_obj["writer_list"]]
            star_role_list = [(star, "Star") for star in dict_obj["star_list"]]
            person_role_list = director_role_list + writer_role_list + star_role_list
            person_role_key_list = []

            if not dict_obj["score"]:
                dict_obj["score"] = None

            if not dict_obj["aspect_ratio"]:
                dict_obj["aspect_ratio"] = None

            if not dict_obj["year"]:
                dict_obj["year"] = None

            if not dict_obj["length"]:
                dict_obj["score"] = None

            for (person, role) in person_role_list:
                # Check if entry is already in database and get key if it is
                query = NameOccupation.all().filter('name =', person).filter('occupation =', role)
                key = query.get(keys_only=True)
                if not key:
                    n = NameOccupation(name=person, occupation=role)
                    key = n.put()
                person_role_key_list.append(key)

            v = Video(
                score=dict_obj["score"],
                aspect_ratio=dict_obj["aspect_ratio"],
                year=dict_obj["year"],
                length=dict_obj["length"],
                title=dict_obj["title"],
                rating=dict_obj["rating"],
                imdb_id=dict_obj["imdb_id"],
                poster_url=dict_obj["imdb_poster_url"],
                plot=dict_obj["plot"],
                tagline=dict_obj["tagline"],
                gross=dict_obj["gross"],
                budget=dict_obj["budget"],
                video_type=dict_obj["video_type"],
                genre_list=dict_obj["genre_list"],
                name_occupation_key_list=person_role_key_list,
            )
            v.put()


application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
