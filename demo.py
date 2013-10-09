#!/usr/bin/python

import roger_ebert_scraper
import rottentomatoes_scraper
import imdb_scraper
import metacritic_scraper

if __name__ == '__main__':
    imdb_title_obj_dict = imdb_scraper.scrape_imdb_data('Gliding Over All')

    title = imdb_title_obj_dict["title"]
    type = imdb_title_obj_dict["video_type"]
    if imdb_title_obj_dict["year"]:
        year = imdb_title_obj_dict["year"]
    else:
        year = ''

    # print imdb
    for i,j in imdb_title_obj_dict.iteritems():
        print i
        print j
        print ''
    print '--------------------------------------'

    # netacritic, rogerebert, and rottentomatoes only take movies
    if type == "Movie":
        metacritic_obj_dict = metacritic_scraper.scrape_metacritic(title, year, type)
        if metacritic_obj_dict:
            for i,j in metacritic_obj_dict.iteritems():
                print i
                print j
                print ''
            print '#########################################'

        rogerebert_obj_dict = roger_ebert_scraper.scrape_rogerebert_data(title, year)
        if rogerebert_obj_dict:
            f = open('test.html', 'w')
            f.write(rogerebert_obj_dict["formatted_review_text"])
            f.close()
            for i,j in rogerebert_obj_dict.iteritems():
                print i
                print j
                print ''
            print "============================================"

        rottentomatoes_obj_dict = rottentomatoes_scraper.scrape_rottentomatoes(title, year)
        for i,j in rottentomatoes_obj_dict.iteritems():
            print i
            print j
            print ''
