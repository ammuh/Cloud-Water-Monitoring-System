import endpoints
import os
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
from request_models import SensorDataResponse
from request_models import SensorDataForm
from request_models import RawSensorData
from request_models import UserRegForm
from request_models import UserRegResponse
from request_models import GetDataResponse
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