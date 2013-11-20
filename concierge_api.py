#!/usr/bin/python


import endpoints

from protorpc import message_types
from protorpc import messages
from protorpc import remote

import models


REQUEST_RESOURCE_CONTAINER = endpoints.ResourceContainer(
    message_types.VoidMessage,
    request_id=messages.StringField(2, required=True)
)


@endpoints.api(name="concierge", version="v1")
class ConciergeApi(remote.Service):
    """Concierge API v1."""
    @staticmethod
    @endpoints.method(message_types.VoidMessage, models.VideoMessageCollection,
                      path="concierge_list", http_method="GET", name="videos.listVideos")
    def list_videos(self, unused_request):
        video_message_collection_obj = models.VideoMessageCollection(video_list=[])
        video_query = models.Video.all()
        for this_query in video_query.run(limit=100):
            video_message_collection_obj.video_list.append(self.get_video_message_from_query_obj(this_query))
        
        return video_message_collection_obj

    @staticmethod
    @endpoints.method(REQUEST_RESOURCE_CONTAINER, models.VideoMessage,
                      path="concierge_display/{request_id}", http_method="GET", name="videos.displayVideo")
    def display_video(self, request):
        return models.Video.get_by_key_name(request.request_id)

    @classmethod
    def get_video_message_from_query_obj(cls, query_obj):
        # Get occupation data into a dict
        director_list_str = ""
        writer_list_str = ""
        star_list_str = ""
        for name_occupation_key in query_obj.name_occupation_key_list:
            occupation_obj = models.NameOccupation.get(name_occupation_key)
            if occupation_obj.occupation == "Director":
                director_list_str = add_comma_if_needed(director_list_str)
                director_list_str += occupation_obj.name
            elif occupation_obj.occupation == "Writer":
                writer_list_str = add_comma_if_needed(writer_list_str)
                writer_list_str += occupation_obj.name
            elif occupation_obj.occupation == "Star":
                star_list_str = add_comma_if_needed(star_list_str)
                star_list_str += occupation_obj.name

        genre_list_str = unwrap_list(query_obj.genre_list)

        # Get video data into message object
        this_video_message = models.VideoMessage(poster_url=query_obj.poster_url,
                                                 title=query_obj.title,
                                                 plot=query_obj.plot,
                                                 tagline=query_obj.tagline,
                                                 budget=query_obj.budget,
                                                 gross=query_obj.gross,
                                                 rating=query_obj.rating,
                                                 video_type=query_obj.video_type,
                                                 aspect_ratio=str(query_obj.aspect_ratio),
                                                 imdb_id=query_obj.imdb_id,
                                                 length=query_obj.length,
                                                 year=query_obj.year,
                                                 genre_list_str=genre_list_str,
                                                 writer_list_str=writer_list_str,
                                                 director_list_str=director_list_str,
                                                 star_list_str=star_list_str)

        if query_obj.score:
            this_video_message.score = round(query_obj.score, 2)

        # Get reviews into message objects
        review_obj_list = models.Review.all().ancestor(query_obj).order("review_source")

        for review_obj in review_obj_list:
            review_sample = ""
            review_sample_match = models.EBERT_REVIEW_SAMPLE_REGEX.search(review_obj.review_content)
            if review_sample_match:
                review_sample = review_sample_match.group(1).strip()

            if review_obj.review_date is None:
                review_obj.review_date = ""

            this_review = models.ReviewMessage(review_source=review_obj.review_source,
                                               review_score=round(review_obj.review_score, 2),
                                               review_author=review_obj.review_author,
                                               review_content=review_obj.review_content,
                                               review_sample=review_sample,
                                               review_date=str(review_obj.review_date))

            if review_obj.review_source == models.ROGEREBERT_REVIEW_SOURCE:
                this_video_message.ebert_review = this_review
            elif review_obj.review_source == models.METACRITIC_METASCORE_SOURCE:
                this_video_message.metacritic_metascore_review = this_review
            elif review_obj.review_source == models.METACRITIC_USERSCORE_SOURCE:
                this_video_message.metacritic_userscore_review = this_review
            elif review_obj.review_source == models.ROTTENTOMATOES_TOP_CRITICS_SOURCE:
                this_video_message.rottentomatoes_top_critics_review = this_review
            elif review_obj.review_source == models.ROTTENTOMATOES_ALL_CRITICS_SOURCE:
                this_video_message.rottentomatoes_all_critics_review = this_review
            elif review_obj.review_source == models.ROTTENTOMATOES_AUDIENCE_METER_SOURCE:
                this_video_message.rottentomatoes_audience_meter_review = this_review

        return this_video_message


def unwrap_list(this_list):
    """ Convert a python list to a comma separated string """
    return_str = ""
    for item in this_list:
        if return_str:
            return_str += ", "

        return_str += str(item)

    return return_str


def add_comma_if_needed(this_str):
    """ Append ", " only if this string is not empty """
    if this_str:
        this_str += ", "

    return this_str


api_application = endpoints.api_server([ConciergeApi])
