"""This module contains the ASI client service knowledge processor.

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
