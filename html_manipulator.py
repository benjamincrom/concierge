#!/usr/bin/python


import re
import urllib2

from HTMLParser import HTMLParser


GOOGLE_QUERY_URL = "http://www.google.com/search?q=%s"
REGEX_NOT_FOUND_ERROR = "ERROR: Target regex '%s' not found--this value cannot be null"
RETRIEVE_HTML_ERROR = "ERROR: URL '%s' cannot be properly retrieved"

SPOOFED_HEADERS = {
    'User-Agent':           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko)'
                            ' Chrome/23.0.1271.64 Safari/537.11',
    'Accept':               '``text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset':       'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding':      'none',
    'Accept-Language':      'en-US,en;q=0.8',
    'Connection':           'keep-alive',
}

GOOGLE_REGEX_SEARCH = re.compile("<h2 class=\"hd\">Search Results.*?<a href=\"(.+?)\"", re.DOTALL)
GOOGLE_REGEX_SIMILAR = re.compile("<h2 class=\"hd\">.*?Results for similar searches.*?<a href=\"(.+?)\"", re.DOTALL)


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def get_top_google_result_url(search_string):
    """Return the url for the top google result returned when using this search string as a query.

    This method prefers the top entry of 'Results for Similar Searches' if that section is present on the page.
    Returns None if no Google results are returned.
    """
    top_result_url = None
    formatted_search_string = search_string.replace(' ', '+').replace('&', '')
    html = retrieve_html_from_url(GOOGLE_QUERY_URL % formatted_search_string)
    if html:
        top_result_url_similar_match = GOOGLE_REGEX_SIMILAR.search(html)
        if top_result_url_similar_match:
            top_result_url = top_result_url_similar_match.groups()[0]
        else:
            top_result_url_search_match = GOOGLE_REGEX_SEARCH.search(html)
            if top_result_url_search_match:
                top_result_url = top_result_url_search_match.groups()[0]

    return top_result_url


def retrieve_html_from_url(url):
    """Return the raw html found at the given URL"""
    html = None
    if url:
        try:
            req = urllib2.Request(url, headers=SPOOFED_HEADERS)
            html = urllib2.urlopen(req).read().decode('latin-1').encode('ascii', 'ignore')
        except (AttributeError, UnicodeDecodeError):
            print RETRIEVE_HTML_ERROR % url
            raise
        except urllib2.URLError as e:
            print RETRIEVE_HTML_ERROR % url
            print e.reason

    return html


def remove_html_tags(html_str):
    """Removes all html tags from the given string"""
    return_str = None
    if html_str:
        s = MLStripper()
        s.feed(html_str.decode('latin-1').encode('ascii', 'ignore'))
        return_str = s.get_data()

    return return_str


def use_regex(given_regex, target_str, can_be_null):
    """Searches for given regex in target string and returns the first group if the regex is found.

    Returns None if the given rexex is not found and can_be_null is True.
    Throws exception if given regex is not found and can_be_null is False.
    """
    return_str = None
    match = given_regex.search(target_str)
    try:
        return_str = str(match.groups()[0]).strip()
    except (AttributeError, IndexError):
        if not can_be_null:
            print REGEX_NOT_FOUND_ERROR % given_regex.pattern
            raise

    return return_str
