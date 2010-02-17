"""Classes/functions related to global session management in the studyplanner"""
from django.http import HttpResponseRedirect
from api import Session

"""Decorator that checks if the user is authenticated. If not, they are
returned the login page.

"""
class check_authentication(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, request, *args, **kwargs):
        if 'asi_session' in request.session:
            return self.func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse(frontpage))

""" Dis is a decorator

@check_authentication
def foo():
  pass

foo = check_authentication(foo)
"""

"""Checks if the user is authenticated. Returns True/False"""
def is_authenticated(request):
    if 'asi_session' in request.session:
        return True
    else:
        return False

"""Tries to authenticate user.

Status of authentication can be checked with is_authenticated()
Will also pass through LoginFailed exception from api

This is still a dummy that will authenticate anyone with any password

"""
def authenticate(request, username, password):
    # Call the ASI authentication functions here
    asi_session = Session(username, password)
    # This will throw exception for invalid username
    # Let's say the caller will handle it.
    asi_session.open()

    request.session['asi_session'] = asi_session
