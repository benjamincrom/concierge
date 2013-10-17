#!/usr/bin/python


import imdb_scraper
import metacritic_scraper
import roger_ebert_scraper
import rottentomatoes_scraper
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

        lines = open('test_list.txt').readlines()
        times = []
        for line in lines:
            (ebert_link, search_title, search_year) = line.split(';')
            ebert_link = ebert_link.strip()
            search_title = search_title.strip()
            search_year = search_year.strip()

            imdb_title_obj_dict = imdb_scraper.scrape_imdb_data(search_title, search_year)
            # If nothing is found then check the range below the search year to correct for inaccuracy
            if search_year and not imdb_title_obj_dict:
                search_year = int(search_year)
                search_year_list = [search_year - 1, search_year - 2]
                for current_search_year in search_year_list:
                    imdb_title_obj_dict = imdb_scraper.scrape_imdb_data(search_title, current_search_year)
                    if imdb_title_obj_dict:
                        break

            # If we can't get the IMDB scrape completed then there is no point in continuing
            if imdb_title_obj_dict:
                title = imdb_title_obj_dict["title"]
                media_type = imdb_title_obj_dict["video_type"]
                if imdb_title_obj_dict["year"]:
                    year = int(imdb_title_obj_dict["year"])
                else:
                    year = ''

                # Print IMDB data
                director_role_list = [(director, "Director") for director in imdb_title_obj_dict["director_list"]]
                writer_role_list = [(writer, "Writer") for writer in imdb_title_obj_dict["writer_list"]]
                star_role_list = [(star, "Star") for star in imdb_title_obj_dict["star_list"]]
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

                # If this is a TV Series then get the Metacritic data for every season
                if media_type == "TV Series":
                    season_list = range(1, imdb_title_obj_dict["tv_total_seasons"] + 1)
                    season_title_list = ["Season %s" % season_index for season_index in season_list]
                    # Print Metacritic data for each season
                    for season_title in season_title_list:
                        print season_title
                        metacritic_obj_dict = metacritic_scraper.scrape_metacritic(title, season=season_title)
                        if metacritic_obj_dict:
                            print '#########################################'
                            print ' METACRITIC '
                            for i, j in metacritic_obj_dict.iteritems():
                                print "%s:\t\t%s" % (i, j)

                            print '#########################################'

                # rogerebert and rottentomatoes only have good data for movies
                if media_type == "Movie":
                    year_list = [year, year - 1, year - 2]
                    # Get Metacritic data
                    for current_year in year_list:
                        metacritic_obj_dict = metacritic_scraper.scrape_metacritic(title, current_year)
                        if metacritic_obj_dict:
                            break

                    if not metacritic_obj_dict and title != search_title:
                        for current_year in year_list:
                            metacritic_obj_dict = metacritic_scraper.scrape_metacritic(search_title, current_year)
                            if metacritic_obj_dict:
                                break

                    # Print Metacritic data
                    if metacritic_obj_dict:
                        print '#########################################'
                        print ' METACRITIC '
                        for i, j in metacritic_obj_dict.iteritems():
                            print "%s:\t\t%s" % (i, j)

                        print '#########################################'

                    # Get Rottentomatoes data
                    for current_year in year_list:
                        rottentomatoes_obj_dict = rottentomatoes_scraper.scrape_rottentomatoes(title, current_year)
                        if rottentomatoes_obj_dict:
                            break

                    if not rottentomatoes_obj_dict and title != search_title:
                        for current_year in year_list:
                            rottentomatoes_obj_dict = rottentomatoes_scraper.scrape_rottentomatoes(search_title, current_year)
                            if rottentomatoes_obj_dict:
                                break

                    # Print Rottentomatoes data
                    if rottentomatoes_obj_dict:
                        print "''''''''''''''f''''''''''''''''''''''''''''''"
                        print ' ROTTEN TOMATOES '
                        for i, j in rottentomatoes_obj_dict.iteritems():
                            print "%s:\t\t%s" % (i, j)

                        print "''''''''''''''''''''''''''''''''''''''''''''"

                    if ebert_link:
                        # Get Rogerebert Data
                        rogerebert_obj_dict = roger_ebert_scraper.scrape_rogerebert_data(ebert_link)
                        # Print Rogerebert Data
                        if rogerebert_obj_dict:
                            print "============================================"
                            print ' ROGEREBERT '
                            for i, j in rogerebert_obj_dict.iteritems():
                                print "%s:\t\t%s" % (i, j)

                            print "============================================"

                print '***********************************************************************************'
                print ''
"""

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)