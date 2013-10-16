__author__ = 'bcrom'

from google.appengine.ext import db
from google.appengine.api import users

class Video(ndb.Model):
    title = ndb.StringProperty()
    tagline = ndb.StringProperty()


v = Video(title="test", tagline="lol")
v.put()
