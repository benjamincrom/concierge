

import endpoints
import models
import webapp2

from google.appengine.api.datastore import Key
from protorpc import messages
from protorpc import message_types
from protorpc import remote


ROGEREBERT_REVIEW_SOURCE = 'RogerEbert.com'
ROTTENTOMATOES_TOP_CRITICS_SOURCE = 'Rottentomatoes Top Critics'
ROTTENTOMATOES_ALL_CRITICS_SOURCE = 'Rottentomatoes All Critics'
ROTTENTOMATOES_AUDIENCE_METER_SOURCE = 'Rottentomatoes Audience Meter'
METACRITIC_METASCORE_SOURCE = 'Metacritic Metascore'
METACRITIC_USERSCORE_SOURCE = 'Metacritic Userscore'

REQUEST_RESOURCE_CONTAINER = endpoints.ResourceContainer(
    message_types.VoidMessage,
    request_id=messages.StringField(2, required=True)
)


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
    genre_list_str = messages.StringField(14)
    ebert_review = messages.MessageField(ReviewMessage, 16)
    metacritic_metascore_review = messages.MessageField(ReviewMessage, 17)
    metacritic_userscore_review = messages.MessageField(ReviewMessage, 18)
    rottentomatoes_top_critics_review = messages.MessageField(ReviewMessage, 19)
    rottentomatoes_all_critics_review = messages.MessageField(ReviewMessage, 20)
    rottentomatoes_audience_meter_review = messages.MessageField(ReviewMessage, 21)
    director_list_str = messages.StringField(22)
    writer_list_str = messages.StringField(23)
    star_list_str = messages.StringField(24)
    


class VideoMessageCollection(messages.Message):
    video_list = messages.MessageField(VideoMessage, 1, repeated=True)


@endpoints.api(name='concierge', version='v1')
class ConciergeApi(remote.Service):
    """Concierge API v1."""
    @staticmethod
    @endpoints.method(message_types.VoidMessage, VideoMessageCollection,
                      path='concierge_list', http_method='GET', name='videos.listVideos')
    def list_videos(self, unused_request):
        video_message_collection_obj = VideoMessageCollection(video_list=[])

        video_query = models.Video.all()
        for q in video_query.run(limit=100):
            video_message_collection_obj.video_list.append(self.get_video_message_from_query_obj(q))
        
        return video_message_collection_obj

    @staticmethod
    @endpoints.method(REQUEST_RESOURCE_CONTAINER, VideoMessage,
                      path='concierge_display/{request_id}', http_method='GET', name='videos.displayVideo')
    def display_video(self, request):
        q = models.Video.all().filter('imdb_id =', request.request_id).get()
        return self.get_video_message_from_query_obj(q)

    @classmethod
    def get_video_message_from_query_obj(cls, q):
        # Get occupation data into a dict
        director_list_str = ""
        writer_list_str = ""
        star_list_str = ""
        for name_occupation_key in q.name_occupation_key_list:
            occupation_obj = models.NameOccupation.get(name_occupation_key)
            if occupation_obj.occupation == 'Director':
                if director_list_str:
                    director_list_str += ', '
                director_list_str += occupation_obj.name
            elif occupation_obj.occupation == 'Writer':
                if writer_list_str:
                    writer_list_str += ', '
                writer_list_str += occupation_obj.name
            elif occupation_obj.occupation == 'Star':
                if star_list_str:
                    star_list_str += ', '
                star_list_str += occupation_obj.name

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
                                          genre_list_str=genre_list_str,
                                          writer_list_str=writer_list_str,
                                          director_list_str=director_list_str,
                                          star_list_str=star_list_str)

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

            if review_obj.review_source == ROGEREBERT_REVIEW_SOURCE:
                this_video_message.ebert_review = this_review
            elif review_obj.review_source == METACRITIC_METASCORE_SOURCE:
                this_video_message.metacritic_metascore_review = this_review
            elif review_obj.review_source == METACRITIC_USERSCORE_SOURCE:
                this_video_message.metacritic_userscore_review = this_review
            elif review_obj.review_source == ROTTENTOMATOES_TOP_CRITICS_SOURCE:
                this_video_message.rottentomatoes_top_critics_review = this_review
            elif review_obj.review_source == ROTTENTOMATOES_ALL_CRITICS_SOURCE:
                this_video_message.rottentomatoes_all_critics_review = this_review
            elif review_obj.review_source == ROTTENTOMATOES_AUDIENCE_METER_SOURCE:
                this_video_message.rottentomatoes_audience_meter_review = this_review

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

