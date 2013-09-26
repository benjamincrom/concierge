#!/usr/bin/python


import json
import re
import string
import urllib

from datetime import datetime


class Review:
    def __init__(self, content, author, source, date, percent_score):
        self.content = content
        self.author = author
        self.source = source
        self.date = date
        self.percent_score = percent_score


class Video:
    IMDB_LOOKUP_404 = '{"Response":"False","Error":"Movie not found!"}'
    IMDB_LOOKUP_URL = "http://www.omdbapi.com/?t=%s"
    IMDB_API_404 = '{"code":404, "error":"Film not found"}'
    IMDB_API_URL = ("http://mymovieapi.com/?id=%s&type=json&plot=simple&episode=1&lang=en-US&aka=simple&release="
                    "simple&business=1&tech=1")
    IMDB_URL_DELIMITER = '+'

    LOCAL_LINK_PREFIX = '<a href="'
    EBERT_LINK_PREFIX = '<a href="http://www.rogerebert.com'
    EBERT_FULL_STAR = 'icon-star-full'
    EBERT_HALF_STAR = 'icon-star-half'
    EBERT_REVIEW_NOT_FOUND = "There is no review on rogerebert.com for this title: %s"
    EBERT_REVIEW_URL = "http://www.rogerebert.com/reviews/%s"
    EBERT_SITE_TITLE = "RogerEbert.com"
    EBERT_URL_DELIMITER = '-'

    IMDB_RUNTIME_REGEX = re.compile("(\d+) min")
    IMDB_RATING_REGEX = re.compile("itemprop=\"contentRating\" content=\"(.+?)\"></span>")
    IMDB_TITLE_REGEX = re.compile("itemprop=\"name\">(.+?)</span>")
    IMDB_TAGLINE_REGEX = re.compile("Taglines:</h4>\n(.+?)\s*<", re.DOTALL)
    EBERT_REVIEW_REGEX = re.compile('<div itemprop="reviewBody">(.+?)</div>', re.DOTALL)
    EBERT_AUTHOR_REGEX = re.compile('<meta content="(.+?)" name="author">')
    EBERT_DATE_REGEX = re.compile('itemprop="datePublished">(.+?)</time>')
    EBERT_STARS_REGEX = re.compile('itemprop="reviewRating"(.+?)</span>', re.DOTALL)

    def __init__(self, title):
        """This class will pull data for this title from remote sources and store it in a video object"""
        self.review_obj_list = []
        self.set_imdb_data(title)
        self.set_rogerebert_data()

    def set_imdb_data(self, title):
        """ Pull down JSON data for this title from the IMDB API and store in imdb_json_dict """
        imdb_id = self.get_imdb_id_from_title(title)
        imdb_json_dict = self.get_json_dict_from_imdb_id(imdb_id)
        imdb_html = urllib.urlopen(imdb_json_dict['imdb_url']).read()

        self.plot = imdb_json_dict['plot_simple']
        self.poster_url = imdb_json_dict['poster']['cover']
        self.video_type = imdb_json_dict['type']
        self.year = int(imdb_json_dict['year'])

        self.actor_list = [actor.encode('ascii','ignore') for actor in imdb_json_dict['actors']]
        self.director_list = [director.encode('ascii','ignore') for director in imdb_json_dict['directors']]
        self.genre_list = [genre.encode('ascii','ignore') for genre in imdb_json_dict['genres']]
        self.writer_list = [writer.encode('ascii','ignore') for writer in imdb_json_dict['writers']]

        self.aspect_ratio = self.get_aspect_ratio_float_from_str(imdb_json_dict['technical']['aspect_ratio'][0])

        # Extract the length in number of minutes as an int from this type of string: '135 min'
        length_match = self.IMDB_RUNTIME_REGEX.search(imdb_json_dict['runtime'][0].encode('ascii','ignore'))
        self.length = int(length_match.groups()[0])

        # Extract the title, rating, and tagline from the scraped IMDB html since the API sucks at this
        title_match = self.IMDB_TITLE_REGEX.search(imdb_html)
        self.title = title_match.groups()[0]

        rating_match = self.IMDB_RATING_REGEX.search(imdb_html)
        self.rating = rating_match.groups()[0]

        tagline_match = self.IMDB_TAGLINE_REGEX.search(imdb_html)
        if tagline_match:
            self.tagline = tagline_match.groups()[0]
        else:
            self.tagline = None

        if 'budget' in imdb_json_dict['business']:
            self.budget = imdb_json_dict['business']['budget'][0]['money']
        else:
            self.budget = None

        if 'gross' in imdb_json_dict['business']:
            self.gross = imdb_json_dict['business']['gross'][0]['money']
        else:
            self.gross = None

    def set_rogerebert_data(self):
        """ Search for rogerbert.com review by querying '[title]-[year]', '[title]-[year+1]', and '[title]-[year-1]'"""
        year_list = [self.year - 1, self.year, self.year + 1]
        for selected_year in year_list:
            ebert_review_url = self.format_ebert_review_url(self.title, selected_year)
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
                review_percent_score = self.compute_ebert_percent_score(review_stars_string)

                new_review_obj = Review(
                                        formatted_review_text,
                                        review_author,
                                        self.EBERT_SITE_TITLE,
                                        review_date,
                                        review_percent_score,
                                        )
                self.review_obj_list.append(new_review_obj)

    @classmethod
    def get_imdb_id_from_title(cls, title):
        lookup_str = urllib.urlopen(cls.IMDB_LOOKUP_URL %(urllib.quote(title))).read()
        if lookup_str == cls.IMDB_LOOKUP_404:
            raise Exception(cls.IMDB_LOOKUP_404)
        lookup_json_obj = json.loads(lookup_str)
        return lookup_json_obj['imdbID']

    @classmethod
    def get_json_dict_from_imdb_id(cls, imdb_id):
        imdb_json_str = urllib.urlopen(cls.IMDB_API_URL %(imdb_id)).read()
        if imdb_json_str == cls.IMDB_API_404:
            raise Exception(cls.IMDB_API_404)
        return json.loads(imdb_json_str)

    @classmethod
    def get_aspect_ratio_float_from_str(cls, aspect_ratio_str):
        width, height = aspect_ratio_str.split(' : ')
        trimmed_height = height.split(' ')[0]
        return float(width) / float(trimmed_height)

    @classmethod
    def sanitize_url_segment(cls, url_segment, delimiter):
        url_str = url_segment.encode('ascii','ignore')
        url_str_no_punctuation = url_str.translate(string.maketrans("",""), string.punctuation)
        sanitized_url_str = url_str_no_punctuation.replace(' ', delimiter)
        return sanitized_url_str

    @classmethod
    def format_ebert_review_text(cls, review_text):
        review_text = review_text.replace('\n', '')
        formatted_review_text = review_text.replace(cls.LOCAL_LINK_PREFIX, cls.EBERT_LINK_PREFIX)
        return formatted_review_text

    @classmethod
    def compute_ebert_percent_score(cls, review_stars_string):
        full_stars = len(re.findall(cls.EBERT_FULL_STAR, review_stars_string))
        half_stars = len(re.findall(cls.EBERT_HALF_STAR, review_stars_string))
        review_percent_score = 100*(full_stars*2 + half_stars)/8.0
        return review_percent_score

    @classmethod
    def format_ebert_review_url(cls, title, year):
        title_str = cls.sanitize_url_segment(title, cls.EBERT_URL_DELIMITER).lower()
        url_formatted_title = urllib.quote("%s-%s" %(title_str, year))
        ebert_review_url = cls.EBERT_REVIEW_URL %(url_formatted_title)
        return ebert_review_url


if __name__ == '__main__':
    g = Video('This is the End')
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
    print g.budget
    print g.gross
    print g.aspect_ratio
    print g.tagline
    # print g.collection_obj (if exists--properties: name, season, episode, index)
    print "=============================="
    for review_obj in g.review_obj_list:
        print "Review: "
        print review_obj.content
        f = open('test.html','w')
        f.write(review_obj.content)
        f.close()
        print review_obj.source
        print review_obj.author
        print review_obj.percent_score
        print review_obj.date
    print "=============================="
