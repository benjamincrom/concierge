#!/usr/bin/python


import json
import re
import socket
import urllib2

from HTMLParser import HTMLParser


GOOGLE_QUERY_URL = ("https://www.googleapis.com/customsearch/v1"
                    "?key=AIzaSyCMGfdDaSfjqv5zYoS0mTJnOT3e9MURWkU&cx=017381156867331432490:g58htnlfkuk&q=%s")
REGEX_NOT_FOUND_ERROR = "ERROR: Target regex \"%s\" not found--this value cannot be null"
RETRIEVE_HTML_ERROR = "ERROR: URL \"%s\" cannot be properly retrieved"
RETRIEVE_QUERY_ERROR = "ERROR: Query \"%s\" cannot be properly retrieved"

SPOOFED_HEADERS = {
    "User-Agent":           "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko)"
                            " Chrome/23.0.1271.64 Safari/537.11",
    "Accept":               "``text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Charset":       "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Accept-Encoding":      "none",
    "Accept-Language":      "en-US,en;q=0.8",
    "Connection":           "keep-alive",
}

GOOGLE_REGEX_SEARCH = re.compile("<h2 class=\"hd\">Search Results.*?<a href=\"(.+?)\"", re.DOTALL)


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, data):
        self.fed.append(data)

    def get_data(self):
        return "".join(self.fed)


def get_top_google_result_url(search_string):
    """Return the url for the top google result returned when using this search string as a query.

    This method prefers the top entry of "Results for Similar Searches" if that section is present on the page.
    Returns "" if no Google results are returned.
    """
    top_result_url = ""
    formatted_search_string = search_string.replace(" ", "+").replace("&", "")
    try:
        json_str = urllib2.urlopen(GOOGLE_QUERY_URL % formatted_search_string).read()
    except urllib2.HTTPError:
        json_str = ""
        print(RETRIEVE_QUERY_ERROR % search_string)
        
    if json_str:
        json_obj = json.loads(json_str)
        if "items" in json_obj:
            top_result_url = str(json_obj["items"][0]["link"])

    return top_result_url


def retrieve_html_from_url(url):
    """Return the raw html found at the given URL"""
    html = ""
    if url:
        try:
            req = urllib2.Request(url, headers=SPOOFED_HEADERS)
            html = urllib2.urlopen(req).read()
        except (AttributeError, UnicodeDecodeError):
            print(RETRIEVE_HTML_ERROR % url)
            raise
        except (urllib2.URLError, socket.error):
            print(RETRIEVE_HTML_ERROR % url)

    return html


def remove_html_tags(html_str):
    """Removes all html tags from the given string"""
    return_str = ""
    if html_str:
        s = MLStripper()
        s.feed(html_str.decode("latin-1").encode("ascii", "ignore"))
        return_str = s.get_data()

    return return_str.strip()


def use_regex(given_regex, target_str, can_be_null):
    """Searches for given regex in target string and returns the first group if the regex is found.

    Returns "" if the given rexex is not found and can_be_null is True.
    Throws exception if given regex is not found and can_be_null is False.
    """
    return_str = ""
    try:
        match = given_regex.search(target_str)
        if match:
            return_str = str(match.group(1)).strip()

    except (AttributeError, TypeError):
        if not can_be_null:
            raise Exception("REGEX_NOT_FOUND_ERROR % given_regex.pattern")

    return return_str
