#!/usr/bin/python


import re

import html_manipulator


ROTTENTOMATOES_QUERY_STRING = "site:rottentomatoes.com %s (%s)"

ROTTENTOMATOES_ALL_CRITICS_REGEX = re.compile(
    "<span itemprop=\"ratingValue\" id=\"all-critics-meter\".*?"
    "class=\"meter .*? numeric .*?\">(\d+)</span>.*?"
    "<meta itemprop=\"name\" content=\"Tomatometer Score\" />.*?"
    "<p class=\"critic_stats\">.*?"
    "Average Rating: <span>([0-9]*\.?[0-9]+)/10</span><br />.*?"
    "Reviews Counted: <span itemprop=\"reviewCount\">(\d+)</span><br />.*?"
    "Fresh: (\d+) \| Rotten: (\d+).*?</p>",
    re.DOTALL
)
ROTTENTOMATOES_TOP_CRITICS_REGEX = re.compile(
    "<span id=\"all-critics-meter\" class=\"meter .*? numeric .*?\">(\d+)</span>.*?"
    "<p class=\"critic_stats\">.*?Average Rating: <span>([0-9]*\.?[0-9]+)/10</span><br />.*?"
    "Critic Reviews: (\d+)<br />.*?Fresh: (\d+) \| Rotten: (\d+)</p>.*?</div>",
    re.DOTALL
)
ROTTENTOMATOES_AUDIENCE_REGEX = re.compile(
    "<span class=\"meter .*? numeric .*?\">(\d+)</span>.*?"
    "<p class=\"critic_stats\">.*?<span class=\"subText liked_it\" >liked it</span><br/>.*?"
    "Average Rating: ([0-9]*\.?[0-9]+)/5<br/>.*?User Ratings: ([\d+,]*\d+).*?</p>",
    re.DOTALL
)
ROTTENTOMATOES_YEAR_REGEX = re.compile("<span itemprop=\"name\">.*?\((\d\d\d\d)\)</span>")


def scrape_rottentomatoes(title, year):
    """Scrape rottentomatoes stats for a given title and year and return values in a dict.

    Return empty dict if page is not found or does not match regex.
    """
    return_dict = {}
    rottentomatoes_review_url = html_manipulator.get_top_google_result_url(ROTTENTOMATOES_QUERY_STRING % (title, year))
    rottentomatoes_review_html = html_manipulator.retrieve_html_from_url(rottentomatoes_review_url)
    if rottentomatoes_review_html and re.search(title, rottentomatoes_review_html):
        rottentomatoes_year_str = html_manipulator.use_regex(ROTTENTOMATOES_YEAR_REGEX, rottentomatoes_review_html, 
                                                             True)
        # Allow for a range of years (+/- 2) to correct for error
        if rottentomatoes_year_str:
            rottentomatoes_year = int(rottentomatoes_year_str)
            rottentomatoes_year_list = range(rottentomatoes_year - 2, rottentomatoes_year + 3)
        else:
            rottentomatoes_year_list = []

        if year in rottentomatoes_year_list:
            rottentomatoes_all_critics_match = ROTTENTOMATOES_ALL_CRITICS_REGEX.search(rottentomatoes_review_html)
            if rottentomatoes_all_critics_match:
                return_dict["all_critics_meter"] = float(rottentomatoes_all_critics_match.group(1)) / 100.0
                return_dict["all_critics_avg_score"] = float(rottentomatoes_all_critics_match.group(2)) / 10.0
                return_dict["all_critics_total"] = int(rottentomatoes_all_critics_match.group(3))
                return_dict["all_critics_fresh"] = int(rottentomatoes_all_critics_match.group(4))
                return_dict["all_critics_rotten"] = int(rottentomatoes_all_critics_match.group(5))

            rottentomatoes_top_critics_match = ROTTENTOMATOES_TOP_CRITICS_REGEX.search(rottentomatoes_review_html)
            if rottentomatoes_top_critics_match:
                return_dict["top_critics_meter"] = float(rottentomatoes_top_critics_match.group(1)) / 100.0
                return_dict["top_critics_avg_score"] = float(rottentomatoes_top_critics_match.group(2)) / 10.0
                return_dict["top_critics_total"] = int(rottentomatoes_top_critics_match.group(3))
                return_dict["top_critics_fresh"] = int(rottentomatoes_top_critics_match.group(4))
                return_dict["top_critics_rotten"] = int(rottentomatoes_top_critics_match.group(5))

            rottentomatoes_audience_match = ROTTENTOMATOES_AUDIENCE_REGEX.search(rottentomatoes_review_html)
            if rottentomatoes_audience_match:
                return_dict["audience_meter"] = float(rottentomatoes_audience_match.group(1)) / 100.0
                return_dict["audience_avg_score"] = float(rottentomatoes_audience_match.group(2)) / 5.0
                return_dict["audience_total"] = int(rottentomatoes_audience_match.group(3).replace(",", ""))

    return return_dict
