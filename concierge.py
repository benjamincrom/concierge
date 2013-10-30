

from google.appengine.ext import db

import webapp2


class NameOccupation(db.Model):
    name = db.StringProperty()
    occupation = db.StringProperty()


class Review(db.Model):
    review_score = db.FloatProperty()
    review_author = db.StringProperty()
    review_source = db.StringProperty()
    review_content = db.TextProperty()
    review_date = db.DateProperty()


class Series(db.Model):
    series_name = db.StringProperty()
    total_episodes_in_series = db.IntegerProperty()
    total_seasons_in_series = db.IntegerProperty()
    genre_list = db.StringListProperty()
    creator = db.ReferenceProperty(NameOccupation)
    season_key_list = db.ListProperty(db.Key)


class Season(db.Model):
    season_number = db.IntegerProperty()
    total_episodes_in_season = db.IntegerProperty()
    series = db.ReferenceProperty(Series)
    review_key_list = db.ListProperty(db.Key)


class Video(db.Model):
    title = db.StringProperty()
    poster_url = db.StringProperty()
    plot = db.TextProperty()
    tagline = db.StringProperty()
    gross = db.TextProperty()
    imdb_id = db.StringProperty()
    budget = db.TextProperty()
    video_type = db.StringProperty()
    rating = db.StringProperty()
    genre_list = db.StringListProperty()
    aspect_ratio = db.FloatProperty()
    score = db.FloatProperty()
    episode_number_in_season = db.IntegerProperty()
    episode_number_in_total = db.IntegerProperty()
    year = db.IntegerProperty()
    length = db.IntegerProperty()
    name_occupation_key_list = db.ListProperty(db.Key)
    review_key_list = db.ListProperty(db.Key)
    season = db.ReferenceProperty(Season)


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('<html><head></head><body>')

        video_query = Video.all()
        for q in video_query.run(limit=50):
            genre_str = ''
            for genre in q.genre_list:
                if genre_str:
                    genre_str += ', '

                genre_str += str(genre)

            occupation_dict = {}
            for name_occupation_key in q.name_occupation_key_list:
                occupation_obj = NameOccupation.all().filter('__key__ >', name_occupation_key).get()
                if occupation_obj.occupation not in occupation_dict:
                    occupation_dict[str(occupation_obj.occupation)] = []

                occupation_dict[str(occupation_obj.occupation)].append(str(occupation_obj.name))

            self.response.write('<table>')
            self.response.write('<tr><td></td><td><img src="%s"></td></tr>' % q.poster_url)
            self.response.write('<tr><td>Title: </td><td>%s</td></tr>' % q.title)
            self.response.write('<tr><td>Year: </td><td>%s</td></tr>' % q.year)
            self.response.write('<tr><td>Plot: </td><td>%s</td></tr>' % q.plot)
            self.response.write('<tr><td>Tagline: </td><td>%s</td></tr>' % q.tagline)
            self.response.write('<tr><td>Budget: </td><td>%s</td></tr>' % q.budget)
            self.response.write('<tr><td>Gross: </td><td>%s</td></tr>' % q.gross)
            self.response.write('<tr><td>Rating: </td><td>%s</td></tr>' % q.rating)
            self.response.write('<tr><td>Video Type: </td><td>%s</td></tr>' % q.video_type)
            self.response.write('<tr><td>Genres: </td><td>%s</td></tr>' % genre_str)
            self.response.write('<tr><td>Aspect Ratio: </td><td>%s</td></tr>' % q.aspect_ratio)
            self.response.write('<tr><td>Score: </td><td>%s</td></tr>' % q.score)
            self.response.write('<tr><td>Length: </td><td>%s</td></tr>' % q.length)
            self.response.write('<tr><td>IMDB ID: </td><td>%s</td></tr>' % q.imdb_id)

            self.response.write('<tr><td></td><td></td></tr>')

            self.response.write('<tr><td>occupation list: </td><td><table>')
            for (occupation, person_list) in occupation_dict.iteritems():
                self.response.write('<tr><td><br /></td><td></td></tr>')
                self.response.write('<tr><td><strong>' + occupation + '(s):</strong></td><td>')
                for person in person_list:
                    self.response.write(person + '<br />')

                self.response.write('</td></tr>')

            self.response.write('</table><br /></td></tr>')

            self.response.write('<tr><td>review list: </td><td>%s</td></tr>' % q.review_key_list)
            self.response.write('</table><br /><br />')

        self.response.write('</body></html>')


application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)