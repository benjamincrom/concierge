__author__ = 'bcrom'

from google.appengine.ext import ndb

class Video(ndb.Model):
    title = ndb.StringProperty()
    tagline = ndb.StringProperty()
