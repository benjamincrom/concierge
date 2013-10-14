#!/usr/bin/python


import html_manipulator
import re


METACRITIC_QUERY_STRING = "site:metacritic.com %s %s - Metacritic"

METACRITIC_METASCORE_REGEX = re.compile(
    "<span class=\"score_value\" itemprop=\"ratingValue\">(\d+)</span>.*?"
    "<span class=\"based\">based on</span>.*?<span itemprop=\"reviewCount\">.*?"
    "(\d+).*?</span> Critics",
    re.DOTALL
)
METACRITIC_RELEASE_YEAR_REGEX = re.compile(
    "<span class=\"data\" itemprop=\"datePublished\">.*?(\d\d\d\d).*?</span>",
    re.DOTALL
)
METACRITIC_USERSCORE_REGEX = re.compile(
    "<div class=\"data avguserscore .*?\">.*?<span class=\"score_value\">([0-9]*\.?[0-9]+)</span>.*?"
    "<span class=\"score_total\">out of 10</span>.*?"
    "<span class=\"based\">based on</span> <strong>(\d+) Ratings",
    re.DOTALL
)


def scrape_metacritic(title, year='', season=''):
    """Scrape metacritic site for given title and year and return values in dict.

    Return values in dict if page exists.
    Return empty dict if page does not exists or does not match regex.
    """
    return_dict = {}
    metacritic_review_url = html_manipulator.get_top_google_result_url(METACRITIC_QUERY_STRING % (title, season))
    metacritic_review_html = html_manipulator.retrieve_html_from_url(metacritic_review_url)
    if metacritic_review_html and re.search(title, metacritic_review_html):
        # If this is not a TV season then scrape the year from the metacritic HTML
        if not season:
            metacritic_release_year_str = html_manipulator.use_regex(METACRITIC_RELEASE_YEAR_REGEX,
                                                                     metacritic_review_html,
                                                                     True)
            if metacritic_release_year_str:
                metacritic_release_year = int(metacritic_release_year_str)
            else:
                metacritic_release_year = None

        # Allow for a range of years (+/- 2) to correct for error
        if year:
            year_list = range(int(year) - 2, int(year) + 3)
        else:
            year_list = []

        # Return values only if the movie release year matches the metacritic release year or if title is a TV Season
        if season or metacritic_release_year in year_list:
            metacritic_metascore_match = METACRITIC_METASCORE_REGEX.search(metacritic_review_html)
            if metacritic_metascore_match:
                return_dict["metacritic_metascore_meter"] = float(metacritic_metascore_match.groups()[0]) / 100.0
                return_dict["metacritic_metascore_total"] = int(metacritic_metascore_match.groups()[1])

            metacritic_userscore_match = METACRITIC_USERSCORE_REGEX.search(metacritic_review_html)
            if metacritic_userscore_match:
                return_dict["metacritic_userscore_meter"] = float(metacritic_userscore_match.groups()[0]) / 10.0
                return_dict["metacritic_userscore_total"] = int(metacritic_userscore_match.groups()[1])

    return return_dict
