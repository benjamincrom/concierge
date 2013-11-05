

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