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

#Handling New Sessions
class newSessionForm(messages.Message):
  uniqueId= messages.StringField(1, required=True)

class newSessionResponse(messages.Message):
  clientToken= messages.StringField(1)

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
  clientToken= messages.StringField(2, required=True)
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

class SensorDataResponse(messages.Message):
  datatype= messages.EnumField(dataTypes, 1, required=True)
  allSessions= messages.MessageField(RawSensorData, 2, repeated=True)