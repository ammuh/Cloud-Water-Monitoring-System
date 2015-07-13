# -*- coding: utf-8 -*-
import logging
import secrets

import webapp2
import webob.multidict

from webapp2_extras import auth, sessions, jinja2
from jinja2.runtime import TemplateNotFound

from simpleauth import SimpleAuthHandler

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

class ProfileHandler(BaseRequestHandler):
  def get(self):
    """Handles GET /profile"""
    if self.logged_in:
      self.render('index.html', {
        'user': self.current_user,
        'session': self.auth.get_user_by_session()
      })
    else:
      self.redirect('/login')

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
      'profile': 'link'
    },
    'googleplus': {
      'image': lambda img: ('avatar_url', img.get('url', DEFAULT_AVATAR_URL)),
      'displayName': 'name',
      'url': 'link'
    },
    'windows_live': {
      'avatar_url': 'avatar_url',
      'name': 'name',
      'link': 'link'
    },
    'twitter': {
      'profile_image_url': 'avatar_url',
      'screen_name': 'name',
      'link': 'link'
    },
    'linkedin': {
      'picture-url': 'avatar_url',
      'first-name': 'name',
      'public-profile-url': 'link'
    },
    'linkedin2': {
      'picture-url': 'avatar_url',
      'first-name': 'name',
      'public-profile-url': 'link'
    },
    'foursquare': {
      'photo': lambda photo: ('avatar_url', photo.get('prefix') + '100x100'\
                                          + photo.get('suffix')),
      'firstName': 'firstName',
      'lastName': 'lastName',
      'contact': lambda contact: ('email', contact.get('email')),
      'id': lambda id: ('link', FOURSQUARE_USER_LINK.format(id))
    },
    'openid': {
      'id': lambda id: ('avatar_url', DEFAULT_AVATAR_URL),
      'nickname': 'name',
      'email': 'link'
    }
  }

  def _on_signin(self, data, auth_info, provider, extra=None):
    """Callback whenever a new or existing user is logging in.
    data is a user info dictionary.
    auth_info contains access token or oauth token and secret.
    extra is a dict with additional params passed to the auth init handler.

    See what's in it with e.g. logging.info(auth_info)
    """
    logging.info(data)
    auth_id = '%s:%s' % (provider, data['id'])

    # Possible flow:
    # 
    # 1. check whether user exist, e.g.
    #    User.get_by_auth_id(auth_id)
    #
    # 2. create a new user if it doesn't
    #    User(**data).put()
    #
    # 3. sign in the user
    #    self.session['_user_id'] = auth_id
    #
    # 4. redirect somewhere, e.g. self.redirect('/profile')
    #
    # See more on how to work the above steps here:
    # http://webapp-improved.appspot.com/api/webapp2_extras/auth.html
    # http://code.google.com/p/webapp-improved/issues/detail?id=20
    logging.debug('Looking for a user with id %s', auth_id)
    user = self.auth.store.user_model.get_by_auth_id(auth_id)
    _attrs = self._to_user_model_attrs(data, self.USER_ATTRS[provider])
    self.auth.set_session(self.auth.store.user_to_dict(user))
    self.redirect('/fp/profile')

  def logout(self):
    self.auth.unset_session()
    self.redirect('/login')

  def _callback_uri_for(self, provider):
    return self.uri_for('auth_callback', provider=provider, _full=True)

  def _get_consumer_info_for(self, provider):
    """Should return a tuple (key, secret) for auth init requests.
    For OAuth 2.0 you should also return a scope, e.g.
    ('my app/client id', 'my app/client secret', 'email,user_about_me')

    The scope depends solely on the provider.
    See example/secrets.py.template
    """
    return secrets.AUTH_CONFIG[provider]