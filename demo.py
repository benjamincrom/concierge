#!/usr/bin/python


import imdb_scraper
import metacritic_scraper
import roger_ebert_scraper
import rottentomatoes_scraper


def parse_title(search_title, search_year='', ebert_link=''):
    print '***********************************************************************************'
    print "%s (%s)" % (search_title, search_year)
    # Get IMDB data 
    imdb_title_obj_dict = imdb_scraper.scrape_imdb_data(search_title, search_year)
    # If nothing is found then check the range around the search year to correct for inaccuracy
    if search_year and not imdb_title_obj_dict:
        search_year = int(search_year)
        search_year_list = [search_year - 1, search_year + 1, search_year - 2, search_year + 2]
        for current_search_year in search_year_list:
            imdb_title_obj_dict = imdb_scraper.scrape_imdb_data(search_title, current_search_year)
            if imdb_title_obj_dict:
                break

    # If we can't get the IMDB scrape completed then there is no point in continuing
    if imdb_title_obj_dict:
        title = imdb_title_obj_dict["title"]
        media_type = imdb_title_obj_dict["video_type"]
        if imdb_title_obj_dict["year"]:
            year = int(imdb_title_obj_dict["year"])
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

        # If this is a TV Series then get the Metacritic data for every season
        if media_type == "TV Series":
            season_list = range(1, imdb_title_obj_dict["tv_total_seasons"] + 1)
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


        # rogerebert and rottentomatoes only have good data for movies
        if media_type == "Movie":
            year_list = [year, year - 1, year + 1, year - 2, year + 2]
            # Get Metacritic data
            for current_year in year_list:
                metacritic_obj_dict = metacritic_scraper.scrape_metacritic(title, current_year)
                if metacritic_obj_dict:
                    break

            # Print Metacritic data
            if metacritic_obj_dict:
                print '#########################################'
                print ' METACRITIC '
                for i, j in metacritic_obj_dict.iteritems():
                    print "%s:\t\t%s" % (i, j)

                print '#########################################'

            # Get Rottentomatoes data
            for current_year in year_list:
                rottentomatoes_obj_dict = rottentomatoes_scraper.scrape_rottentomatoes(title, current_year)
                if rottentomatoes_obj_dict:
                    break

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
