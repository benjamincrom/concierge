#!/usr/bin/python

import re
import urllib2

from datetime import datetime
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


class RogerEbertScraper:
    LOCAL_LINK_PREFIX = '<a href="'
    EBERT_LINK_PREFIX = '<a href="http://www.rogerebert.com'
    EBERT_FULL_STAR = 'icon-star-full'
    EBERT_GOOGLE_QUERY_STRING = "rogerebert.com %s"
    EBERT_HALF_STAR = 'icon-star-half'
    EBERT_REVIEW_NOT_FOUND = "There is no review on rogerebert.com for this title: %s"
    EBERT_REVIEW_URL = "http://www.rogerebert.com/reviews/%s"
    EBERT_SITE_TITLE = "RogerEbert.com"
    EBERT_URL_DELIMITER = '-'

    EBERT_REVIEW_REGEX = re.compile('<div itemprop="reviewBody">(.+?)</div>', re.DOTALL)
    EBERT_AUTHOR_REGEX = re.compile('<meta content="(.+?)" name="author">')
    EBERT_DATE_REGEX = re.compile('itemprop="datePublished">(.+?)</time>')
    EBERT_STARS_REGEX = re.compile('itemprop="reviewRating"(.+?)</span>', re.DOTALL)

    @classmethod
    def set_rogerebert_data(cls, title):
        return_dict = None
        ebert_review_url = cls.get_ebert_url_from_title(title)
        ebert_review_html = urllib2.urlopen(ebert_review_url).read()
        review_text_match = cls.EBERT_REVIEW_REGEX.search(ebert_review_html)
        if review_text_match:
            review_text = review_text_match.groups()[0]
            review_unicode_text = cls.format_ebert_review_text(review_text)
            formatted_review_text = ''.join([x for x in review_unicode_text if ord(x) < 128])  # Remove unicode chars

            review_author_match = cls.EBERT_AUTHOR_REGEX.search(ebert_review_html)
            review_author = review_author_match.groups()[0]

            review_date_match = cls.EBERT_DATE_REGEX.search(ebert_review_html)
            review_date_string = review_date_match.groups()[0]
            review_datetime = datetime.strptime(review_date_string, '%B %d, %Y')
            review_date = review_datetime.date()

            review_stars_match = cls.EBERT_STARS_REGEX.search(ebert_review_html)
            review_stars_string = review_stars_match.groups()[0]
            review_percent_score = cls.compute_ebert_percent_score(review_stars_string)

            return_dict = {}
            return_dict["formatted_review_text"] = formatted_review_text
            return_dict["review_author"] = review_author
            return_dict["review_source"] = cls.EBERT_SITE_TITLE
            return_dict["review_date"] = review_date.strftime("%Y-%m-%d")
            return_dict["review_percent_score"] = review_percent_score

        return return_dict

    @classmethod
    def get_ebert_url_from_title(cls, title):
        return ManipulateHTML.get_top_google_result_url(cls.EBERT_GOOGLE_QUERY_STRING % title)

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
        lowercase_title = title.lower()
        title_str = lowercase_title.replace(' ', cls.EBERT_URL_DELIMITER)
        url_formatted_title = "%s-%s" %(title_str, year)
        ebert_review_url = cls.EBERT_REVIEW_URL %(url_formatted_title)
        return ebert_review_url


class ImdbScraper:
    IMDB_BUDGET_URL = "http://www.imdb.com/title/%s/business"
    IMDB_GOOGLE_QUERY_STRING = "imdb %s"
    IMDB_INVALID_TYPE_ERROR = "Invalid video type for title '%s'"
    IMDB_TYPE_MOVIE = "Movie"
    IMDB_TYPE_TV_EPISODE = "TV Episode"
    IMDB_TYPE_TV_SERIES = "TV Series"

    IMDB_ID_REGEX = re.compile("www\.imdb\.com/title/(.+?)/")  # not null
    IMDB_LENGTH_REGEX = re.compile("itemprop=\"duration\".*?>(\d+) min<")
    IMDB_RATING_REGEX = re.compile("itemprop=\"contentRating\" content=\"(.+?)\"></span>")
    IMDB_TITLE_REGEX = re.compile("itemprop=\"name\">(.+?)</span>")  # not null
    IMDB_TV_EPISODE_REGEX = re.compile("\s+TV Episode\s+")
    IMDB_TV_SERIES_REGEX = re.compile("\s+TV Series\s+")

    # These regexes require the DOTALL flag
    IMDB_ASPECT_RATIO_REGEX = re.compile("<h4 class=\"inline\">Aspect Ratio:</h4>(.+?)<", re.DOTALL)
    IMDB_BUDGET_REGEX = re.compile("<h5>Budget</h5>.*?(\$.+?)<", re.DOTALL)
    IMDB_CREATOR_STR_REGEX = re.compile("<h4 class=\"inline\">Creators?:</h4>(.+?)</div>", re.DOTALL)
    IMDB_DIRECTOR_STR_REGEX = re.compile("<h4 class=\"inline\">Directors?:</h4>(.+?)</div>", re.DOTALL)
    IMDB_GENRE_LIST_REGEX = re.compile("<a.*?> *(.+?) *<", re.DOTALL)
    IMDB_GENRE_STR_REGEX = re.compile("<h4 class=\"inline\">Genres?:</h4>(.+?)</div>", re.DOTALL)
    IMDB_GROSS_REGEX = re.compile("<h5>Gross</h5>.*?(\$.+?) \(USA\)", re.DOTALL)
    IMDB_NAME_LIST_REGEX = re.compile("itemprop=\"name\">(.+?)<", re.DOTALL)
    IMDB_PLOT_REGEX = re.compile("itemprop=\"description\">(.+?)<div", re.DOTALL)
    IMDB_POSTER_REGEX = re.compile("<meta property='og:image' content=\"(.+?)\" />", re.DOTALL)
    IMDB_STAR_STR_REGEX = re.compile("<h4 class=\"inline\">Stars?:</h4>(.+?)</div>", re.DOTALL)
    IMDB_TAGLINE_REGEX = re.compile("Taglines:</h4>\n(.+?)\s*<", re.DOTALL)
    IMDB_TV_SEASON_AND_EPISODE_REGEX = re.compile("<span class=\"nobr\">Season (\d+), Episode (\d+).+?</span>",
                                                  re.DOTALL)
    IMDB_WIDTH_HEIGHT_REGEX = re.compile(".*?([0-9]*\.?[0-9]+).*?:.*?([0-9]*\.?[0-9]+).*?")
    IMDB_WRITER_STR_REGEX = re.compile("<h4 class=\"inline\">Writers?:</h4>(.+?)</div>", re.DOTALL)
    IMDB_YEAR_REGEX = re.compile("itemprop=\"name\".+?<a href=\"/year/(\d+)/", re.DOTALL)

    @classmethod
    def scrape_imdb_data(self, title):
        # Scrape IMDB page for this title
        imdb_url = self.get_imdb_url_from_title(title)
        imdb_html = ManipulateHTML.retrieve_html_from_url(imdb_url)

        # These values cannot be null
        imdb_id = ManipulateHTML.use_regex(self.IMDB_ID_REGEX, imdb_url, False)
        title = ManipulateHTML.use_regex(self.IMDB_TITLE_REGEX, imdb_html, False)
        video_type = self.determine_imdb_video_type(imdb_html)

        # Scrape IMDB budget page for this title
        imdb_budget_url = self.IMDB_BUDGET_URL % imdb_id
        imdb_budget_html = ManipulateHTML.retrieve_html_from_url(imdb_budget_url)

        # TV Episodes exclusively have episode, season
        if video_type == self.IMDB_TYPE_TV_EPISODE:
            season_and_episode_match = self.IMDB_TV_SEASON_AND_EPISODE_REGEX.search(imdb_html)
            if season_and_episode_match:
                (season, episode) = season_and_episode_match.groups()
            else:
                season = None
                episode = None
        # TV Series exclusively have creators
        elif video_type == self.IMDB_TYPE_TV_SERIES:
            creator_str = ManipulateHTML.use_regex(self.IMDB_CREATOR_STR_REGEX, imdb_html, True)
            creator_list = self.get_list_of_names(creator_str)
        # Movies exclusively have gross
        elif video_type == self.IMDB_TYPE_MOVIE:
            gross = ManipulateHTML.use_regex(self.IMDB_GROSS_REGEX, imdb_budget_html, True)
        else:
            raise Exception(self.IMDB_INVALID_TYPE_ERROR % title)

        imdb_poster_url = ManipulateHTML.use_regex(self.IMDB_POSTER_REGEX, imdb_html, True)
        length = ManipulateHTML.use_regex(self.IMDB_LENGTH_REGEX, imdb_html, True)
        rating = ManipulateHTML.use_regex(self.IMDB_RATING_REGEX, imdb_html, True)
        year = int(ManipulateHTML.use_regex(self.IMDB_YEAR_REGEX, imdb_html, True))
        budget = ManipulateHTML.use_regex(self.IMDB_BUDGET_REGEX, imdb_budget_html, True)

        aspect_ratio_str = ManipulateHTML.use_regex(self.IMDB_ASPECT_RATIO_REGEX, imdb_html, True)
        aspect_ratio = self.get_aspect_ratio_float_from_str(aspect_ratio_str)

        genre_str = ManipulateHTML.use_regex(self.IMDB_GENRE_STR_REGEX, imdb_html, True)
        genre_list = self.IMDB_GENRE_LIST_REGEX.findall(genre_str)

        director_str = ManipulateHTML.use_regex(self.IMDB_DIRECTOR_STR_REGEX, imdb_html, True)
        director_list = self.get_list_of_names(director_str)

        writer_str = ManipulateHTML.use_regex(self.IMDB_WRITER_STR_REGEX, imdb_html, True)
        writer_list = self.get_list_of_names(writer_str)

        star_str = ManipulateHTML.use_regex(self.IMDB_STAR_STR_REGEX, imdb_html, True)
        star_list = self.get_list_of_names(star_str)

        plot_html = ManipulateHTML.use_regex(self.IMDB_PLOT_REGEX, imdb_html, True)
        plot = ManipulateHTML.remove_html_tags(plot_html).strip()

        tagline_html = ManipulateHTML.use_regex(self.IMDB_TAGLINE_REGEX, imdb_html, True)
        tagline = ManipulateHTML.remove_html_tags(tagline_html)

        # Dump values into dictionary
        return_dict = {}
        if video_type == self.IMDB_TYPE_TV_EPISODE:
            return_dict["season"] = season
            return_dict["episode"] = episode
        elif video_type == self.IMDB_TYPE_TV_SERIES:
            return_dict["creator_list"] = creator_list
        elif video_type == self.IMDB_TYPE_MOVIE:
            return_dict["gross"] = gross

        return_dict["video_type"] = video_type
        return_dict["year"] = year
        return_dict["title"] = title
        return_dict["tagline"] = tagline
        return_dict["rating"] = rating
        return_dict["length"] = length
        return_dict["imdb_poster_url"] = imdb_poster_url
        return_dict["imdb_id"] = imdb_id
        return_dict["budget"] = budget
        return_dict["plot"] = plot
        return_dict["genre_list"] = genre_list
        return_dict["writer_list"] = writer_list
        return_dict["director_list"] = director_list
        return_dict["star_list"] = star_list
        return return_dict

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
        return ManipulateHTML.get_top_google_result_url(cls.IMDB_GOOGLE_QUERY_STRING % title)

    @classmethod
    def get_aspect_ratio_float_from_str(cls, aspect_ratio_str):
        width_height_match = cls.IMDB_WIDTH_HEIGHT_REGEX.search(aspect_ratio_str)
        if width_height_match:
            (width, height) = width_height_match.groups()
            aspect_ratio = float(width) / float(height)
        else:
            aspect_ratio = None
        return aspect_ratio

class ManipulateHTML:
    SPOOFED_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': '``text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }
    GOOGLE_REGEX = re.compile("<h2 class=\"hd\">Search Results.*?<a href=\"(.+?)\"", re.DOTALL)

    @classmethod
    def retrieve_html_from_url(cls, url):
        try:
            req = urllib2.Request(url, headers=cls.SPOOFED_HEADERS)
            html = urllib2.urlopen(req).read()
        except AttributeError:
            print "ERROR: URL '%s' is not a valid IMDB page " % url
            raise
        return html

    @classmethod
    def remove_html_tags(cls, str):
        if str:
            s = MLStripper()
            s.feed(str)
            return_str = s.get_data()
        else:
            return_str = None
        return return_str

    @classmethod
    def use_regex(cls, given_regex, target_str, can_be_null):
        match = given_regex.search(target_str)
        try:
            return_str = str(match.groups()[0]).strip()
        except (AttributeError, IndexError):
            return_str = None
            if not can_be_null:
                print "ERROR: Target regex '%s' not found--this value cannot be null" % given_regex
                raise
        return return_str

    @classmethod
    def get_top_google_result_url(cls, search_string):
        formatted_search_string = search_string.replace(' ', '+')
        html = cls.retrieve_html_from_url("http://www.google.com/search?q=%s" % formatted_search_string)
        return cls.use_regex(cls.GOOGLE_REGEX, html, False)

if __name__ == '__main__':
    imdb_title_obj_dict = ImdbScraper.scrape_imdb_data('Terminator 2')
    print imdb_title_obj_dict

    if imdb_title_obj_dict["video_type"] == "Movie":
        rogerebert_obj_dict = RogerEbertScraper.set_rogerebert_data(imdb_title_obj_dict["title"])
        print rogerebert_obj_dict
        # f = open('test.html', 'w')
        # f.write(rogerebert_obj_dict["formatted_review_text"])
        # f.close()