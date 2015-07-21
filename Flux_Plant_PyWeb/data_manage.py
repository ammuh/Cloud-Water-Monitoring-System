from google.appengine.ext import ndb
import webapp2_extras.appengine.auth.models as auth_models

#class FLuxUser(ndb.Model):
  # Sensor Entity Group
class sessIdPointers(ndb.Model):
  SessionId= ndb.StringProperty()

class FluxSensors(ndb.Model):
  name= ndb.StringProperty()
  Ip= ndb.IntegerProperty()
  Mac=ndb.StringProperty()
  ConsumId= ndb.StringProperty()
  Type= ndb.StringProperty()
  Privacy= ndb.StringProperty()
  bqpointer= ndb.StringProperty()
  lock= ndb.BooleanProperty()
  location = ndb.StringProperty()
  sublocation = ndb.StringProperty()
# Sensor Sessions Entity Group
class FluxSessions(ndb.Model):
  uId= ndb.StringProperty()
  DateTime= ndb.DateTimeProperty(auto_now_add=True)
  AverageTemp= ndb.FloatProperty()
  mlUsed= ndb.FloatProperty()
#User Class
class Users(auth_models.User):
  email= ndb.StringProperty()
  name= ndb.StringProperty()
  Sensors= ndb.StringProperty(repeated=True)
  locations= ndb.StringProperty(repeated=True)
  sublocations= ndb.StringProperty(repeated=True)