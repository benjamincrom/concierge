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
    IMDB_TITLE_NOT_FOUND_ERROR = "IMDB title '%s' not found"
    IMDB_TYPE_TV_SERIES = "TV Series"
    IMDB_TYPE_TV_EPISODE = "TV Episode"
    IMDB_TYPE_MOVIE = "Movie"

    IMDB_TITLE_REGEX = re.compile("itemprop=\"name\">(.+?)</span>")  # not null
    IMDB_YEAR_REGEX = re.compile("itemprop=\"contentRating\" content=\"(.*?)\"")
    IMDB_LENGTH_REGEX = re.compile("itemprop=\"duration\".*?>(\d+) min<")
    IMDB_TV_SERIES:BytesWarning_REGEX = re.compile("\s+TV Episode\s+")
    IMDB_TV_EPISODE_REGEX = re.compile("\s+TV Episode\s+")

    IMDB_RATING_REGEX = re.compile("itemprop=\"contentRating\" content=\"(.+?)\"></span>")
    IMDB_TAGLINE_REGEX = re.compile("Taglines:</h4>\n(.+?)\s*<", re.DOTALL)
    IMDB_ID_REGEX = re.compile("www\.imdb\.com/title/(.+?)/")

    @classmethod
    def scrape_imdb_data(self, title):
        imdb_url = self.get_imdb_url_from_title(title)
        imdb_html = urllib.urlopen(imdb_url).read()

        # Title (not null)
        title_match = self.IMDB_TITLE_REGEX.search(imdb_html)
        try:
            title = title_match.groups()[0]
        except AttributeError:
            print self.IMDB_TITLE_NOT_FOUND_ERROR % title

        # Type (not null)
        if ind(self.IMDB_TYPE_TV_EPISODE) != -1:
            video_type = self.IMDB_TYPE_TV_EPISODE
        elif imdb_html.find(self.IMDB_TYPE_TV_SERIES) != -1:
            video_type = self.IMDB_TYPE_TV_SERIES
        else:
            video_type = self.IMDB_TYPE_MOVIE

        # Year
        year_match = self.IMDB_YEAR_REGEX.search(imdb_html)
        if year_match: year = year_match.groups()[0]
        else: year = None

        # Length
        length_match = self.IMDB_LENGTH_REGEX.search(imdb_html)
        if length_match: length = length_match.groups()[0]
        else: length = None


        print title
        print video_type
        print year
        print length




    @classmethod
    def get_imdb_url_from_title(cls, title):
        return get_top_google_result_url(cls.IMDB_GOOGLE_QUERY_STRING % title)

    @classmethod
    def get_aspect_ratio_float_from_str(cls, aspect_ratio_str):
        width, height = aspect_ratio_str.split(' : ')
        trimmed_height = height.split(' ')[0]
        return float(width) / float(trimmed_height)


def get_top_google_result_url(search_string):
    google_search_results = pygoogle(search_string)
    google_search_results.pages = 1
    return google_search_results.get_urls()[0]


if __name__ == '__main__':
    ImdbScraper.scrape_imdb_data('Two Cathedrals')