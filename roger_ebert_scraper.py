#!/usr/bin/python


import html_manipulator
import re

from datetime import datetime


LOCAL_LINK_PREFIX = '<a href="'
EBERT_LINK_PREFIX = '<a href="http://www.rogerebert.com'
EBERT_FULL_STAR = 'icon-star-full'
EBERT_GOOGLE_QUERY_STRING = "rogerebert.com %s %s"
EBERT_HALF_STAR = 'icon-star-half'
EBERT_REVIEW_NOT_FOUND = "There is no review on rogerebert.com for this title: %s"
EBERT_REVIEW_URL = "http://www.rogerebert.com/reviews/%s"
EBERT_SITE_TITLE = "RogerEbert.com"
EBERT_URL_DELIMITER = '-'

EBERT_AUTHOR_REGEX = re.compile('<meta content="(.+?)" name="author">')
EBERT_DATE_REGEX = re.compile('itemprop="datePublished">(.+?)</time>')

EBERT_REVIEW_REGEX = re.compile('<div itemprop="reviewBody">(.+?)</div>', re.DOTALL)
EBERT_STARS_REGEX = re.compile('itemprop="reviewRating"(.+?)</span>', re.DOTALL)


def scrape_rogerebert_data(title, year):
    return_dict = None
    ebert_review_url = html_manipulator.get_top_google_result_url(EBERT_GOOGLE_QUERY_STRING %(title, year))
    ebert_review_html = html_manipulator.retrieve_html_from_url(ebert_review_url)
    review_text_match = EBERT_REVIEW_REGEX.search(ebert_review_html)
    if review_text_match:
        review_text = review_text_match.groups()[0]
        formatted_review_text = _format_ebert_review_text(review_text)

        review_author_match = EBERT_AUTHOR_REGEX.search(ebert_review_html)
        review_author = review_author_match.groups()[0]

        review_date_match = EBERT_DATE_REGEX.search(ebert_review_html)
        review_date_string = review_date_match.groups()[0]
        review_datetime = datetime.strptime(review_date_string, '%B %d, %Y')
        review_date = review_datetime.date()

        review_stars_match = EBERT_STARS_REGEX.search(ebert_review_html)
        review_stars_string = review_stars_match.groups()[0]
        review_percent_score = _compute_ebert_percent_score(review_stars_string)

        return_dict = {
            "formatted_review_text":    formatted_review_text,
            "review_author":            review_author,
            "review_source":            EBERT_SITE_TITLE,
            "review_date":              review_date.strftime("%Y-%m-%d"),
            "review_percent_score":     review_percent_score,
        }

    return return_dict


def _compute_ebert_percent_score(review_stars_string):
    full_stars = len(re.findall(EBERT_FULL_STAR, review_stars_string))
    half_stars = len(re.findall(EBERT_HALF_STAR, review_stars_string))
    review_percent_score = (full_stars*2 + half_stars)/8.0
    return review_percent_score


def _format_ebert_review_text(review_text):
    review_text = review_text.replace('\n', '')
    formatted_review_text = review_text.replace(LOCAL_LINK_PREFIX, EBERT_LINK_PREFIX)
    return formatted_review_text
