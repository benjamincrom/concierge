

import endpoints
import models

from protorpc import messages
from protorpc import message_types
from protorpc import remote


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


@endpoints.api(name='concierge', version='v1')
class ConciergeApi(remote.Service):
    """Concierge API v1."""

    @staticmethod
    @endpoints.method(message_types.VoidMessage, VideoMessageCollection,
                      path='concierge', http_method='GET', name='videos.listVideos')
    def list_videos(self, unused_request):
        video_message_collection_obj = VideoMessageCollection(video_list=[])
        video_query = models.Video.all()
        for q in video_query.run(limit=50):
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
                                              score=q.score,
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
                                            review_score=review_obj.review_score,
                                            review_author=review_obj.review_author,
                                            review_content=review_obj.review_content,
                                            review_date=str(review_obj.review_date))
                this_video_message.review_list.append(this_review)

            video_message_collection_obj.video_list.append(this_video_message)

        return video_message_collection_obj


def unwrap_list(this_list):
    return_str = ''
    for item in this_list:
        if return_str:
            return_str += ', '

        return_str += item

    return return_str


application = endpoints.api_server([ConciergeApi])

