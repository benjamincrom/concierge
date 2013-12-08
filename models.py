#!/usr/bin/python


import re

from google.appengine.ext import db
from protorpc import messages


ROGEREBERT_REVIEW_SOURCE = "RogerEbert.com"
ROTTENTOMATOES_ALL_CRITICS_SOURCE = "Rottentomatoes All Critics"
ROTTENTOMATOES_AUDIENCE_METER_SOURCE = "Rottentomatoes Audience Meter"
ROTTENTOMATOES_TOP_CRITICS_SOURCE = "Rottentomatoes Top Critics"
METACRITIC_METASCORE_SOURCE = "Metacritic Metascore"
METACRITIC_USERSCORE_SOURCE = "Metacritic Userscore"

EBERT_REVIEW_SAMPLE_REGEX = re.compile("<p>(.+?)</p>", re.DOTALL)


# Appengine DB declaration
class NameOccupation(db.Model):
    name = db.StringProperty()
    occupation = db.StringProperty()


class Review(db.Model):
    review_author = db.StringProperty()
    review_source = db.StringProperty()
    review_content = db.TextProperty()
    review_score = db.FloatProperty()
    review_date = db.DateProperty()


class Video(db.Model):
    title = db.StringProperty()
    poster_url = db.StringProperty()
    imdb_id = db.StringProperty()
    video_type = db.StringProperty()
    rating = db.StringProperty()
    genre_list = db.StringListProperty()
    tagline = db.TextProperty()
    plot = db.TextProperty()
    gross = db.TextProperty()
    budget = db.TextProperty()
    aspect_ratio = db.FloatProperty()
    score = db.FloatProperty()
    year = db.IntegerProperty()
    length = db.IntegerProperty()
    name_occupation_key_list = db.ListProperty(db.Key)
    review_key_list = db.ListProperty(db.Key)


# Messaging object declarations
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
    genre_list_str = messages.StringField(11)
    director_list_str = messages.StringField(12)
    writer_list_str = messages.StringField(13)
    star_list_str = messages.StringField(14)
    score = messages.FloatField(15)
    length = messages.IntegerField(16)
    year = messages.IntegerField(17)
    ebert_review = messages.MessageField(ReviewMessage, 18)
    metacritic_metascore_review = messages.MessageField(ReviewMessage, 19)
    metacritic_userscore_review = messages.MessageField(ReviewMessage, 20)
    rottentomatoes_top_critics_review = messages.MessageField(ReviewMessage, 21)
    rottentomatoes_all_critics_review = messages.MessageField(ReviewMessage, 22)
    rottentomatoes_audience_meter_review = messages.MessageField(ReviewMessage, 23)


class VideoMessageCollection(messages.Message):
    video_list = messages.MessageField(VideoMessage, 1, repeated=True)
