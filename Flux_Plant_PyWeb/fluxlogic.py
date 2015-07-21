import endpoints
import os
from protorpc import messages
from protorpc import message_types
from protorpc import remote
#DataStore Structure
from data_manage import sessIdPointers #Only a Structured Property Class
from data_manage import FluxSensors
from data_manage import FluxSessions
from data_manage import Users
from google.appengine.ext import ndb
#Random String Generation
import random
import string
#Gplus Auth Util
#import auth_util
#OAUTH
from google.appengine.api import oauth
WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID

#Sessions
def _NewData(uId, temp, mL):
  snsrKey = FluxSensors.query(FluxSensors.ConsumId == uId).fetch(1)[0].key
  sid= FluxSessions.allocate_ids(size=1, parent=snsrKey)[0]
  sessKey = ndb.Key('FluxSessions', sid, parent= snsrKey)
  session = FluxSessions(uId= uId, AverageTemp= temp, mlUsed=mL, key=sessKey)
  state = False
  if session.put() == False:
    state = False
  else:
    state = True
  return state
#Sensors
def _SensorReg(attrs):
  cid= ""
  if attrs.get('ConsumId', None) != None:
    snsr = FluxSensors.query(FluxSensors.ConsumId == attrs.get('ConsumId')).fetch(1)[0]
    if attrs.get('name', None) != None:
      snsr.name = attrs.get('name')
    if attrs.get('location', None) != None:
      snsr.location = attrs.get('location')
    if attrs.get('sublocation', None) != None:
      snsr.sublocation = attrs.get('sublocation')
    snsr.put()
    cid= "Registered"
  else:
    snsr = FluxSensors()
    if attrs.get('name', None) != None:
      snsr.name = attrs.get('Ip')
    if attrs.get('Ip', None) != None:
      snsr.Ip = attrs.get('Ip')
    if attrs.get('Type', None) != None:
      snsr.Type = attrs.get('Type')
    if attrs.get('Privacy', None) != None:
      snsr.Privacy = attrs.get('Privacy')
    if attrs.get('mac', None) != None:
      snsr.Mac = attrs.get('mac') 
    if attrs.get('location', None) != None:
      snsr.location = attrs.get('location')
    if attrs.get('sublocation', None) != None:
      snsr.sublocation = attrs.get('sublocation')  
    snsrId= FluxSensors.allocate_ids(size=1)[0]
    snsrKey= ndb.Key('FluxSensors', snsrId)
    rando = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(10)])
    conId= rando + "-" + str(snsrId)
    snsr.ConsumId= conId
    snsr.key = snsrKey
    snsr.put()
    cid=conId
  return cid