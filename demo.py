#!/usr/bin/python


import roger_ebert_scraper
import rottentomatoes_scraper
import imdb_scraper
import metacritic_scraper


def printout(ebert_link, title, year):
    print '***********************************************************************************'
    print "%s (%s)" % (title, year)
    imdb_title_obj_dict = imdb_scraper.scrape_imdb_data(title, year)

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
        (ebert_link, title, year) = line.split(';')
        printout(ebert_link.strip(), title.strip(), year.strip())
