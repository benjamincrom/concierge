#!/usr/bin/python


import html_manipulator
import re


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
IMDB_TV_TITLE_SEASON_EPISODE_REGEX = re.compile("<h2 class=\"tv_header\">.*?<a href=.*?> *(.+?) *</a>:.*?"
                                                "<span class=\"nobr\">Season (\d+), Episode (\d+).+?</span>",
                                                re.DOTALL)
IMDB_WIDTH_HEIGHT_REGEX = re.compile(".*?([0-9]*\.?[0-9]+).*?:.*?([0-9]*\.?[0-9]+).*?")
IMDB_WRITER_STR_REGEX = re.compile("<h4 class=\"inline\">Writers?:</h4>(.+?)</div>", re.DOTALL)
IMDB_YEAR_REGEX = re.compile("itemprop=\"name\".+?<a href=\"/year/(\d+)/", re.DOTALL)


def scrape_imdb_data(title):
    # Scrape IMDB page for this title
    imdb_url = html_manipulator.get_top_google_result_url(IMDB_GOOGLE_QUERY_STRING % title)
    imdb_html = html_manipulator.retrieve_html_from_url(imdb_url)

    # These values cannot be null
    imdb_id = html_manipulator.use_regex(IMDB_ID_REGEX, imdb_url, False)
    title = html_manipulator.use_regex(IMDB_TITLE_REGEX, imdb_html, False)
    video_type = _determine_imdb_video_type(imdb_html)

    # Scrape IMDB budget page for this title
    imdb_budget_url = IMDB_BUDGET_URL % imdb_id
    imdb_budget_html = html_manipulator.retrieve_html_from_url(imdb_budget_url)

    # TV Episodes exclusively have show title, episode, season
    if video_type == IMDB_TYPE_TV_EPISODE:
        title_season_episode_match = IMDB_TV_TITLE_SEASON_EPISODE_REGEX.search(imdb_html)
        if title_season_episode_match:
            (show_title, season, episode) = title_season_episode_match.groups()
        else:
            show_title = None
            season = None
            episode = None
    # TV Series exclusively have creators
    elif video_type == IMDB_TYPE_TV_SERIES:
        creator_str = html_manipulator.use_regex(IMDB_CREATOR_STR_REGEX, imdb_html, True)
        creator_list = _get_list_of_names(creator_str)
    # Movies exclusively have gross
    elif video_type == IMDB_TYPE_MOVIE:
        gross = html_manipulator.use_regex(IMDB_GROSS_REGEX, imdb_budget_html, True)
    else:
        raise Exception(IMDB_INVALID_TYPE_ERROR % title)

    imdb_poster_url = html_manipulator.use_regex(IMDB_POSTER_REGEX, imdb_html, True)
    length = html_manipulator.use_regex(IMDB_LENGTH_REGEX, imdb_html, True)
    rating = html_manipulator.use_regex(IMDB_RATING_REGEX, imdb_html, True)
    budget = html_manipulator.use_regex(IMDB_BUDGET_REGEX, imdb_budget_html, True)

    aspect_ratio_str = html_manipulator.use_regex(IMDB_ASPECT_RATIO_REGEX, imdb_html, True)
    aspect_ratio = _get_aspect_ratio_float_from_str(aspect_ratio_str)

    genre_str = html_manipulator.use_regex(IMDB_GENRE_STR_REGEX, imdb_html, True)
    genre_list = IMDB_GENRE_LIST_REGEX.findall(genre_str)

    year = html_manipulator.use_regex(IMDB_YEAR_REGEX, imdb_html, True)
    if year: year = int(year)  # if year is not null then make it an int

    director_str = html_manipulator.use_regex(IMDB_DIRECTOR_STR_REGEX, imdb_html, True)
    director_list = _get_list_of_names(director_str)

    writer_str = html_manipulator.use_regex(IMDB_WRITER_STR_REGEX, imdb_html, True)
    writer_list = _get_list_of_names(writer_str)

    star_str = html_manipulator.use_regex(IMDB_STAR_STR_REGEX, imdb_html, True)
    star_list = _get_list_of_names(star_str)

    plot_html = html_manipulator.use_regex(IMDB_PLOT_REGEX, imdb_html, True)
    plot = html_manipulator.remove_html_tags(plot_html).strip()

    tagline_html = html_manipulator.use_regex(IMDB_TAGLINE_REGEX, imdb_html, True)
    tagline = html_manipulator.remove_html_tags(tagline_html)

    # Dump values into dictionary
    return_dict = {}
    if video_type == IMDB_TYPE_TV_EPISODE:
        return_dict["season"] = season
        return_dict["episode"] = episode
        return_dict["show_title"] = show_title
    elif video_type == IMDB_TYPE_TV_SERIES:
        return_dict["creator_list"] = creator_list
    elif video_type == IMDB_TYPE_MOVIE:
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
    return_dict["aspect_ratio"] = aspect_ratio
    return_dict["genre_list"] = genre_list
    return_dict["writer_list"] = writer_list
    return_dict["director_list"] = director_list
    return_dict["star_list"] = star_list
    return return_dict


def _determine_imdb_video_type(imdb_html):
    if IMDB_TV_EPISODE_REGEX.search(imdb_html):
        video_type = IMDB_TYPE_TV_EPISODE
    elif IMDB_TV_SERIES_REGEX.search(imdb_html):
        video_type = IMDB_TYPE_TV_SERIES
    else:
        video_type = IMDB_TYPE_MOVIE
    return video_type


def _get_aspect_ratio_float_from_str(aspect_ratio_str):
    aspect_ratio = None
    if aspect_ratio_str:
        width_height_match = IMDB_WIDTH_HEIGHT_REGEX.search(aspect_ratio_str)
        if width_height_match:
            (width, height) = width_height_match.groups()
            aspect_ratio = float(width) / float(height)
    return aspect_ratio


def _get_list_of_names(name_str):
    if name_str:
        name_list = IMDB_NAME_LIST_REGEX.findall(name_str)
    else:
        name_list = None
    return name_list