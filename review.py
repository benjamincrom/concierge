#!/usr/bin/python

class Review:
    LOCAL_LINK_PREFIX = '<a href="'
    EBERT_LINK_PREFIX = '<a href="http://www.rogerebert.com'
    EBERT_FULL_STAR = 'icon-star-full'
    EBERT_HALF_STAR = 'icon-star-half'
    EBERT_REVIEW_NOT_FOUND = "There is no review on rogerebert.com for this title: %s"
    EBERT_REVIEW_URL = "http://www.rogerebert.com/reviews/%s"
    EBERT_SITE_TITLE = "RogerEbert.com"
    EBERT_URL_DELIMITER = '-'

    EBERT_REVIEW_REGEX = re.compile('<div itemprop="reviewBody">(.+?)</div>', re.DOTALL)
    EBERT_AUTHOR_REGEX = re.compile('<meta content="(.+?)" name="author">')
    EBERT_DATE_REGEX = re.compile('itemprop="datePublished">(.+?)</time>')
    EBERT_STARS_REGEX = re.compile('itemprop="reviewRating"(.+?)</span>', re.DOTALL)


    def __init__(self, content, author, source, date, percent_score):
        self.content = content
        self.author = author
        self.source = source
        self.date = date
        self.percent_score = percent_score

    @classmethod
    def format_ebert_review_text(cls, review_text):
        review_text = review_text.replace('\n', '')
        formatted_review_text = review_text.replace(cls.LOCAL_LINK_PREFIX, cls.EBERT_LINK_PREFIX)
        return formatted_review_text

    @classmethod
    def compute_ebert_percent_score(cls, review_stars_string):
        full_stars = len(re.findall(cls.EBERT_FULL_STAR, review_stars_string))
        half_stars = len(re.findall(cls.EBERT_HALF_STAR, review_stars_string))
        review_percent_score = 100*(full_stars*2 + half_stars)/8.0
        return review_percent_score

    @classmethod
    def format_ebert_review_url(cls, title, year):
        title_str = cls.sanitize_url_segment(title, cls.EBERT_URL_DELIMITER).lower()
        url_formatted_title = urllib.quote("%s-%s" %(title_str, year))
        ebert_review_url = cls.EBERT_REVIEW_URL %(url_formatted_title)
        return ebert_revi

    def set_rogerebert_data(self):
        year_list = [self.year - 1, self.year, self.year + 1]
        for selected_year in year_list:
            ebert_review_url = self.format_ebert_review_url(self.title, selected_year)
            ebert_review_html = urllib.urlopen(ebert_review_url).read()

            review_text_match = self.EBERT_REVIEW_REGEX.search(ebert_review_html)
            if review_text_match:
                review_text = review_text_match.groups()[0]
                formatted_review_text = self.format_ebert_review_text(review_text)

                review_author_match = self.EBERT_AUTHOR_REGEX.search(ebert_review_html)
                review_author = review_author_match.groups()[0]

                review_date_match = self.EBERT_DATE_REGEX.search(ebert_review_html)
                review_date_string = review_date_match.groups()[0]
                review_date = datetime.strptime(review_date_string, '%B %d, %Y')

                review_stars_match = self.EBERT_STARS_REGEX.search(ebert_review_html)
                review_stars_string = review_stars_match.groups()[0]
                review_percent_score = self.compute_ebert_percent_score(review_stars_string)

                new_review_obj = Review(
                    formatted_review_text,
                    review_author,
                    self.EBERT_SITE_TITLE,
                    review_date,
                    rview_percent_score,
                                        )
                self.review_obj_list.append(new_review_obj)ew_url