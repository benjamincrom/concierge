#!/usr/bin/python

from datetime import datetime
import json
import re
import string
import urllib

class Review:
    def __init__(self, content, author, source, date, percent_score):
        self.content = content
        self.author = author
        self.source = source
        self.date = date
        self.percent_score = percent_score


class Video:
    LOCAL_LINK_PREFIX = '<a href="'
    EBERT_LINK_PREFIX = '<a href="http://www.rogerebert.com'
    EBERT_REVIEW_NOT_FOUND = "There is no review on rogerebert.com for this title: %s"
    EBERT_REVIEWS_URL = "http://www.rogerebert.com/reviews/%s"
    EBERT_SITE_TITLE = "RogerEbert.com"
    EBERT_FULL_STAR = 'icon-star-full'
    EBERT_HALF_STAR = 'icon-star-half'

    EBERT_REVIEW_REGEX = re.compile('<div itemprop="reviewBody">(.+?)</div>', re.DOTALL)
    EBERT_AUTHOR_REGEX = re.compile('<meta content="(.+?)" name="author">')
    EBERT_DATE_REGEX = re.compile('itemprop="datePublished">(.+?)</time>')
    EBERT_STARS_REGEX = re.compile('itemprop="reviewRating"(.+?)</span>', re.DOTALL)

    def __init__(self, title):
        """This class will pull metadata from remote sources and store it in a video object"""
        # initialize empty lists
        self.review_obj_list = []

        # populate object with data
        self.set_imdb_data(title)
        self.set_rogerebert_data()

    def set_imdb_data(self, title):
        """ Pull down JSON data for this title from the IMDB API and store in imdb_json_dict """
        imdb_json_str = urllib.urlopen("http://www.omdbapi.com/?t=%s" %(urllib.quote(title))).read()
        imdb_json_dict = json.loads(imdb_json_str)

        # Check to see that the query returned a valid response
        if imdb_json_dict['Response'] == 'False':
            raise Exception(imdb_json_dict['Error'])

        # Store the following IMDB metadata directly in video object
        self.title = imdb_json_dict['Title']
        self.rating = imdb_json_dict['Rated']
        self.plot = imdb_json_dict['Plot']
        self.poster_url = imdb_json_dict['Poster']
        self.year = int(imdb_json_dict['Year'])
        self.video_type = imdb_json_dict['Type']

        # Convert the following IMDB metadata into the correct format and then store it in video object
        self.length = self.calculate_length_from_runtime_str(imdb_json_dict['Runtime'])

        # Split comma separated fields into python lists
        self.writer_list = [str(writer_name.strip()) for writer_name in imdb_json_dict['Writer'].split(',')]
        self.director_list = [str(director_name.strip()) for director_name in imdb_json_dict['Director'].split(',')]
        self.actor_list = [str(actor_name.strip()) for actor_name in imdb_json_dict['Actors'].split(',')]
        self.genre_list = [str(genre_name.strip()) for genre_name in imdb_json_dict['Genre'].split(',')]

    def set_rogerebert_data(self):
        """ Search for rogerbert.com review by querying '[title]-[year]', '[title]-[year+1]', and '[title]-[year-1]'"""
        year_list = [self.year - 1, self.year, self.year + 1]
        for selected_year in year_list:
            ebert_review_url = self.get_ebert_review_url(self.title, selected_year)
            ebert_review_html = urllib.urlopen(ebert_review_url).read()

            review_text_match = self.EBERT_REVIEW_REGEX.search(ebert_review_html)
            if review_text_match:
                review_text = review_text_match.groups()[0]
                formatted_review_text = self.format_ebert_review_text(review_text)

                review_author_match = self.EBERT_AUTHOR_REGEX.search(ebert_review_html)
                review_author = review_author_match.groups()[0]

                review_date_match = self.EBERT_DATE_REGEX.search(ebert_review_html)
                review_date_string = review_date_match.groups()[0]
                review_date = datetime.strptime(review_date_string, '%B %d, %Y')

                review_stars_match = self.EBERT_STARS_REGEX.search(ebert_review_html)
                review_stars_string = review_stars_match.groups()[0]
                review_percent_score = self.get_ebert_percent_score(review_stars_string)

                new_review_obj = Review(
                                    formatted_review_text,
                                    review_author,
                                    self.EBERT_SITE_TITLE,
                                    review_date,
                                    review_percent_score,
                                    )

                self.review_obj_list.append(new_review_obj)

    @classmethod
    def get_ebert_percent_score(cls, review_stars_string):
        full_stars = len(re.findall(cls.EBERT_FULL_STAR, review_stars_string))
        half_stars = len(re.findall(cls.EBERT_HALF_STAR, review_stars_string))
        review_percent_score = 100*(full_stars*2 + half_stars)/8.0
        return review_percent_score

    @classmethod
    def get_ebert_review_url(cls, title, year):
        title_str = str(title)
        sanitized_title = title_str.translate(string.maketrans("",""), string.punctuation)
        lowercase_hyphenated_title = sanitized_title.lower().replace(' ', '-')
        url_formatted_title = urllib.quote("%s-%s" %(lowercase_hyphenated_title, year))
        ebert_review_url = cls.EBERT_REVIEWS_URL %(url_formatted_title)
        return ebert_review_url

    @classmethod
    def format_ebert_review_text(cls, review_text):
        review_text = review_text.replace('\n', '')
        formatted_review_text = review_text.replace(cls.LOCAL_LINK_PREFIX, cls.EBERT_LINK_PREFIX)
        return formatted_review_text

    @classmethod
    def calculate_length_from_runtime_str(cls, runtime_str):
        """ Given a runtime of the format '2 h 24 min' return the length in minutes """
        match_object = re.match("(\d+) h (\d+) min", runtime_str)
        hours, minutes = match_object.groups()
        length = int(hours)*60 + int(minutes)
        return length


if __name__ == '__main__':
    g = Video('Men in Black II')
    print g.title
    print g.year
    print g.length
    print g.poster_url
    print g.plot
    print g.rating
    print g.video_type
    print g.genre_list
    print g.writer_list
    print g.director_list
    print g.actor_list
    # print g.budget
    # print g.gross
    # print g.tagline
    # print g.aspect_ratio
    # print g.collection_obj (if exists--properties: name, season, episode, index)
    print "=============================="
    for review_obj in g.review_obj_list: # (review_obj properties: source, percent_score, headline, text)
        print "Review: "
        print review_obj.content
        print review_obj.source
        print review_obj.author
        print review_obj.percent_score
        print review_obj.date
    print "=============================="
