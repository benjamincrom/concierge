#!/usr/bin/python

import roger_ebert_scraper
import imdb_scraper

if __name__ == '__main__':
    imdb_title_obj_dict = imdb_scraper.scrape_imdb_data('101 Dalmatians')
    for i,j in imdb_title_obj_dict.iteritems():
        print i
        print j
        print ''
    print '--------------------------------------'

    if imdb_title_obj_dict["video_type"] == "Movie":
        rogerebert_obj_dict = roger_ebert_scraper.scrape_rogerebert_data(imdb_title_obj_dict["title"],
                                                                         imdb_title_obj_dict["year"])
        f = open('test.html', 'w')
        f.write(rogerebert_obj_dict["formatted_review_text"])
        f.close()
        for i,j in rogerebert_obj_dict.iteritems():
            print i
            print j
            print ''
