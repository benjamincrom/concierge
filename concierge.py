#!/usr/bin/python


import datetime
import json
import webapp2

from google.appengine.ext import db


class NameOccupation(db.Model):
    name = db.StringProperty()
    occupation = db.StringProperty()


class Review(db.Model):
    review_score = db.FloatProperty()
    review_author = db.StringProperty()
    review_source = db.StringProperty()
    review_content = db.TextProperty()
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
            review_key_list = []

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

            # Ebert Review
            if 'formatted_review_text' in dict_obj:
                ebert_review_date = datetime.datetime.strptime(str(dict_obj['review_date']), "%Y-%m-%d").date()
                r = Review(
                    review_score=dict_obj['review_percent_score'],
                    review_author=dict_obj['review_author'],
                    review_source=dict_obj['review_source'],
                    review_content=dict_obj['formatted_review_text'],
                    review_date=ebert_review_date,
                )
                ebert_review_key = r.put()
                review_key_list.append(ebert_review_key)

            # Metacritic Review
            if 'metacritic_metascore_meter' in dict_obj:
                r = Review(
                    review_score=dict_obj['metacritic_metascore_meter'],
                    review_content=str(dict_obj['metacritic_metascore_total']),
                    review_source='Metacritic Metascore',
                )
                metacritic_metascore_key = r.put()
                review_key_list.append(metacritic_metascore_key)

            if 'metacritic_userscore_meter' in dict_obj:
                r = Review(
                    review_score=dict_obj['metacritic_userscore_meter'],
                    review_content=str(dict_obj['metacritic_userscore_total']),
                    review_source='Metacritic Userscore',
                )
                metacritic_userscore_key = r.put()
                review_key_list.append(metacritic_userscore_key)

            # Rottentomatoes Review
            if 'audience_meter' in dict_obj:
                r = Review(
                    review_score=dict_obj['audience_meter'],
                    review_content="%s (%s)" % (dict_obj['audience_avg_score'], dict_obj['audience_total']),
                    review_source='Rottentomatoes Audience Meter',
                )
                rottentomatoes_audience_key = r.put()
                review_key_list.append(rottentomatoes_audience_key)

            if 'top_critics_rotten' in dict_obj:
                r = Review(
                    review_score=dict_obj['top_critics_meter'],
                    review_content="%s (+%s, -%s)" % (dict_obj['top_critics_avg_score'], dict_obj['top_critics_fresh'], dict_obj['top_critics_rotten']),
                    review_source='Rottentomatoes Top Critics',
                )
                rottentomatoes_top_critics_key = r.put()
                review_key_list.append(rottentomatoes_top_critics_key)

            if 'all_critics_rotten' in dict_obj:
                r = Review(
                    review_score=dict_obj['all_critics_meter'],
                    review_content="%s (+%s, -%s)" % (dict_obj['all_critics_avg_score'], dict_obj['all_critics_fresh'], dict_obj['all_critics_rotten']),
                    review_source='Rottentomatoes All Critics',
                )
                rottentomatoes_all_critics_key = r.put()
                review_key_list.append(rottentomatoes_all_critics_key)

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
                review_key_list=review_key_list,
            )
            v.put()


application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
