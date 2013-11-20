#!/usr/bin/python


from google.appengine.ext import db
from protorpc import messages


ROGEREBERT_REVIEW_SOURCE = 'RogerEbert.com'
ROTTENTOMATOES_TOP_CRITICS_SOURCE = 'Rottentomatoes Top Critics'
ROTTENTOMATOES_ALL_CRITICS_SOURCE = 'Rottentomatoes All Critics'
ROTTENTOMATOES_AUDIENCE_METER_SOURCE = 'Rottentomatoes Audience Meter'
METACRITIC_METASCORE_SOURCE = 'Metacritic Metascore'
METACRITIC_USERSCORE_SOURCE = 'Metacritic Userscore'


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


class ReviewMessage(messages.Message):
    review_source = messages.StringField(1)
    review_author = messages.StringField(2)
    review_content = messages.StringField(3)
    review_sample = messages.StringField(4)
    review_date = messages.StringField(5)
    review_score = messages.FloatField(6)


class VideoMessage(messages.Message):
    poster_url = messages.StringField(1)
    title = messages.StringField(2)
    plot = messages.StringField(3)
    tagline = messages.StringField(4)
    budget = messages.StringField(5)
    gross = messages.StringField(6)
    rating = messages.StringField(7)
    video_type = messages.StringField(8)
    aspect_ratio = messages.StringField(9)
    imdb_id = messages.StringField(10)
    score = messages.FloatField(11)
    length = messages.IntegerField(12)
    year = messages.IntegerField(13)
    genre_list_str = messages.StringField(14)
    ebert_review = messages.MessageField(ReviewMessage, 16)
    metacritic_metascore_review = messages.MessageField(ReviewMessage, 17)
    metacritic_userscore_review = messages.MessageField(ReviewMessage, 18)
    rottentomatoes_top_critics_review = messages.MessageField(ReviewMessage, 19)
    rottentomatoes_all_critics_review = messages.MessageField(ReviewMessage, 20)
    rottentomatoes_audience_meter_review = messages.MessageField(ReviewMessage, 21)
    director_list_str = messages.StringField(22)
    writer_list_str = messages.StringField(23)
    star_list_str = messages.StringField(24)


class VideoMessageCollection(messages.Message):
    video_list = messages.MessageField(VideoMessage, 1, repeated=True)