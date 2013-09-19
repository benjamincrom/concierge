#!/usr/bin/python
review_blocks = open('Reviews_Roger_Ebert.html').read().split('<figure class="movie review">')

class Review:
  def __init__(self, name, star_rating, poster_file, review_link):
    self.name = name
    self.star_rating = star_rating
    self.poster_file = poster_file
    self.review_link = review_link
    
for block in review_blocks:
   
