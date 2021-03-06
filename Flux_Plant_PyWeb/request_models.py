from protorpc import messages
from protorpc import message_types
from protorpc import remote

#Registering new sensors
class snsTypes(messages.Message):
  fluid = messages.BooleanField(1)
  temperature = messages.BooleanField(2)
    
class RegSensorForm(messages.Message):
  ip = messages.IntegerField(1)
  mac = messages.StringField(2)
  uniqueId = messages.StringField(3)
  sensorType = messages.MessageField(snsTypes, 4)

class RegSensorResponse(messages.Message):
  uniqueId = messages.StringField(1)
  senstype = messages.StringField(2)

#Handling Session Data
class dataTypes(messages.Enum):
  JSON = 1
  AGG = 2

class sessionDataRaw(messages.Message):
  time= messages.IntegerField(1, required=True)
  flowRate= messages.FloatField(2, required=True)
  mlUsed= messages.FloatField(3, required=True)
  temperature= messages.FloatField(4, required=True)

class sessionDataAgg(messages.Message):
  mlUsed= messages.FloatField(1, required=True)
  avgTemperature= messages.FloatField(4, required=True)

class sessionDataSubmit(messages.Message):
  uniqueId= messages.StringField(1, required=True)
  datatype= messages.EnumField(dataTypes, 3, required=True)
  rawData= messages.MessageField(sessionDataRaw, 4, repeated=True)
  aggData= messages.MessageField(sessionDataAgg, 5)

class sessionDataSubResponse(messages.Message):
  status= messages.StringField(1)
  dataview= messages.StringField(2)

#Getting Sensor Data
class RawSensorData (messages.Message):
  time= messages.StringField(1)
  mlUsed= messages.FloatField(2)
  avgTemperature= messages.FloatField(3)

class SensorDataForm(messages.Message):
  uniqueId=messages.StringField(1, required=True)
  message = messages.StringField(2)

class SensorDataResponse(messages.Message):
  datatype= messages.EnumField(dataTypes, 1, required=True)
  allSessions= messages.MessageField(RawSensorData, 2, repeated=True)
  message = messages.StringField(3)

#User Registration
class UserRegForm(messages.Message):
  displayName = messages.StringField(1)
  sensorIds= messages.StringField(2, repeated=True)

class UserRegResponse(messages.Message):
  userEmail = messages.StringField(1)
  status = messages.StringField(2)

#Getting User Data
class SensorDataStructure(messages.Message):
  sensorId= messages.StringField(1)
  data= messages.MessageField(RawSensorData, 2, repeated=True)

class GetDataResponse(messages.Message):
  userEmail= messages.StringField(1)
  DataBySensors= messages.MessageField(SensorDataStructure, 2, repeated=True)
