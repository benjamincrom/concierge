#!/usr/bin/python

import html_manipulator
import imdb_scraper
import metacritic_scraper
import roger_ebert_scraper
import rottentomatoes_scraper


def printout(ebert_link, search_title, search_year):
    print '***********************************************************************************'
    print "%s (%s)" % (search_title, search_year)
    imdb_title_obj_dict = imdb_scraper.scrape_imdb_data(search_title, search_year)

    title = imdb_title_obj_dict["title"]
    media_type = imdb_title_obj_dict["video_type"]
    if imdb_title_obj_dict["year"]:
        year = imdb_title_obj_dict["year"]
    else:
        year = ''

    print ''
    print '--------------------------------------'
    print title
    print ''
    # print imdb
    for i, j in imdb_title_obj_dict.iteritems():
        print "%s:\t\t%s" % (i, j)

    # netacritic, rogerebert, and rottentomatoes only take movies
    if media_type == "Movie":
        metacritic_obj_dict = metacritic_scraper.scrape_metacritic(title, year)
        if metacritic_obj_dict:
            print '#########################################'
            print ' METACRITIC '
            for i, j in metacritic_obj_dict.iteritems():
                print "%s:\t\t%s" % (i, j)
            print '#########################################'

        rogerebert_obj_dict = roger_ebert_scraper.scrape_rogerebert_data(ebert_link)
        if rogerebert_obj_dict:
            print "============================================"
            print ' ROGEREBERT '
            for i, j in rogerebert_obj_dict.iteritems():
                print "%s:\t\t%s" % (i, j)
            print "============================================"


        rottentomatoes_obj_dict = rottentomatoes_scraper.scrape_rottentomatoes(title, year)
        if rottentomatoes_obj_dict:
            print "''''''''''''''''''''''''''''''''''''''''''''"
            print ' ROTTEN TOMATOES '
            for i, j in rottentomatoes_obj_dict.iteritems():
                print "%s:\t\t%s" % (i, j)
            print "''''''''''''''''''''''''''''''''''''''''''''"


if __name__ == '__main__':
    lines = open('test_list.txt').readlines()
    for line in lines:
        (ebert_review_url, ebert_title, ebert_year) = line.split(';')
        printout(ebert_review_url.strip(), ebert_title.strip(), ebert_year.strip())
