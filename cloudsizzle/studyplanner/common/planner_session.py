"""
Classes/functions related to global session management in the studyplanner.

"""
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from api import Session


def check_authentication(func):
    """Decorator that checks if the user is authenticated. If not, they are
    returned the login page.

    """
    def wrapped(request, *args, **kwargs):
        if is_authenticated(request):
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('frontpage'))
    return wrapped


def is_authenticated(request):
    """Checks if the user is authenticated. Returns True/False"""
    return 'asi_session' in request.session


def authenticate(request, username, password):
    """Tries to authenticate user.

    Status of authentication can be checked with is_authenticated()
    Will also pass through LoginFailed exception from api

    This is still a dummy that will authenticate anyone with any password

    """
    # Call the ASI authentication functions here
    asi_session = Session(username, password)
    # This will throw exception for invalid username
    # Let's say the caller will handle it.
    asi_session.open()

    request.session['asi_session'] = asi_session
