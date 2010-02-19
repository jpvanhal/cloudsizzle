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
This module contains the ASI client service knowledge processor.

Example usage:

    >>> from cloudsizzle.api.asi_client import get_service()
    >>> login_service = get_service('Login')
    >>> # Do something with the login service

"""
from cloudsizzle.asi.service import ASIServiceKnowledgeProcessor
from cloudsizzle.asi.client import LoginClient, LogoutClient, LogoutClient, \
    RegisterClient, RejectFriendRequestClient, RemoveFriendsClient, \
    AddFriendsClient
from cloudsizzle.kp import SIBConnection

ASI_CLIENT = None

def _init():
    """Initializes ASI service client knowledge processor."""
    global ASI_CLIENT

    sc = SIBConnection('ASI service client', method='preconfigured')
    sc.open()

    ASI_CLIENT = ASIServiceKnowledgeProcessor(services=(
       LoginClient(sc),
       LogoutClient(sc),
       RegisterClient(sc),
       RejectFriendRequestClient(sc),
       RemoveFriendsClient(sc),
       AddFriendsClient(sc),
    ))

def get_service(name):
    """Return the service client instance with the given name."""
    if not ASI_CLIENT:
        _init()
    return ASI_CLIENT[name]
