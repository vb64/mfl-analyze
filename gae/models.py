from google.appengine.ext import db

class Request(db.Model): # ANCESTOR: Client
  date = db.DateTimeProperty(auto_now_add=True, indexed=False)
  status = db.IntegerProperty(default=0)
  data = db.TextProperty(default=None)
