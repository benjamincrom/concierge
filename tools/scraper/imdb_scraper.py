#!/usr/bin/python


import html_manipulator
import re


IMDB_BUDGET_URL = "http://www.imdb.com/title/%s/business"
IMDB_GOOGLE_QUERY_STRING = "site:imdb.com %s %s"
IMDB_TYPE_MOVIE = "Movie"

IMDB_ID_REGEX = re.compile("www\.imdb\.com/title/(.+?)/")  # not null
IMDB_RATING_REGEX = re.compile("itemprop=\"contentRating\" content=\"(.+?)\"></span>")
IMDB_SCORE_REGEX = re.compile("<span itemprop=\"ratingValue\">([0-9]*\.?[0-9]+)</span>")
IMDB_TITLE_REGEX = re.compile("itemprop=\"name\">(.+?)</span>")  # not null
IMDB_WIDTH_HEIGHT_REGEX = re.compile(".*?([0-9]*\.?[0-9]+).*?:.*?([0-9]*\.?[0-9]+).*?")

IMDB_ASPECT_RATIO_REGEX = re.compile("<h4 class=\"inline\">Aspect Ratio:</h4>(.+?)<", re.DOTALL)
IMDB_BUDGET_REGEX = re.compile("<h5>Budget</h5>.*?(\$.+?)<", re.DOTALL)
IMDB_CREATOR_STR_REGEX = re.compile("<h4 class=\"inline\">Creators?:</h4>(.+?)</div>", re.DOTALL)
IMDB_DIRECTOR_STR_REGEX = re.compile("<h4 class=\"inline\">Directors?:</h4>(.+?)</div>", re.DOTALL)
IMDB_GENRE_LIST_REGEX = re.compile("<a.*?> *(.+?) *<", re.DOTALL)
IMDB_GENRE_STR_REGEX = re.compile("<h4 class=\"inline\">Genres?:</h4>(.+?)</div>", re.DOTALL)
IMDB_GROSS_REGEX = re.compile("<h5>Gross</h5>.*?(\$.+?) \(USA\)", re.DOTALL)
IMDB_LENGTH_REGEX = re.compile("itemprop=\"duration\".*?>.*?(\d+) min.*?<", re.DOTALL)
IMDB_NAME_LIST_REGEX = re.compile("itemprop=\"name\">(.+?)<", re.DOTALL)
IMDB_PLOT_REGEX = re.compile("itemprop=\"description\">(.+?)<div", re.DOTALL)
IMDB_POSTER_REGEX = re.compile("<meta property=\"og:image\" content=\"(.+?)\" />", re.DOTALL)
IMDB_STAR_STR_REGEX = re.compile("<h4 class=\"inline\">Stars?:</h4>(.+?)</div>", re.DOTALL)
IMDB_TAGLINE_REGEX = re.compile("Taglines:</h4>\n(.+?)\s*<", re.DOTALL)
IMDB_WRITER_STR_REGEX = re.compile("<h4 class=\"inline\">Writers?:</h4>(.+?)</div>", re.DOTALL)
IMDB_YEAR_REGEX = re.compile("itemprop=\"name\".+?<a href=\"/year/(\d+)/", re.DOTALL)


def scrape_imdb_data(search_title, year=""):
    """Return IMDB data for the given title and year in a dict"""
    return_dict = {}

    # Scrape IMDB page for this title
    imdb_url = html_manipulator.get_top_google_result_url(IMDB_GOOGLE_QUERY_STRING % (search_title, year))
    imdb_html = html_manipulator.retrieve_html_from_url(imdb_url)

    # These values cannot be null.  If they are null then return empty dict
    imdb_id = html_manipulator.use_regex(IMDB_ID_REGEX, imdb_url, True)
    title = html_manipulator.use_regex(IMDB_TITLE_REGEX, imdb_html, True)
    if imdb_id and title:
        title = title.replace("*", "")  # Remove stars from title
        video_type = IMDB_TYPE_MOVIE    # Set video type

        # Scrape IMDB budget page for this title
        imdb_budget_url = IMDB_BUDGET_URL % imdb_id
        imdb_budget_html = html_manipulator.retrieve_html_from_url(imdb_budget_url)

        gross = html_manipulator.use_regex(IMDB_GROSS_REGEX, imdb_budget_html, True)
        imdb_poster_url = html_manipulator.use_regex(IMDB_POSTER_REGEX, imdb_html, True)
        rating = html_manipulator.use_regex(IMDB_RATING_REGEX, imdb_html, True)
        budget = html_manipulator.use_regex(IMDB_BUDGET_REGEX, imdb_budget_html, True)

        score_str = html_manipulator.use_regex(IMDB_SCORE_REGEX, imdb_html, True)
        if score_str:
            score = float(score_str)/10.0
        else:
            score = ""

        aspect_ratio_str = html_manipulator.use_regex(IMDB_ASPECT_RATIO_REGEX, imdb_html, True)
        aspect_ratio = _get_aspect_ratio_float_from_str(aspect_ratio_str)

        genre_str = html_manipulator.use_regex(IMDB_GENRE_STR_REGEX, imdb_html, True)
        genre_list = IMDB_GENRE_LIST_REGEX.findall(genre_str)

        director_str = html_manipulator.use_regex(IMDB_DIRECTOR_STR_REGEX, imdb_html, True)
        director_list = _get_list_of_names(director_str)

        writer_str = html_manipulator.use_regex(IMDB_WRITER_STR_REGEX, imdb_html, True)
        writer_list = _get_list_of_names(writer_str)

        star_str = html_manipulator.use_regex(IMDB_STAR_STR_REGEX, imdb_html, True)
        star_list = _get_list_of_names(star_str)

        plot_html = html_manipulator.use_regex(IMDB_PLOT_REGEX, imdb_html, True)
        plot = html_manipulator.remove_html_tags(plot_html)

        tagline_html = html_manipulator.use_regex(IMDB_TAGLINE_REGEX, imdb_html, True)
        tagline = html_manipulator.remove_html_tags(tagline_html)

        year = html_manipulator.use_regex(IMDB_YEAR_REGEX, imdb_html, True)
        if year:
            year = int(year)

        length = html_manipulator.use_regex(IMDB_LENGTH_REGEX, imdb_html, True)
        if length:
            length = int(length)
        else:
            length = None

        # Dump values into dictionary
        return_dict = {
            "video_type":           video_type,
            "year":                 year,
            "title":                title,
            "tagline":              tagline,
            "rating":               rating,
            "score":                score,
            "length":               length,
            "imdb_poster_url":      imdb_poster_url,
            "imdb_id":              imdb_id,
            "budget":               budget,
            "plot":                 plot,
            "aspect_ratio":         aspect_ratio,
            "genre_list":           genre_list,
            "writer_list":          writer_list,
            "director_list":        director_list,
            "star_list":            star_list,
            "gross":                gross,
        }

    return return_dict


def _get_aspect_ratio_float_from_str(aspect_ratio_str):
    """Returns a float describing the aspect ratio given a text string describing the aspect ratio"""
    aspect_ratio = ""
    if aspect_ratio_str:
        width_height_match = IMDB_WIDTH_HEIGHT_REGEX.search(aspect_ratio_str)
        if width_height_match:
            (width, height) = width_height_match.groups()
            aspect_ratio = float(width) / float(height)
			
    return aspect_ratio


def _get_list_of_names(name_str):
    """Returns a python list of names given an IMDB HTML list of names"""
    if name_str:
        name_list = IMDB_NAME_LIST_REGEX.findall(name_str)
    else:
        name_list = ""

    return name_list
