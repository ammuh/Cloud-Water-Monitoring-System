from google.appengine.ext import ndb
import webapp2_extras.appengine.auth.models as auth_models

#class FLuxUser(ndb.Model):
  # Sensor Entity Group
class sessIdPointers(ndb.Model):
  SessionId= ndb.StringProperty()

class FluxSensors(ndb.Model):
  Ip= ndb.IntegerProperty()
  Mac=ndb.StringProperty()
  ConsumId= ndb.StringProperty()
  Type= ndb.StringProperty()
  Privacy= ndb.StringProperty()
  bqpointer= ndb.StringProperty()
  lock= ndb.BooleanProperty()
# Sensor Sessions Entity Group
class FluxSessions(ndb.Model):
  Time= ndb.TimeProperty(auto_now_add=True)
  uId= ndb.StringProperty()
  Date= ndb.DateProperty(auto_now_add=True)
  AverageTemp= ndb.FloatProperty()
  mlUsed= ndb.FloatProperty()
#User Class
class Users(auth_models.User):
  email= ndb.StringProperty()
  name= ndb.StringProperty()
  Sensors= ndb.KeyProperty(repeated=True)