#!/usr/bin/python

import json
import re
import urllib

class Review:
    def __init__(self, content, source):
        self.content = content
        self.source = source


class Video:
    LOCAL_LINK_PREFIX = '<a href="'
    EBERT_LINK_PREFIX = '<a href="http://www.rogerebert.com'
    EBERT_REVIEW_NOT_FOUND = "There is no review on rogerebert.com for this title: %s"
    EBERT_REVIEWS_URL = "http://www.rogerebert.com/reviews/%s"
    EBERT_SITE_TITLE = "RogerEbert.com"
    EBERT_REVIEW_REGEX = re.compile('<div itemprop="reviewBody">(.+?)</div>', re.DOTALL)

    def __init__(self, title):
        """This class will pull metadata from remote sources and store it in a video object"""
        # initialize empty lists
        self.review_obj_list = []

        # populate object with data
        self.set_imdb_data(title)
        self.set_rogerebert_data()

    def set_imdb_data(self, title):
        """ Pull down JSON data for this title from the IMDB API and store in imdb_json_dict """
        imdb_json_str = urllib.urlopen("http://www.omdbapi.com/?t=%s" %(urllib.quote(title))).read()
        imdb_json_dict = json.loads(imdb_json_str)

        # Check to see that the query returned a valid response
        if imdb_json_dict['Response'] == 'False':
            raise Exception(imdb_json_dict['Error'])

        # Store the following IMDB metadata directly in video object
        self.title = imdb_json_dict['Title']
        self.rating = imdb_json_dict['Rated']
        self.plot = imdb_json_dict['Plot']
        self.poster_url = imdb_json_dict['Poster']
        self.year = int(imdb_json_dict['Year'])
        self.video_type = imdb_json_dict['Type']

        # Convert the following IMDB metadata into the correct format and then store it in video object
        self.length = self.calculate_length_from_runtime_str(imdb_json_dict['Runtime'])

        # Split comma separated fields into python lists
        self.writer_list = [str(writer_name.strip()) for writer_name in imdb_json_dict['Writer'].split(',')]
        self.director_list = [str(director_name.strip()) for director_name in imdb_json_dict['Director'].split(',')]
        self.actor_list = [str(actor_name.strip()) for actor_name in imdb_json_dict['Actors'].split(',')]
        self.genre_list = [str(genre_name.strip()) for genre_name in imdb_json_dict['Genre'].split(',')]

    def set_rogerebert_data(self):
        """ Search for rogerbert.com review by querying '[title]-[year]', '[title]-[year+1]', and '[title]-[year-1]'"""
        year_list = [self.year - 1, self.year, self.year + 1]
        for year in year_list:
            lowercase_hyphenated_title = self.title.lower().replace(' ', '-')
            url_formatted_title = urllib.quote("%s-%s" %(lowercase_hyphenated_title, year))
            ebert_review_url = self.EBERT_REVIEWS_URL %(url_formatted_title)
            ebert_review_html = urllib.urlopen(ebert_review_url).read()
            review_match = self.EBERT_REVIEW_REGEX.search(ebert_review_html)
            if review_match:
                review_text = review_match.groups()[0]
                # remove newline characters from review
                review_text = review_text.replace('\n', '')
                # turn local links into fully qualified links
                review_text = review_text.replace(self.LOCAL_LINK_PREFIX, self.EBERT_LINK_PREFIX)
                new_review_obj = Review(review_text, self.EBERT_SITE_TITLE)
                self.review_obj_list.append(new_review_obj)

    @classmethod
    def calculate_length_from_runtime_str(cls, runtime_str):
        """ Given a runtime of the format '2 h 24 min' return the length in minutes """
        match_object = re.match("(\d+) h (\d+) min", runtime_str)
        hours, minutes = match_object.groups()
        length = int(hours)*60 + int(minutes)
        return length


if __name__ == '__main__':
    g = Video('Now You See Me')
    print g.title
    print g.year
    print g.length
    print g.poster_url
    print g.plot
    print g.rating
    print g.video_type
    print g.genre_list
    print g.writer_list
    print g.director_list
    print g.actor_list
    # print g.budget
    # print g.gross
    # print g.tagline
    # print g.aspect_ratio
    # print g.collection_obj (if exists--properties: name, season, episode, index)
    print "=============================="
    for review_obj in g.review_obj_list: # (review_obj properties: source, percent_score, headline, text)
        print "Review: "
        print review_obj.content
        print review_obj.source
        # print review_obj.author =
        # print review_obj.percentage_score =
        # print review_obj.headline =
        # print review_obj.date =
        f = open('test.html','w')
        f.write(review_obj.content)
        f.close()
    print "=============================="
