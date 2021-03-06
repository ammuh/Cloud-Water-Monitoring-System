import endpoints
import os
from protorpc import messages
from protorpc import message_types
from protorpc import remote
#Request Forms and Response Structures
from request_models import RegSensorForm
from request_models import snsTypes
from request_models import RegSensorResponse
from request_models import sessionDataRaw
from request_models import sessionDataSubmit
from request_models import sessionDataSubResponse
from request_models import sessionDataAgg
from request_models import dataTypes
from request_models import SensorDataResponse
from request_models import SensorDataForm
from request_models import RawSensorData
from request_models import UserRegForm
from request_models import UserRegResponse
from request_models import GetDataResponse
from request_models import SensorDataStructure
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
#Logic
from fluxlogic import _SensorReg
from fluxlogic import _NewData
WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID

@endpoints.api(name='fluxplant', version='v1', scopes=[endpoints.EMAIL_SCOPE])
class FluxPlantApi(remote.Service):
  """FluxPlantApi v1."""

  #Registering new sensor in network
  @endpoints.method(RegSensorForm, RegSensorResponse, path='RegSensor', http_method='POST', name='sensors.RegSensor')
  def RegSensor(self, request):
    #TODO: Add functionality to store all request data in datastore
    privacy="Private" 
    senstype=""
    if request.sensorType.fluid == True and request.sensorType.temperature == True:
      senstype="Fluid and Temperature"
    elif request.sensorType.fluid == True and request.sensorType.temperature == False:
      senstype="Fluid"
    elif request.sensorType.fluid == False and request.sensodrype.temperature == True:
      senstype="Temperature"
    attrs = {'Ip':request.ip, 'Type': senstype, 'Privacy': privacy, 'ConsumId': request.uniqueId, 'mac':request.mac}
    conId=_SensorReg(attrs)
    #TODO save key in datastore
    return RegSensorResponse(uniqueId= str(conId), senstype=senstype)

  @endpoints.method(sessionDataSubmit, sessionDataSubResponse, path='DataSubmit', http_method='POST', name='sessions.DataSubmit')
  def DataSubmit(self, request):
    temp=0
    mlUsed=0
    if request.datatype == dataTypes.JSON:
      runningTotal=0
      for i in xrange(len(request.rawData)):
        runningTotal+= request.rawData[i].temperature
      temp= runningTotal/(len(request.rawData))
      mlUsed= request.rawData[len(request.rawData)-1].mlUsed
    else:
      mlUsed= request.aggData.mlUsed
      temp= request.aggData.avgTemperature
    state= _NewData(request.uniqueId, temp, mlUsed)
    response = sessionDataSubResponse()
    if state:
      response.status= "Success"
    else:
      response.status= "Fail"
    return response
  #Session and Submit Data
  #Aggregating SensorData and returning in JSON dataset
  @endpoints.method(SensorDataForm, SensorDataResponse, path='GetSensData', http_method='POST', name='sessions.GetSensData')
  def GetSensData(self, request):
    sensor = FluxSensors.query(FluxSensors.ConsumId == request.uniqueId).fetch(1)[0]
    sessQryObj = FluxSessions.query(ancestor=sensor.key).fetch()
    sessList = []
    for i in xrange(len(sessQryObj)):
      sessData = RawSensorData(time=str(sessQryObj[i].DateTime), mlUsed=sessQryObj[i].mlUsed, avgTemperature=sessQryObj[i].AverageTemp)
      sessList.append(sessData)

    return SensorDataResponse(datatype=dataTypes.JSON, allSessions=sessList, message=request.message)
  #Registering Users  
  @endpoints.method(UserRegForm, UserRegResponse, path='RegUser', http_method='POST', name='Users.RegUser')
  def RegUser(self, request):
    #Dev Server Code since OAUTH bugs up on local host when working with user

    currentUser = endpoints.get_current_user()
    userid=currentUser.user_id() # THIS RETURNS NONE, DO NOT USE IN DEPLOYMENT CODE, OK FOR TESTING
    usrKey = ndb.Key(Users, userid)
    usr = Users(key= usrKey, email=currentUser.email(), userObj=currentUser)
    if request.displayName != None and len(request.displayName) <= 4:
      usr.username= request.displayName
    else:
      usr.username= currentUser.nickname()
    snsrs=[]
    if request.sensorIds != None:
      for i in range(len(request.sensorIds)):
        qry= FluxSensors.query(FluxSensors.ConsumId == request.sensorIds[i]).fetch(1)
        snsrs.append(qry[0].key)
      usr.Sensors= snsrs
    usr.put()

    #Deployment Code
    #endpoints_user = endpoints.get_current_user()
    #if endpoints_user is None:
    #  raise endpoints.UnauthorizedException()

    #oauth_user = oauth.get_current_user(os.getenv('OAUTH_LAST_SCOPE'))
    #if oauth_user is None or oauth_user.user_id() is None:
      # This should never happen
     # raise endpoints.NotFoundException()

    #id1= endpoints_user.user_id()
    #if Users.get_by_id(id1).key.id == id1:
    #  raise endpoints.BadRequestException("User Already Exists")

    return UserRegResponse(status=str("OK"))
  #Fetch User Data
  @endpoints.method(message_types.VoidMessage, GetDataResponse, path='GetUserData', http_method='GET', name='Users.GetData')
  def GetUserData(self, request):
    user = endpoints.get_current_user()
    email = user.email()
    qryUser = Users.query(Users.email == email).fetch(1)[0]
    snsrsKeys=qryUser.Sensors
    userData=[]
    for i in range(len(snsrsKeys)):
      ConsumId= snsrsKeys[i].get().ConsumId
      sessQuery= FluxSessions.query(ancestor=snsrsKeys[i]).fetch()
      sessData=[]
      for a in range(len(sessQuery)):
        data=RawSensorData(time=str(sessQuery[a].Time), mlUsed=sessQuery[a].mlUsed, avgTemperature=sessQuery[a].AverageTemp)
        sessData.append(data)
      dataStructure= SensorDataStructure(sensorId=ConsumId, data=sessData)
      userData.append(dataStructure)    
    
    resp=GetDataResponse(userEmail=email, DataBySensors=userData)
    #for i in range(len(qryUser.Sensors)):
    #  snsrsKey=qryUser.Sensors[i]
    #  ConsumId= snsrsKey.get().ConsumId
    #  snsrs.append(ConsumId)

    return resp

APPLICATION = endpoints.api_server([FluxPlantApi])