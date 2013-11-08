#!/usr/bin/python


import datetime
import json
import webapp2

from google.appengine.ext import db


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')
        
        json_str_list = open('json_titles.txt', 'r').readlines()
        json_obj_list = [json.loads(this_str) for this_str in json_str_list]
        for dict_obj in json_obj_list:
            # 'v' is our main video object for each title
            # All reviews are children of v
            # All collaborators are NameOccupation foreign keys in a list
            video_key_name = str(dict_obj['imdb_id'])
            v = Video(key_name=video_key_name)

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
                person_role_key = str(person) + '-' + str(role)
                n = NameOccupation.get_or_insert(person_role_key, name=person, occupation=role)
                person_role_key_list.append(n.key())

            # Ebert Review
            if 'formatted_review_text' in dict_obj:
                ebert_review_date = datetime.datetime.strptime(str(dict_obj['review_date']), "%Y-%m-%d").date()
                r = Review(
                    parent=v,
                    review_score=dict_obj['review_percent_score'],
                    review_author=dict_obj['review_author'],
                    review_source=dict_obj['review_source'],
                    review_content=dict_obj['formatted_review_text'],
                    review_date=ebert_review_date,
                )
                ebert_review_key = r.put()

            # Metacritic Review
            if 'metacritic_metascore_meter' in dict_obj:
                r = Review(
                    parent=v,
                    review_score=dict_obj['metacritic_metascore_meter'],
                    review_content=str(dict_obj['metacritic_metascore_total']),
                    review_source='Metacritic Metascore',
                )
                metacritic_metascore_key = r.put()

            if 'metacritic_userscore_meter' in dict_obj:
                r = Review(
                    parent=v,
                    review_score=dict_obj['metacritic_userscore_meter'],
                    review_content=str(dict_obj['metacritic_userscore_total']),
                    review_source='Metacritic Userscore',
                )
                metacritic_userscore_key = r.put()

            # Rottentomatoes Review
            if 'audience_meter' in dict_obj:
                r = Review(
                    parent=v,
                    review_score=dict_obj['audience_meter'],
                    review_content="%s (%s)" % (dict_obj['audience_avg_score'], dict_obj['audience_total']),
                    review_source='Rottentomatoes Audience Meter',
                )
                rottentomatoes_audience_key = r.put()

            if 'top_critics_rotten' in dict_obj:
                r = Review(
                    parent=v,
                    review_score=dict_obj['top_critics_meter'],
                    review_content="%s (+%s, -%s)" % (dict_obj['top_critics_avg_score'], 
                                                      dict_obj['top_critics_fresh'], 
                                                      dict_obj['top_critics_rotten']),
                    review_source='Rottentomatoes Top Critics',
                )
                rottentomatoes_top_critics_key = r.put()

            if 'all_critics_rotten' in dict_obj:
                r = Review(
                    parent=v,
                    review_score=dict_obj['all_critics_meter'],
                    review_content="%s (+%s, -%s)" % (dict_obj['all_critics_avg_score'], 
                                                      dict_obj['all_critics_fresh'], 
                                                      dict_obj['all_critics_rotten']),
                    review_source='Rottentomatoes All Critics',
                )
                rottentomatoes_all_critics_key = r.put()

            v.score=dict_obj["score"]
            v.aspect_ratio=dict_obj["aspect_ratio"]
            v.year=dict_obj["year"]
            v.length=dict_obj["length"]
            v.title=dict_obj["title"]
            v.rating=dict_obj["rating"]
            v.imdb_id=dict_obj["imdb_id"]
            v.poster_url=dict_obj["imdb_poster_url"]
            v.plot=dict_obj["plot"]
            v.tagline=dict_obj["tagline"]
            v.gross=dict_obj["gross"]
            v.budget=dict_obj["budget"]
            v.video_type=dict_obj["video_type"]
            v.genre_list=dict_obj["genre_list"]
            v.name_occupation_key_list=person_role_key_list

            v.put()


application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
