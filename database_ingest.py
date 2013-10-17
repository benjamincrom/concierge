#!/usr/bin/python


import imdb_scraper
import json
import metacritic_scraper
import roger_ebert_scraper
import rottentomatoes_scraper


INPUT_FILE = 'test_list.txt'
OUTPUT_FILE = 'formatted_titles.txt'


def parse_title(search_title, out_file, search_year='', ebert_link=''):
    # Get IMDB data
    imdb_title_obj_dict = imdb_scraper.scrape_imdb_data(search_title, search_year)
    # If nothing is found then check the range (-2) below the search year to correct for inaccuracy
    if search_year and not imdb_title_obj_dict:
        search_year = int(search_year)
        search_year_list = [search_year - 1, search_year - 2]
        for current_search_year in search_year_list:
            imdb_title_obj_dict = imdb_scraper.scrape_imdb_data(search_title, current_search_year)
            if imdb_title_obj_dict:
                break

    # If we can't get the IMDB scrape completed then there is no point in continuing
    if imdb_title_obj_dict:
        rottentomatoes_obj_dict = {}
        metacritic_obj_dict = {}

        title = imdb_title_obj_dict["title"]
        media_type = imdb_title_obj_dict["video_type"]
        if imdb_title_obj_dict["year"]:
            year = int(imdb_title_obj_dict["year"])
        else:
            year = ''

        # If this is a TV Series then get the Metacritic data for every season
        if media_type == "TV Series":
            season_list = range(1, imdb_title_obj_dict["tv_total_seasons"] + 1)
            season_title_list = ["Season %s" % season_index for season_index in season_list]
            # Scrape Metacritic data for each season
            for season_title in season_title_list:
                metacritic_obj_dict = metacritic_scraper.scrape_metacritic(title, season=season_title)

        # rogerebert and rottentomatoes only have good data for movies
        if media_type == "Movie":
            year_list = [year, year - 1, year - 2]
            # Get Metacritic data -- try both the IMDB title and the given search title
            for current_year in year_list:
                metacritic_obj_dict = metacritic_scraper.scrape_metacritic(title, current_year)
                if metacritic_obj_dict:
                    break

            if not metacritic_obj_dict and title != search_title:
                for current_year in year_list:
                    metacritic_obj_dict = metacritic_scraper.scrape_metacritic(search_title, current_year)
                    if metacritic_obj_dict:
                        break

            # Get Rottentomatoes data -- try both the IMDB title and the given search title
            for current_year in year_list:
                rottentomatoes_obj_dict = rottentomatoes_scraper.scrape_rottentomatoes(title, current_year)
                if rottentomatoes_obj_dict:
                    break

            if not rottentomatoes_obj_dict and title != search_title:
                for current_year in year_list:
                    rottentomatoes_obj_dict = rottentomatoes_scraper.scrape_rottentomatoes(search_title, current_year)
                    if rottentomatoes_obj_dict:
                        break

            # Get Rogerebert Data
            if ebert_link:
                rogerebert_obj_dict = roger_ebert_scraper.scrape_rogerebert_data(ebert_link)

        # Build json string containing all data and append to output file
        return_dict = dict(imdb_title_obj_dict.items() + rottentomatoes_obj_dict.items() +
                           metacritic_obj_dict.items() + rogerebert_obj_dict.items())

        return_json_str = json.dumps(return_dict, sort_keys=True, indent=4, separators=(',', ': '))
        out_file.write(return_json_str)


if __name__ == '__main__':
    output_file = open(OUTPUT_FILE, 'a')
    lines = open(INPUT_FILE).readlines()
    for line in lines:
        (ebert_review_url, ebert_title, ebert_year) = line.split(';')
        parse_title(ebert_title.strip(), output_file, ebert_year.strip(), ebert_review_url.strip())
    output_file.close()
