#!/usr/bin/python


import webapp2

import models


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers["Content-Type"] = "text/html"
        self.response.write("<html><head></head><body>")

        video_query = models.Video.all()
        for q in video_query.run(limit=100):
            genre_str = ""
            for genre in q.genre_list:
                if genre_str:
                    genre_str += ", "

                genre_str += str(genre)

            occupation_dict = {}
            for name_occupation_key in q.name_occupation_key_list:
                occupation_obj = models.NameOccupation.get(name_occupation_key)
                if occupation_obj.occupation not in occupation_dict:
                    occupation_dict[str(occupation_obj.occupation)] = []

                occupation_dict[str(occupation_obj.occupation)].append(str(occupation_obj.name))

            review_obj_list = models.Review.all().ancestor(q)

            self.response.write("<table>")
            self.response.write("<tr><td></td><td><img src="%s"></td></tr>" % q.poster_url)
            self.response.write("<tr><td>Title: </td><td>%s</td></tr>" % q.title)
            self.response.write("<tr><td>Year: </td><td>%s</td></tr>" % q.year)
            self.response.write("<tr><td>Plot: </td><td>%s</td></tr>" % q.plot)
            self.response.write("<tr><td>Tagline: </td><td>%s</td></tr>" % q.tagline)
            if q.budget:
                self.response.write("<tr><td>Budget: </td><td>%s</td></tr>" % q.budget)

            if q.gross:
                self.response.write("<tr><td>Gross: </td><td>%s</td></tr>" % q.gross)

            self.response.write("<tr><td>Rating: </td><td>%s</td></tr>" % q.rating)
            self.response.write("<tr><td>Video Type: </td><td>%s</td></tr>" % q.video_type)
            self.response.write("<tr><td>Genres: </td><td>%s</td></tr>" % genre_str)
            self.response.write("<tr><td>Aspect Ratio: </td><td>%s</td></tr>" % q.aspect_ratio)
            self.response.write("<tr><td>Score: </td><td><strong>%s</strong></td></tr>" % q.score)
            self.response.write("<tr><td>Length: </td><td>%s</td></tr>" % q.length)
            self.response.write("<tr><td>IMDB ID: </td><td>%s</td></tr>" % q.imdb_id)

            for (occupation, person_list) in occupation_dict.iteritems():
                self.response.write("<tr><td><br /></td><td></td></tr>")
                self.response.write("<tr><td>" + occupation + "(s):</td><td>")
                for person in person_list:
                    self.response.write(person + "<br />")

            for review_obj in review_obj_list:
                self.response.write("<tr><td><br /></td><td></td></tr>")
                self.response.write("<tr><td>%s: </td><td><strong>%s</strong></td></tr>" % (review_obj.review_source,
                                                                                            review_obj.review_score))
                if review_obj.review_author:
                    self.response.write("<tr><td></td><td>%s</td></tr>" % review_obj.review_author)

                if review_obj.review_content:
                    self.response.write("<tr><td></td><td>%s</td></tr>" % review_obj.review_content)

                if review_obj.review_date:
                    self.response.write("<tr><td></td><td>Review Date: %s</td></tr>" % review_obj.review_date)

            self.response.write("</table><br /><br /><br /><br /><br />")

        self.response.write("</body></html>")


application = webapp2.WSGIApplication([
    ("/", MainPage),
], debug=True)
