

import json
import webapp2

import models


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'

        video_query = models.Video.all()
        for q in video_query.run(limit=50):
            # Add video data to return dictionary
            return_dict = {'poster_url': q.poster_url,
                           'title': q.title,
                           'year': q.year,
                           'plot': q.plot,
                           'tagline': q.tagline,
                           'budget': q.budget,
                           'gross': q.gross,
                           'rating': q.rating,
                           'video_type': q.video_type,
                           'genre_list': q.genre_list,
                           'aspect_ratio': q.aspect_ratio,
                           'score': q.score,
                           'length': q.length,
                           'imdb_id': q.imdb_id,
                           'review_data_dict': {}}

            # Add people to return dictionary
            for name_occupation_key in q.name_occupation_key_list:
                occupation_obj = models.NameOccupation.get(name_occupation_key)
                if occupation_obj.occupation not in return_dict:
                    return_dict[str(occupation_obj.occupation)] = []

                return_dict[str(occupation_obj.occupation)].append(str(occupation_obj.name))

            # Add reviews to return dictionary
            review_obj_list = models.Review.all().ancestor(q)
            for review_obj in review_obj_list:
                this_review_dict = {'review_score': review_obj.review_score,
                                    'review_author': review_obj.review_author,
                                    'review_content': review_obj.review_content,
                                    'review_date': str(review_obj.review_date)}

                return_dict['review_data_dict'][review_obj.review_source] = this_review_dict

            self.response.write(json.dumps(return_dict, sort_keys=True, indent=4, separators=(',', ': ')))

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
