# -*- coding: utf-8 -*-
import logging
import secrets

import webapp2
import webob.multidict

from webapp2_extras import auth, sessions, jinja2
from jinja2.runtime import TemplateNotFound
from simpleauth import SimpleAuthHandler

from fluxlogic import _SensorReg
from fluxlogic import _NewData
from request_models import dataTypes

import json

class BaseRequestHandler(webapp2.RequestHandler):
  def dispatch(self):
    # Get a session store for this request.
    self.session_store = sessions.get_store(request=self.request)

    try:
      # Dispatch the request.
      webapp2.RequestHandler.dispatch(self)
    finally:
      # Save all sessions.
      self.session_store.save_sessions(self.response)

  @webapp2.cached_property
  def jinja2(self):
    """Returns a Jinja2 renderer cached in the app registry"""
    return jinja2.get_jinja2(app=self.app)

  @webapp2.cached_property
  def session(self):
    """Returns a session using the default cookie key"""
    return self.session_store.get_session()

  @webapp2.cached_property
  def auth(self):
      return auth.get_auth()

  @webapp2.cached_property
  def current_user(self):
    """Returns currently logged in user"""
    user_dict = self.auth.get_user_by_session()
    return self.auth.store.user_model.get_by_id(user_dict['user_id'])

  @webapp2.cached_property
  def logged_in(self):
    """Returns true if a user is currently logged in, false otherwise"""
    return self.auth.get_user_by_session() is not None

  def render(self, template_name, template_vars={}):
    # Preset values for the template
    values = {
      'url_for': self.uri_for,
      'logged_in': self.logged_in,
      'flashes': self.session.get_flashes()
    }

    # Add manually supplied template values
    values.update(template_vars)

    # read the template or 404.html
    try:
      self.response.write(self.jinja2.render_template(template_name, **values))
    except TemplateNotFound:
      self.abort(404)

  def head(self, *args):
    """Head is used by Twitter. If not there the tweet button shows 0"""
    pass

class RootHandler(BaseRequestHandler):
  def get(self):
    if self.logged_in:
      self.redirect('/profile')
    else:
      self.redirect('/')

class ProfileHandler(BaseRequestHandler):
  def get(self):
    """Handles GET /profile"""
    if self.logged_in:
      self.render('profile.html', {
        'user': self.current_user,
        'session': self.auth.get_user_by_session()
      })
    else:
      self.redirect('/')

class AuthHandler(BaseRequestHandler, SimpleAuthHandler):
  """Authentication handler for all kinds of auth."""
  OAUTH2_CSRF_STATE = True

  USER_ATTRS = {
    'facebook': {
      'id': lambda id: ('avatar_url', FACEBOOK_AVATAR_URL.format(id)),
      'name': 'name',
      'link': 'link'
    },
    'google': {
      'picture': 'avatar_url',
      'name': 'name',
      'profile': 'link',
      'email':'email'
    },
    'googleplus': {
      'image': lambda img: ('avatar_url', img.get('url', DEFAULT_AVATAR_URL)),
      'displayName': 'name',
      'url': 'link'
    }
  }

  def _on_signin(self, data, auth_info, provider, extra=None):
    """Callback whenever a new or existing user is logging in.
    data is a user info dictionary.
    auth_info contains access token or oauth token and secret.
    extra is a dict with additional params passed to the auth init handler.

    See what's in it with e.g. logging.info(auth_info)
    """
    logging.debug('Got user data: %s', str(data))

    auth_id = '%s:%s' % (provider, data['id'])

    logging.debug('Looking for a user with id %s', auth_id)
    user = self.auth.store.user_model.get_by_auth_id(auth_id)
    _attrs = self._to_user_model_attrs(data, self.USER_ATTRS[provider])

    if user:
      logging.debug('Found existing user to log in')
      # Existing users might've changed their profile data so we update our
      # local model anyway. This might result in quite inefficient usage
      # of the Datastore, but we do this anyway for demo purposes.
      #
      # In a real app you could compare _attrs with user's properties fetched
      # from the datastore and update local user in case something's changed.
      user.populate(**_attrs)
      user.put()
      self.auth.set_session(self.auth.store.user_to_dict(user))

    else:
      # check whether there's a user currently logged in
      # then, create a new user if nobody's signed in,
      # otherwise add this auth_id to currently logged in user.

      if self.logged_in:
        logging.debug('Updating currently logged in user')

        u = self.current_user
        u.populate(**_attrs)
        # The following will also do u.put(). Though, in a real app
        # you might want to check the result, which is
        # (boolean, info) tuple where boolean == True indicates success
        # See webapp2_extras.appengine.auth.models.User for details.
        u.add_auth_id(auth_id)

      else:
        logging.debug('Creating a brand new user')
        ok, user = self.auth.store.user_model.create_user(auth_id, **_attrs)
        if ok:
          self.auth.set_session(self.auth.store.user_to_dict(user))

    # user profile page
    destination_url = '/profile'
    if extra is not None:
      params = webob.multidict.MultiDict(extra)
      destination_url = str(params.get('destination_url', '/profile'))
    return self.redirect(destination_url)

  def logout(self):
    self.auth.unset_session()
    self.redirect('/')

  def handle_exception(self, exception, debug):
    logging.error(exception)
    self.render('error.html', {'exception': exception})

  def _callback_uri_for(self, provider):
    return self.uri_for('auth_callback', provider=provider, _full=True)

  def _get_consumer_info_for(self, provider):
    """Returns a tuple (key, secret) for auth init requests."""
    return secrets.AUTH_CONFIG[provider]

  def _get_optional_params_for(self, provider):
    """Returns optional parameters for auth init requests."""
    return secrets.AUTH_OPTIONAL_PARAMS.get(provider)
    
  def _to_user_model_attrs(self, data, attrs_map):
    """Get the needed information from the provider dataset."""
    user_attrs = {}
    for k, v in attrs_map.iteritems():
      attr = (v, data.get(k)) if isinstance(v, str) else v(data.get(k))
      user_attrs.setdefault(*attr)

    return user_attrs
  def _test(self, data, auth_info, extra=None):
    pass

class DataSubmit(webapp2.RequestHandler):
  def post(self):
    b = json.loads(self.request.body)
    temp=0
    mlUsed=0
    if b['datatype'] == 'JSON':
      runningTotal=0
      for i in xrange(len(b['rawData'])):
        runningTotal+= b['rawData'][i]['temperature']
      temp= runningTotal/(len(b['rawData']))
      mlUsed= b['rawData'][len(b['rawData'])-1]['temperature']
    else:
      mlUsed= b['aggData']['mlUsed']
      temp= b['aggData']['avgTemperature']
    state = _NewData(b['uniqueId'], temp, mlUsed)
    status=""
    if state:
      status="Success"
    else:
      status="Failure"
    self.response.write(status)

    