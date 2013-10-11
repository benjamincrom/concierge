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

GOOGLE_REGEX = re.compile("<h2 class=\"hd\">Search Results.*?<a href=\"(.+?)\"", re.DOTALL)


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def get_top_google_result_url(search_string):
    formatted_search_string = search_string.replace(' ', '+')
    html = retrieve_html_from_url(GOOGLE_QUERY_URL % formatted_search_string)
    top_result_url = None
    if html:
        top_result_url = use_regex(GOOGLE_REGEX, html, True)
        if top_result_url:
            top_result_url = top_result_url.strip()
    return top_result_url


def retrieve_html_from_url(url):
    if not url:
        return None

    html = None
    try:
        req = urllib2.Request(url, headers=SPOOFED_HEADERS)
        html = urllib2.urlopen(req).read().decode('latin-1').encode('ascii', 'ignore')
    except (AttributeError, UnicodeDecodeError):
        print RETRIEVE_HTML_ERROR % url
        raise
    except urllib2.URLError:
        print RETRIEVE_HTML_ERROR % url
    return html


def remove_html_tags(html_str):
    if html_str:
        s = MLStripper()
        s.feed(html_str.decode('latin-1').encode('ascii', 'ignore'))
        return_str = s.get_data()
    else:
        return_str = None
    return return_str


def use_regex(given_regex, target_str, can_be_null):
    match = given_regex.search(target_str)
    try:
        return_str = str(match.groups()[0]).strip()
    except (AttributeError, IndexError):
        return_str = None
        if not can_be_null:
            print REGEX_NOT_FOUND_ERROR % given_regex.pattern
            raise
    return return_str
