#!/usr/bin/python

import urllib
import re

from pygoogle import pygoogle


class RogerEbertScraper:

    def __init__(self):
        return


class ImdbScraper:

    def __init__(self):
        return

    IMDB_GOOGLE_QUERY_STRING = "imdb %s"
    IMDB_TYPE_MOVIE = "Movie"
    IMDB_TYPE_TV_EPISODE = "TV Episode"
    IMDB_TYPE_TV_SERIES = "TV Series"

    IMDB_ID_REGEX = re.compile("www\.imdb\.com/title/(.+?)/")
    IMDB_LENGTH_REGEX = re.compile("itemprop=\"duration\".*?>(\d+) min<")
    IMDB_RATING_REGEX = re.compile("itemprop=\"contentRating\" content=\"(.+?)\"></span>")
    IMDB_TITLE_REGEX = re.compile("itemprop=\"name\">(.+?)</span>")  # not null
    IMDB_TV_EPISODE_REGEX = re.compile("\s+TV Episode\s+")
    IMDB_TV_SERIES_REGEX = re.compile("\s+TV Series\s+")

    # These regexes require the DOTALL flag
    IMDB_ASPECT_RATIO_REGEX = re.compile("<h4 class=\"inline\">Aspect Ratio:</h4>(.+?)<", re.DOTALL)
    IMDB_BUDGET_REGEX = re.compile("<h4 class=\"inline\">Budget:</h4>(.+?)<", re.DOTALL)
    IMDB_GROSS_REGEX = re.compile("<h4 class=\"inline\">Gross:</h4>(.+?)<", re.DOTALL)
    IMDB_PLOT_REGEX = re.compile("itemprop=\"description\">(.+?)<div", re.DOTALL)
    IMDB_POSTER_REGEX = re.compile("src=\"(.+?)\".*?itemprop=\"image\" />", re.DOTALL)
    IMDB_TAGLINE_REGEX = re.compile("Taglines:</h4>\n(.+?)\s*<", re.DOTALL)
    IMDB_YEAR_REGEX = re.compile("itemprop=\"name\".+?<a href=\"/year/(\d+)/", re.DOTALL)

    @classmethod
    def scrape_imdb_data(self, title):
        imdb_url = self.get_imdb_url_from_title(title)
        imdb_html = urllib.urlopen(imdb_url).read()

        # Type (not null)
        if self.IMDB_TV_EPISODE_REGEX.search(imdb_html):
            video_type = self.IMDB_TYPE_TV_EPISODE
        elif self.IMDB_TV_SERIES_REGEX.search(imdb_html):
            video_type = self.IMDB_TYPE_TV_SERIES
        else:
            video_type = self.IMDB_TYPE_MOVIE

        # These values cannot be null
        imdb_id = use_regex(self.IMDB_ID_REGEX, imdb_url, False)
        title = use_regex(self.IMDB_TITLE_REGEX, imdb_html, False)

        # Everything else (can be null)
        aspect_ratio_str = use_regex(self.IMDB_ASPECT_RATIO_REGEX, imdb_html, True)
        aspect_ratio = self.get_aspect_ratio_float_from_str(aspect_ratio_str)

        budget = use_regex(self.IMDB_BUDGET_REGEX, imdb_html, True)
        gross = use_regex(self.IMDB_GROSS_REGEX, imdb_html, True)
        imdb_poster_url = use_regex(self.IMDB_POSTER_REGEX, imdb_html, True)
        length = use_regex(self.IMDB_LENGTH_REGEX, imdb_html, True)
        plot = use_regex(self.IMDB_PLOT_REGEX, imdb_html, True)
        rating = use_regex(self.IMDB_RATING_REGEX, imdb_html, True)
        tagline = use_regex(self.IMDB_TAGLINE_REGEX, imdb_html, True)
        year = use_regex(self.IMDB_YEAR_REGEX, imdb_html, True)

        print aspect_ratio
        print budget
        print gross
        print imdb_id
        print imdb_poster_url
        print length
        print rating
        print tagline
        print title
        print video_type
        print year
        #print genre_list
        #print writer_list
        #print director_list
        #print actor_list
        print plot


    @classmethod
    def get_imdb_url_from_title(cls, title):
        return get_top_google_result_url(cls.IMDB_GOOGLE_QUERY_STRING % title)

    @classmethod
    def get_aspect_ratio_float_from_str(cls, aspect_ratio_str):
        width, height = aspect_ratio_str.split(' : ')
        trimmed_height = height.split(' ')[0]
        return float(width) / float(trimmed_height)


def use_regex(given_regex, target_str, can_be_null):
    match = given_regex.search(target_str)
    try:
        return_str = match.groups()[0].strip()
    except AttributeError:
        return_str = None
        if not can_be_null:
            print "Target regex '%s' not found--this value cannot be null" % given_regex
            raise
    return return_str


def get_top_google_result_url(search_string):
    google_search_results = pygoogle(search_string)
    google_search_results.pages = 1
    return google_search_results.get_urls()[0]


if __name__ == '__main__':
    ImdbScraper.scrape_imdb_data('Star Trek')