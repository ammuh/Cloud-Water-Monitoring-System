from google.appengine.ext import ndb

#class FLuxUser(ndb.Model):
# Sensor Entity Group
class sessIdPointers(ndb.Model):
  SessionId= ndb.StringProperty()

class FluxSensors(ndb.Model):
  Ip= ndb.IntegerProperty()
  ConsumId= ndb.StringProperty()
  Type= ndb.StringProperty()
  Privacy= ndb.StringProperty()
  bqpointer= ndb.StringProperty()
  SessionIdPointers= ndb.StructuredProperty(sessIdPointers, repeated=True)
# Sensor Sessions Entity Group
class FluxSessions(ndb.Model):
  Time= ndb.TimeProperty(auto_now_add=True)
  clientToken= ndb.StringProperty() 
  uId= ndb.StringProperty()
  Date= ndb.DateProperty(auto_now_add=True)
  AverageTemp= ndb.FloatProperty()
  mlUsed= ndb.FloatProperty()
