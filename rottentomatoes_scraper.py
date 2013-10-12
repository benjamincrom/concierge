#!/usr/bin/python


import locale
import html_manipulator
import re


ROTTENTOMATOES_QUERY_STRING = "site:rottentomatoes.com %s"

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
    rottentomatoes_review_url = html_manipulator.get_top_google_result_url(ROTTENTOMATOES_QUERY_STRING % title)
    rottentomatoes_review_html = html_manipulator.retrieve_html_from_url(rottentomatoes_review_url)

    if re.search(title, rottentomatoes_review_html):
        return_dict = {}
        rottentomatoes_year = int(html_manipulator.use_regex(ROTTENTOMATOES_YEAR_REGEX, rottentomatoes_review_html, False))
        if rottentomatoes_year == year:
            rottentomatoes_all_critics_match = ROTTENTOMATOES_ALL_CRITICS_REGEX.search(rottentomatoes_review_html)
            if rottentomatoes_all_critics_match:
                return_dict["all_critics_meter"] = float(rottentomatoes_all_critics_match.groups()[0]) / 100.0
                return_dict["all_critics_avg_score"] = float(rottentomatoes_all_critics_match.groups()[1]) / 10.0
                return_dict["all_critics_total"] = int(rottentomatoes_all_critics_match.groups()[2])
                return_dict["all_critics_fresh"] = int(rottentomatoes_all_critics_match.groups()[3])
                return_dict["all_critics_rotten"] = int(rottentomatoes_all_critics_match.groups()[4])

            rottentomatoes_top_critics_match = ROTTENTOMATOES_TOP_CRITICS_REGEX.search(rottentomatoes_review_html)
            if rottentomatoes_top_critics_match:
                return_dict["top_critics_meter"] = float(rottentomatoes_top_critics_match.groups()[0]) / 100.0
                return_dict["top_critics_avg_score"] = float(rottentomatoes_top_critics_match.groups()[1]) / 10.0
                return_dict["top_critics_total"] = int(rottentomatoes_top_critics_match.groups()[2])
                return_dict["top_critics_fresh"] = int(rottentomatoes_top_critics_match.groups()[3])
                return_dict["top_critics_rotten"] = int(rottentomatoes_top_critics_match.groups()[4])

            rottentomatoes_audience_match = ROTTENTOMATOES_AUDIENCE_REGEX.search(rottentomatoes_review_html)
            if rottentomatoes_audience_match:
                return_dict["audience_meter"] = float(rottentomatoes_audience_match.groups()[0]) / 100.0
                return_dict["audience_avg_score"] = float(rottentomatoes_audience_match.groups()[1]) / 5.0

                locale.setlocale(locale.LC_ALL, 'en_US.UTF8')
                return_dict["audience_total"] = locale.atoi(rottentomatoes_audience_match.groups()[2])

    else:
        return_dict = None

    return return_dict
