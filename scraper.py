#!/usr/bin/python

import urllib2
import re

from HTMLParser import HTMLParser
from pygoogle import pygoogle

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


class RogerEbertScraper:

    def __init__(self):
        return


class ImdbScraper:

    def __init__(self):
        return

    IMDB_BUDGET_URL = "http://www.imdb.com/title/%s/business"
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
    IMDB_BUDGET_REGEX = re.compile("<h5>Budget</h5>.*?(\$.+?)<", re.DOTALL)

    IMDB_GROSS_REGEX = re.compile("<h5>Gross</h5>.*?(\$.+?) \(USA\)", re.DOTALL)
    IMDB_PLOT_REGEX = re.compile("itemprop=\"description\">(.+?)<div", re.DOTALL)
    IMDB_POSTER_REGEX = re.compile("<meta property='og:image' content=\"(.+?)\" />", re.DOTALL)
    IMDB_TAGLINE_REGEX = re.compile("Taglines:</h4>\n(.+?)\s*<", re.DOTALL)

    IMDB_GENRE_STR_REGEX = re.compile("<h4 class=\"inline\">Genres?:</h4>(.+?)</div>", re.DOTALL)
    IMDB_GENRE_LIST_REGEX = re.compile("<a.*?> *(.+?) *<", re.DOTALL)

    IMDB_DIRECTOR_STR_REGEX = re.compile("<h4 class=\"inline\">Directors?:</h4>(.+?)</div>", re.DOTALL)
    IMDB_CREATOR_STR_REGEX = re.compile("<h4 class=\"inline\">Creators?:</h4>(.+?)</div>", re.DOTALL)
    IMDB_STAR_STR_REGEX = re.compile("<h4 class=\"inline\">Stars?:</h4>(.+?)</div>", re.DOTALL)
    IMDB_WRITER_STR_REGEX = re.compile("<h4 class=\"inline\">Writers?:</h4>(.+?)</div>", re.DOTALL)
    IMDB_NAME_LIST_REGEX = re.compile("itemprop=\"name\">(.+?)<")

    IMDB_YEAR_REGEX = re.compile("itemprop=\"name\".+?<a href=\"/year/(\d+)/", re.DOTALL)

    @classmethod
    def scrape_imdb_data(self, title):
        imdb_url = self.get_imdb_url_from_title(title)
        imdb_html = retrieve_html_from_url(imdb_url)

        # These values cannot be null
        imdb_id = use_regex(self.IMDB_ID_REGEX, imdb_url, False)
        title = use_regex(self.IMDB_TITLE_REGEX, imdb_html, False)
        video_type = self.determine_imdb_video_type(imdb_html)

        # Everything else (can be null)
        imdb_poster_url = use_regex(self.IMDB_POSTER_REGEX, imdb_html, True)
        length = use_regex(self.IMDB_LENGTH_REGEX, imdb_html, True)
        rating = use_regex(self.IMDB_RATING_REGEX, imdb_html, True)
        year = use_regex(self.IMDB_YEAR_REGEX, imdb_html, True)

        aspect_ratio_str = use_regex(self.IMDB_ASPECT_RATIO_REGEX, imdb_html, True)
        aspect_ratio = self.get_aspect_ratio_float_from_str(aspect_ratio_str)

        genre_str = use_regex(self.IMDB_GENRE_STR_REGEX, imdb_html, True)
        genre_list = self.IMDB_GENRE_LIST_REGEX.findall(genre_str)

        director_str = use_regex(self.IMDB_DIRECTOR_STR_REGEX, imdb_html, True)
        director_list = self.get_list_of_names(director_str)

        writer_str = use_regex(self.IMDB_WRITER_STR_REGEX, imdb_html, True)
        writer_list = self.get_list_of_names(writer_str)

        star_str = use_regex(self.IMDB_STAR_STR_REGEX, imdb_html, True)
        star_list = self.get_list_of_names(star_str)

        creator_str = use_regex(self.IMDB_CREATOR_STR_REGEX, imdb_html, True)
        creator_list = self.get_list_of_names(creator_str)

        plot_html = use_regex(self.IMDB_PLOT_REGEX, imdb_html, True)
        plot = remove_html_tags(plot_html)

        tagline_html = use_regex(self.IMDB_TAGLINE_REGEX, imdb_html, True)
        tagline = remove_html_tags(tagline_html)

        # Scrape IMDB budget page
        imdb_budget_url = self.IMDB_BUDGET_URL % imdb_id
        imdb_budget_html = retrieve_html_from_url(imdb_budget_url)

        gross = use_regex(self.IMDB_GROSS_REGEX, imdb_budget_html, True)
        budget = use_regex(self.IMDB_BUDGET_REGEX, imdb_budget_html, True)

        print "Aspect Ratio: %s" % aspect_ratio
        print "Budget: %s" % budget
        print "Gross: %s" % gross
        print "ID: %s " % imdb_id
        print "Poster URL: %s " % imdb_poster_url
        print "Length: %s" % length
        print "Rating: %s" % rating
        print "Tagline: %s" % tagline
        print "Title: %s" % title
        print "Video Type: %s" % video_type
        print "Year: %s" % year
        print "Genres: "
        print genre_list
        print "Writers: "
        print writer_list
        print "Directors: "
        print director_list
        print "Creators: "
        print creator_list
        print "Stars: "
        print star_list
        print "Plot: "
        print plot

    @classmethod
    def determine_imdb_video_type(cls, imdb_html):
        if cls.IMDB_TV_EPISODE_REGEX.search(imdb_html):
            video_type = cls.IMDB_TYPE_TV_EPISODE
        elif cls.IMDB_TV_SERIES_REGEX.search(imdb_html):
            video_type = cls.IMDB_TYPE_TV_SERIES
        else:
            video_type = cls.IMDB_TYPE_MOVIE
        return video_type

    @classmethod
    def get_list_of_names(cls, name_str):
        if name_str:
            name_list = cls.IMDB_NAME_LIST_REGEX.findall(name_str)
        else:
            name_list = None
        return name_list

    @classmethod
    def get_imdb_url_from_title(cls, title):
        return get_top_google_result_url(cls.IMDB_GOOGLE_QUERY_STRING % title)

    @classmethod
    def get_aspect_ratio_float_from_str(cls, aspect_ratio_str):
        width_height_regex = re.compile(".*?([0-9]*\.?[0-9]+).*?:.*?([0-9]*\.?[0-9]+).*?")
        width_height_match = width_height_regex.search(aspect_ratio_str)
        if width_height_match:
            (width, height) = width_height_match.groups()
            aspect_ratio = float(width) / float(height)
        else:
            aspect_ratio = None
        return aspect_ratio


def retrieve_html_from_url(url):
    spoofed_header = {
       'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': '``text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'
    }
    try:
        req = urllib2.Request(url, headers=spoofed_header)
        html = urllib2.urlopen(req).read()
    except AttributeError:
        print "ERROR: URL '%s' is not a valid IMDB page "% imdb_budget_url
        raise
    return html


def remove_html_tags(str):
    if str:
        s = MLStripper()
        s.feed(str)
        return_str = s.get_data()
    else:
        return_str = None
    return return_str

def use_regex(given_regex, target_str, can_be_null):
    match = given_regex.search(target_str)
    try:
        return_str = match.groups()[0].strip()
    except (AttributeError, IndexError):
        return_str = None
        if not can_be_null:
            print "ERROR: Target regex '%s' not found--this value cannot be null" % given_regex
            raise
    return return_str


def get_top_google_result_url(search_string):
    google_search_results = pygoogle(search_string)
    google_search_results.pages = 1
    try:
        return google_search_results.get_urls()[0]
    except (AttributeError, IndexError):
        print "ERROR: Search string '%s' not found on Google" % search_string
        raise


if __name__ == '__main__':
    ImdbScraper.scrape_imdb_data('Gliding Over All')