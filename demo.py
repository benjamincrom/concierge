#!/usr/bin/python

import roger_ebert_scraper
import rottentomatoes_scraper
import imdb_scraper
import metacritic_scraper



def printout(title):
    imdb_title_obj_dict = imdb_scraper.scrape_imdb_data(title)

    title = imdb_title_obj_dict["title"]
    type = imdb_title_obj_dict["video_type"]
    if imdb_title_obj_dict["year"]:
        year = imdb_title_obj_dict["year"]
    else:
        year = ''

    print ''
    print '--------------------------------------'
    print title
    print ''
    # print imdb
    for i,j in imdb_title_obj_dict.iteritems():
        print "%s:\t\t%s" %(i, j)

    # netacritic, rogerebert, and rottentomatoes only take movies
    if type == "Movie" and imdb_title_obj_dict["year"] > 1959:
        metacritic_obj_dict = metacritic_scraper.scrape_metacritic(title, year, type)
        if metacritic_obj_dict:
            for i,j in metacritic_obj_dict.iteritems():
                print "%s:\t\t%s" %(i, j)
            print '#########################################'


        rogerebert_obj_dict = roger_ebert_scraper.scrape_rogerebert_data(title, year)
        if rogerebert_obj_dict:
            f = open('test.html', 'w')
            f.write(rogerebert_obj_dict["formatted_review_text"])
            f.close()
            for i,j in rogerebert_obj_dict.iteritems():
                print "%s:\t\t%s" %(i, j)
            print "============================================"

        rottentomatoes_obj_dict = rottentomatoes_scraper.scrape_rottentomatoes(title, year)
        for i,j in rottentomatoes_obj_dict.iteritems():
            print "%s:\t\t%s" %(i, j)

if __name__ == '__main__':
    names = open('test_list.txt').readlines()
    for name in names:
        printout(name.strip())
