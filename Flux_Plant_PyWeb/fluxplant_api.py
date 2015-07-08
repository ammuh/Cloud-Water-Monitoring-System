import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
#Request Forms and Response Structures
from request_models import RegSensorForm
from request_models import snsTypes
from request_models import RegSensorResponse
from request_models import newSessionForm
from request_models import newSessionResponse
from request_models import sessionDataRaw
from request_models import sessionDataSubmit
from request_models import sessionDataSubResponse
from request_models import sessionDataAgg
from request_models import dataTypes
from request_models import SensorData
from request_models import SensorDataForm
#DataStore Structure
from data_manage import sessIdPointers #Only a Structured Property Class
from data_manage import FluxSensors
from data_manage import FluxSessions
from google.appengine.ext import ndb
#Random String Generation
import random
import string

@endpoints.api(name='fluxplant', version='v1')
class FluxPlantApi(remote.Service):
  """FluxPlantApi v1."""

  #@endpoints.method( , , path='newSession', http_method='GET', name='sessions.newSession')
  #@endpoints.method( , , path='newSession', http_method='GET', name='sessions.newSession')
  #@endpoints.method( , , path='newSession', http_method='GET', name='sessions.newSession')

  #Registering new sensor in network
  @endpoints.method(RegSensorForm, RegSensorResponse, path='RegSensor', http_method='POST', name='sensors.RegSensor')
  def RegSensor(self, request):
    #TODO: Add functionality to store all request data in datastore
    privacy="Private"
    
    if request.sensorType.fluid == True and request.sensorType.temperature == True:
      senstype="Fluid and Temperature"
    elif request.sensorType.fluid == True and request.sensorType.temperature == False:
      senstype="Fluid"
    elif request.sensorType.fluid == False and request.sensorType.temperature == True:
      senstype="Temperature"
    sensId= FluxSensors.allocate_ids(size=1)[0]
    sensorKey= ndb.Key('FluxSensors', sensId)
    rando = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(10)])
    conId= rando + "-" + str(sensId)
    newSensor= FluxSensors(key= sensorKey, Ip=request.ip, ConsumId=conId, Type=senstype, Privacy=privacy)
    newSensor.put()
     #TODO create unique id and return in body
    #TODO save key in datastore
    return RegSensorResponse(uniqueId= str(conId), senstype=senstype)

  @endpoints.method(newSessionForm, newSessionResponse, path='NewSession', http_method='POST', name='sessions.New')
  def NewSession(self, request):
    #TODO Create New Session Key
    sensor = FluxSensors.query(FluxSensors.ConsumId == request.uniqueId).fetch(1)[0]
    sensKey= ndb.Key(FluxSensors, sensor.key.id())
    sessId = FluxSessions.allocate_ids(size=1, parent=sensKey)[0]
    sessKey= ndb.Key(FluxSessions, sessId, parent=sensKey)

    rando = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(10)])
    cId= rando + "-" + str(sessId)

    newSession= FluxSessions(key=sessKey, uId=request.uniqueId, clientToken=cId)
    newSession.put()

    #Save Session Key in Datastore along with provided Unique ID
    #Return Session Key
    return newSessionResponse(clientToken=cId)

  @endpoints.method(sessionDataSubmit, sessionDataSubResponse, path='DataSubmit', http_method='POST', name='sessions.DataSubmit')
  def DataSubmit(self, request):
    session = FluxSessions.query(FluxSessions.clientToken == request.clientToken).fetch(1)[0]
    temp=3
    mlUsed=123
    runningTotal=0
    if request.datatype == dataTypes.JSON:
      for i in xrange(len(request.rawData)):
        runningTotal+= request.rawData[i].temperature
      temp= runningTotal/(len(request.rawData))
      mlUsed= request.rawData[len(request.rawData)-1].mlUsed
    else:
      mlUsed= request.aggData.mlUsed
      temp= request.aggData.avgTemperature
    session.AverageTemp= temp
    session.mlUsed= mlUsed
    session.put()
    return sessionDataSubResponse(status="Some Response Status", dataview="Link to data")
  #Aggregating SensorData and returning in JSON dataset
  @endpoints.method(SensorDataForm,SensorDataResponse, path'GetSensData', http_method='POST', name='sessions.GetSensData')
  def GetSensData(self, request):

    resp= SensorDataResponse
    return resp
 # @endpoints.method(newSessionRequestForm, newSessionResponse, path='NewSession', http_method='POST', name='sessions.newSession')
 # def session_request(self, request):
 #   return newSessionResponse(message1= request.device_id, message2= request.info)

  #@endpoints.method( , , path='sessionData', http_method='POST', name='sessions.dataSend')
 # def session_request(self):
#    return 


APPLICATION = endpoints.api_server([FluxPlantApi])