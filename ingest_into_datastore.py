#!/usr/bin/python


import datetime
import json
import webapp2

import models


INGEST_SUCCESS_MESSAGE = 'Ingest completed!'
JSON_TITLES_FILE = 'tools/scraper/text_files/json_titles.txt'


class MainPage(webapp2.RequestHandler):
    def get(self):
        # Read JSON objects from file and load into list of JSON dictionaries (one for each video title)
        json_str_list = open(JSON_TITLES_FILE, 'r').readlines()
        json_obj_list = [json.loads(this_str) for this_str in json_str_list]

        # Iterate through JSON dictionary objects
        for dict_obj in json_obj_list:
            # video_obj is our main video object for each title (keyed on IMDB ID)
            # Reviews are children of video_obj
            # Collaborators are stored as NameOccupation keys in a list in video_obj
            video_key_name = str(dict_obj['imdb_id'])
            video_obj = models.Video(key_name=video_key_name)

            # Store all occupation data in NameOccupation objects and store all keys in a single list in this video_obj
            occupation_dict = {"Director": dict_obj["director_list"],
                               "Writer":   dict_obj["writer_list"],
                               "Star":     dict_obj["star_list"]}

            # Create a NameOccupation obj for each writer, director, and star and append each key to a list in video_obj
            person_role_key_list = []
            for (role, person_list) in occupation_dict.iteritems():
                for person in person_list:
                    person_role_key = str(person) + '-' + str(role)
                    name_occupation_obj = models.NameOccupation.get_or_insert(person_role_key,
                                                                              name=person,
                                                                              occupation=role)
                    person_role_key_list.append(name_occupation_obj.key())

            # Store Ebert Review in a review_obj that is a child of this video_obj
            if 'formatted_review_text' in dict_obj:
                ebert_review_date = datetime.datetime.strptime(str(dict_obj['review_date']), "%Y-%m-%d").date()
                review_obj = models.Review(
                    parent=video_obj,
                    review_score=dict_obj['review_percent_score'],
                    review_author=dict_obj['review_author'],
                    review_content=dict_obj['formatted_review_text'],
                    review_date=ebert_review_date,
                    review_source=models.ROGEREBERT_REVIEW_SOURCE,
                )
                review_obj.put()

            # Store Metacritic Reviews in review objects that are children of this video_obj
            # (Metascore, Userscore)
            if 'metacritic_metascore_meter' in dict_obj:
                review_obj = models.Review(
                    parent=video_obj,
                    review_score=dict_obj['metacritic_metascore_meter'],
                    review_content=str(dict_obj['metacritic_metascore_total']),
                    review_source=models.METACRITIC_METASCORE_SOURCE,
                )
                review_obj.put()

            if 'metacritic_userscore_meter' in dict_obj:
                review_obj = models.Review(
                    parent=video_obj,
                    review_score=dict_obj['metacritic_userscore_meter'],
                    review_content=str(dict_obj['metacritic_userscore_total']),
                    review_source=models.METACRITIC_USERSCORE_SOURCE,
                )
                review_obj.put()

            # Store Rottentomatoes Reviews in review objects that are children of this video_obj
            # (Audience, Top Critics, All Critics)
            if 'audience_meter' in dict_obj:
                review_obj = models.Review(
                    parent=video_obj,
                    review_score=dict_obj['audience_meter'],
                    review_content="%s (%s)" % (dict_obj['audience_avg_score'], dict_obj['audience_total']),
                    review_source=models.ROTTENTOMATOES_AUDIENCE_METER_SOURCE,
                )
                review_obj.put()

            if 'top_critics_rotten' in dict_obj:
                review_obj = models.Review(
                    parent=video_obj,
                    review_score=dict_obj['top_critics_meter'],
                    review_content="%s (+%s, -%s)" % (dict_obj['top_critics_avg_score'], 
                                                      dict_obj['top_critics_fresh'], 
                                                      dict_obj['top_critics_rotten']),
                    review_source=models.ROTTENTOMATOES_TOP_CRITICS_SOURCE,
                )
                review_obj.put()

            if 'all_critics_rotten' in dict_obj:
                review_obj = models.Review(
                    parent=video_obj,
                    review_score=dict_obj['all_critics_meter'],
                    review_content="%s (+%s, -%s)" % (dict_obj['all_critics_avg_score'], 
                                                      dict_obj['all_critics_fresh'], 
                                                      dict_obj['all_critics_rotten']),
                    review_source=models.ROTTENTOMATOES_ALL_CRITICS_SOURCE,
                )
                review_obj.put()

            # Initialize any missing video_obj fields to None
            if not dict_obj["score"]:
                dict_obj["score"] = None

            if not dict_obj["aspect_ratio"]:
                dict_obj["aspect_ratio"] = None

            if not dict_obj["year"]:
                dict_obj["year"] = None

            if not dict_obj["length"]:
                dict_obj["score"] = None

            # Store IMDB data in video_obj
            video_obj.score = dict_obj["score"]
            video_obj.aspect_ratio = dict_obj["aspect_ratio"]
            video_obj.year = dict_obj["year"]
            video_obj.length = dict_obj["length"]
            video_obj.title = dict_obj["title"]
            video_obj.rating = dict_obj["rating"]
            video_obj.imdb_id = dict_obj["imdb_id"]
            video_obj.poster_url = dict_obj["imdb_poster_url"]
            video_obj.plot = dict_obj["plot"]
            video_obj.tagline = dict_obj["tagline"]
            video_obj.gross = dict_obj["gross"]
            video_obj.budget = dict_obj["budget"]
            video_obj.video_type = dict_obj["video_type"]
            video_obj.genre_list = dict_obj["genre_list"]
            video_obj.name_occupation_key_list = person_role_key_list

            video_obj.put()

        # Output plain text success message upon completion
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(INGEST_SUCCESS_MESSAGE)


ingest_application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
