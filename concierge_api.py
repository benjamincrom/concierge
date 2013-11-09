

import endpoints
import models
import webapp2

from google.appengine.api.datastore import Key
from protorpc import messages
from protorpc import message_types
from protorpc import remote


ROGEREBERT_REVIEW_SOURCE = 'RogerEbert.com'
ROTTENTOMATOES_REVIEW_SOURCE = 'Rottentomatoes Top Critics'
METACRITIC_REVIEW_SOURCE = 'Metacritic Metascore'

REQUEST_RESOURCE_CONTAINER = endpoints.ResourceContainer(
    message_types.VoidMessage,
    request_id=messages.StringField(2, required=True)
)


class RowMessage(messages.Message):
    title = messages.StringField(1)
    year = messages.IntegerField(2)
    genre_list_str = messages.StringField(3)
    ebert_score = messages.FloatField(4)
    rottentomatoes_score = messages.FloatField(5)
    metacritic_score = messages.FloatField(6)
    imdb_score = messages.FloatField(7)
    imdb_id = messages.StringField(8)


class OccupationMessage(messages.Message):
    occupation = messages.StringField(1)
    name = messages.StringField(2, repeated=True)


class ReviewMessage(messages.Message):
    review_source = messages.StringField(1)
    review_author = messages.StringField(2)
    review_content = messages.StringField(3)
    review_date = messages.StringField(4)
    review_score = messages.FloatField(5)


class VideoMessage(messages.Message):
    poster_url = messages.StringField(1)
    title = messages.StringField(2)
    plot = messages.StringField(3)
    tagline = messages.StringField(4)
    budget = messages.StringField(5)
    gross = messages.StringField(6)
    rating = messages.StringField(7)
    video_type = messages.StringField(8)
    aspect_ratio = messages.StringField(9)
    imdb_id = messages.StringField(10)
    score = messages.FloatField(11)
    length = messages.IntegerField(12)
    year = messages.IntegerField(13)
    genre_list = messages.StringField(14)
    occupation_list = messages.MessageField(OccupationMessage, 15, repeated=True)
    review_list = messages.MessageField(ReviewMessage, 16, repeated=True)


class VideoMessageCollection(messages.Message):
    video_list = messages.MessageField(VideoMessage, 1, repeated=True)


class RowMessageCollection(messages.Message):
    row_list = messages.MessageField(RowMessage, 1, repeated=True)


@endpoints.api(name='concierge', version='v1')
class ConciergeApi(remote.Service):
    """Concierge API v1."""
    @staticmethod
    @endpoints.method(message_types.VoidMessage, RowMessageCollection,
                      path='concierge_list', http_method='GET', name='videos.listVideos')
    def list_videos(self, unused_request):
        row_message_collection_obj = RowMessageCollection(row_list=[])
        video_query = models.Video.all()
        for video_obj in video_query.run(limit=100):
            this_row = RowMessage(title=video_obj.title,
                                  year=video_obj.year,
                                  genre_list_str=unwrap_list(video_obj.genre_list),
                                  imdb_id=video_obj.imdb_id,
                                  imdb_score=round(video_obj.score, 2))

            review_obj_list = models.Review.all().ancestor(video_obj)
            for review_obj in review_obj_list:
                if review_obj.review_source == ROGEREBERT_REVIEW_SOURCE:
                    this_row.ebert_score = round(review_obj.review_score, 2)
                elif review_obj.review_source == ROTTENTOMATOES_REVIEW_SOURCE:
                    this_row.rottentomatoes_score = round(review_obj.review_score, 2)
                elif review_obj.review_source == METACRITIC_REVIEW_SOURCE:
                    this_row.metacritic_score = round(review_obj.review_score, 2)

            row_message_collection_obj.row_list.append(this_row)

        return row_message_collection_obj

    @staticmethod
    @endpoints.method(REQUEST_RESOURCE_CONTAINER, VideoMessage,
                      path='concierge_display/{request_id}', http_method='GET', name='videos.displayVideo')
    def display_video(self, request):
        q = models.Video.all().filter('imdb_id =', request.request_id).get()

        # Get occupation data into a dict
        occupation_dict = {}
        for name_occupation_key in q.name_occupation_key_list:
            occupation_obj = models.NameOccupation.get(name_occupation_key)
            if occupation_obj.occupation not in occupation_dict:
                occupation_dict[occupation_obj.occupation] = []

            occupation_dict[occupation_obj.occupation].append(occupation_obj.name)

        genre_list_str = unwrap_list(q.genre_list)
        # Get video data into message object
        this_video_message = VideoMessage(poster_url=q.poster_url,
                                          title=q.title,
                                          plot=q.plot,
                                          tagline=q.tagline,
                                          budget=q.budget,
                                          gross=q.gross,
                                          rating=q.rating,
                                          video_type=q.video_type,
                                          aspect_ratio=str(q.aspect_ratio),
                                          imdb_id=q.imdb_id,
                                          score=round(q.score, 2),
                                          length=q.length,
                                          year=q.year,
                                          genre_list=genre_list_str,
                                          occupation_list=[],
                                          review_list=[])
        # Get occupation data out of dict and into message objects
        for occupation in occupation_dict:
            this_occupation_obj = OccupationMessage(occupation=occupation,
                                                    name=occupation_dict[occupation])
            this_video_message.occupation_list.append(this_occupation_obj)

        # Get reviews into message objects
        review_obj_list = models.Review.all().ancestor(q).order('review_source')
        for review_obj in review_obj_list:
            if review_obj.review_date is None:
                review_obj.review_date = ''

            this_review = ReviewMessage(review_source=review_obj.review_source,
                                        review_score=round(review_obj.review_score, 2),
                                        review_author=review_obj.review_author,
                                        review_content=review_obj.review_content,
                                        review_date=str(review_obj.review_date))
            this_video_message.review_list.append(this_review)

        return this_video_message


def unwrap_list(this_list):
    return_str = ''
    for item in this_list:
        if return_str:
            return_str += ', '

        return_str += item

    return return_str


application = endpoints.api_server([ConciergeApi])

redirect = webapp2.WSGIApplication([
    webapp2.Route('/<:.*>', webapp2.RedirectHandler, defaults={'_uri': '/app/index.html'}),
], debug=False)

