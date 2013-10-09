#!/usr/bin/python

import html_manipulator
import re

METACRITIC_QUERY_STRING = "site:metacritic.com %s %s Reviews"

METACRITIC_METASCORE_REGEX = re.compile(
    "<span class=\"score_value\" itemprop=\"ratingValue\">(\d+)</span>.*?"
    "<span class=\"based\">based on</span>.*?<span itemprop=\"reviewCount\">.*?"
    "(\d+).*?</span> Critics",
    re.DOTALL
)
METACRITIC_USERSCORE_REGEX = re.compile(
    "<div class=\"data avguserscore .*?\">.*?<span class=\"score_value\">([0-9]*\.?[0-9]+)</span>.*?"
    "<span class=\"score_total\">out of 10</span>.*?"
    "<span class=\"based\">based on</span> <strong>(\d+) Ratings",
    re.DOTALL
)

def scrape_metacritic(title, year, type):
    metacritic_review_url = html_manipulator.get_top_google_result_url(METACRITIC_QUERY_STRING %(title, year))
    metacritic_review_html = html_manipulator.retrieve_html_from_url(metacritic_review_url)

    if re.search(title, metacritic_review_html):
        return_dict = {}
        metacritic_metascore_match = METACRITIC_METASCORE_REGEX.search(metacritic_review_html)
        if metacritic_metascore_match:
            return_dict["metacritic_metascore_meter"] = float(metacritic_metascore_match.groups()[0]) / 100.0
            return_dict["metacritic_metascore_total"] = int(metacritic_metascore_match.groups()[1])

        metacritic_userscore_match = METACRITIC_USERSCORE_REGEX.search(metacritic_review_html)
        if metacritic_userscore_match:
            return_dict["metacritic_userscore_meter"] = float(metacritic_userscore_match.groups()[0]) / 10.0
            return_dict["metacritic_userscore_total"] = int(metacritic_userscore_match.groups()[1])

    else:
        return_dict = None

    return return_dict

