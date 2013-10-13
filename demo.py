#!/usr/bin/python

import imdb_scraper
import metacritic_scraper
import roger_ebert_scraper
import rottentomatoes_scraper


def parse_title(search_title, search_year='', ebert_link=''):
    print '***********************************************************************************'
    print "%s (%s)" % (search_title, search_year)
    # Get IMDB data
    # If we are relying on Roger Ebert for the year then we must check the range around the year to combat inaccuracy
    if ebert_link:
        search_year = int(search_year)
        search_year_list = [search_year, search_year - 1, search_year + 1, search_year - 2, search_year + 2]
        for current_search_year in search_year_list:
            print "jklfdjsklf " + str(current_search_year) + " fkjldjskf"
            imdb_title_obj_dict = imdb_scraper.scrape_imdb_data(search_title, current_search_year)
            if imdb_title_obj_dict:
                break

    else:
        imdb_title_obj_dict = imdb_scraper.scrape_imdb_data(search_title, search_year)

    # If we can't get the IMDB scrape completed then there is no point in continuing
    if imdb_title_obj_dict:
        title = imdb_title_obj_dict["title"]
        media_type = imdb_title_obj_dict["video_type"]
        if imdb_title_obj_dict["year"]:
            year = imdb_title_obj_dict["year"]
        else:
            year = ''

        # Print IMDB data
        print ''
        print '--------------------------------------'
        print title
        print ''
        for i, j in imdb_title_obj_dict.iteritems():
            print "%s:\t\t%s" % (i, j)

        print '--------------------------------------'

        if media_type == "TV Series":
            season_list = range(1, imdb_title_obj_dict["tv_total_seasons"])
            season_title_list = ["Season %s" % season_index for season_index in season_list]
            # Print Metacritic data for each season
            for season_title in season_title_list:
                print season_title
                metacritic_obj_dict = metacritic_scraper.scrape_metacritic(title, season=season_title)
                if metacritic_obj_dict:
                    print '#########################################'
                    print ' METACRITIC '
                    for i, j in metacritic_obj_dict.iteritems():
                        print "%s:\t\t%s" % (i, j)

                    print '#########################################'


        # netacritic, rogerebert, and rottentomatoes only take movies
        if media_type == "Movie":
            # Get Metacritic data
            metacritic_obj_dict = metacritic_scraper.scrape_metacritic(title, year)
            # Print Metacritic data
            if metacritic_obj_dict:
                print '#########################################'
                print ' METACRITIC '
                for i, j in metacritic_obj_dict.iteritems():
                    print "%s:\t\t%s" % (i, j)

                print '#########################################'

            # Get Rottentomatoes data
            rottentomatoes_obj_dict = rottentomatoes_scraper.scrape_rottentomatoes(title, year)
            # Print Rottentomatoes data
            if rottentomatoes_obj_dict:
                print "''''''''''''''f''''''''''''''''''''''''''''''"
                print ' ROTTEN TOMATOES '
                for i, j in rottentomatoes_obj_dict.iteritems():
                    print "%s:\t\t%s" % (i, j)

                print "''''''''''''''''''''''''''''''''''''''''''''"

            if ebert_link:
                # Get Rogerebert Data
                rogerebert_obj_dict = roger_ebert_scraper.scrape_rogerebert_data(ebert_link)
                # Print Rogerebert Data
                if rogerebert_obj_dict:
                    print "============================================"
                    print ' ROGEREBERT '
                    for i, j in rogerebert_obj_dict.iteritems():
                        print "%s:\t\t%s" % (i, j)

                    print "============================================"

        print '***********************************************************************************'
        print ''


if __name__ == '__main__':
    lines = open('test_list.txt').readlines()
    for line in lines:
        (ebert_review_url, ebert_title, ebert_year) = line.split(';')
        parse_title(ebert_title.strip(), ebert_year.strip(), ebert_review_url.strip())
