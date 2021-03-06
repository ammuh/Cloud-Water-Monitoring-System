import sys
from secrets import SESSION_KEY

from webapp2 import WSGIApplication, Route
from data_manage import Users

# inject './lib' dir in the path so that we can simply do "import ndb"
# or whatever there's in the app lib dir.
if 'lib' not in sys.path:
  sys.path[0:0] = ['lib']

# webapp2 config
app_config = {
  'webapp2_extras.sessions': {
    'cookie_name': '_simpleauth_sess',
    'secret_key': SESSION_KEY
  },
  'webapp2_extras.auth': {
    'user_model': Users
  }
}


# Map URLs to handlers
routes = [
  Route('/fp/user/sensors/form', handler='handlers.SensorForm', name='login'),
  Route('/fp/user/data', handler='handlers.UserData', name='Data'),
  Route('/fp/login', handler='handlers.Login', name='login'),
	Route('/fp/profile', handler='handlers.ProfileHandler', name='profile'),
	Route('/fp/auth/<provider>', handler='handlers.AuthHandler:_simple_auth', name='auth_login'),
	Route('/fp/auth/<provider>/callback', handler='handlers.AuthHandler:_auth_callback', name='auth_callback'),
	Route('/fp/logout', handler='handlers.AuthHandler:logout', name='logout'),
  Route('/fp/user/sensors/getSensors', handler='handlers.GetUserSensors', name='UserSensors')
]

webapp = WSGIApplication(routes, config=app_config, debug=True)

#Device App handler

routes2 = [
	Route('/device/DataSubmit', handler='handlers.DataSubmit', name='DataSubmit')
]
deviceAPI = WSGIApplication(routes2, config=app_config, debug=True)
