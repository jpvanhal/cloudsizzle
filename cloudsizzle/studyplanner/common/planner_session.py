# -*- coding: utf-8 -*-
#
# Copyright (c) 2009-2010 CloudSizzle Team
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""
Classes/functions related to global session management in the studyplanner.

"""
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from cloudsizzle import api


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
    asi_session = api.Session(username, password)
    # This will throw exception for invalid username
    # Let's say the caller will handle it.
    asi_session.open()

    request.session['asi_session'] = asi_session
