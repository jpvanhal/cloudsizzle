"""
This module contains CloudSizzle API functions related to people.

"""
from itertools import chain
from cloudsizzle.kp import Triple, uri
from cloudsizzle import pool
from cloudsizzle.utils import fetch_rdf_graph
from cloudsizzle.api.ResponseHandler import RegisterResponseHandler

PEOPLE_BASE_URI = 'http://cos.alpha.sizl.org/people'

class UserAlreadyExists(Exception):
    pass

class UserDoesNotExist(Exception):
    pass

def create(username, password, email):
    """Create a new user.

    Arguments:
    username -- The desired username. Must be unique in the system. Length
                4-20 characters.
    password -- User's password.
    email -- User's email address.

    Exceptions:
    ValueError -- Given parameters were invalid.

    """
    handler = RegisterResponseHandler.getInstance()
    token = handler.do_request(username=username, password=password, email=email)
    request_id = token[0]
    lock = token[1]
    lock.acquire()
    result = handler.get_result(request_id)
    if result.startswith('messages'): # failed
        raise ValueError(result)
    return result                     # return UID

def get(user_id):
    """Get the information of the user specified by user_id.

    Arguments:
    user_id -- User's user id

    Exceptions:
    UserDoesNotExist -- User with specified user_id does not exist.

    """
    user_uri = '{0}/ID#{1}'.format(PEOPLE_BASE_URI, user_id)
    user = fetch_rdf_graph(user_uri, dont_follow=[
        '{0}#Friend'.format(PEOPLE_BASE_URI)])
    if not user:
        raise UserDoesNotExist(user_id)
    return user

def get_all():
    """Return a list of user_ids of all users.

    """
    uids = []
    with pool.get_connection() as sc:
        triples = sc.query(Triple(None, 'rdf:type',
            uri('{0}#Person'.format(PEOPLE_BASE_URI))))
        for triple in triples:
            uid = triple.subject.split('#')[-1]
            uids.append(uid)
    return uids


def get_friends(user_id):
    """Get a list of user's friends.

    Arguments:
    user_id -- The user id of the user.

    """
    friend_ids = []
    with pool.get_connection() as sc:
        friend_triples = sc.query(Triple(
            '{0}/ID#{1}'.format(PEOPLE_BASE_URI, user_id),
            '{0}#Friend'.format(PEOPLE_BASE_URI), None))
        for triple in friend_triples:
            friend_id = triple.object.split('#')[-1]
            friend_ids.append(friend_id)

    return friend_ids

def search(query):
    """Return users based on their real names and usernames.

    Arguments:
    query -- The search term. Every user whose name or user name contains the
             query string will be returned.

    """
    with pool.get_connection() as sc:
        query = query.lower()

        user_ids = set()

        username_triples = sc.query(
            Triple(None, '{0}#username'.format(PEOPLE_BASE_URI), None))
        unstructured_triples = sc.query(
            Triple(None, '{0}#unstructured'.format(PEOPLE_BASE_URI), None))

        for triple in chain(username_triples, unstructured_triples):
            name = str(triple.object)
            if query in name.lower():
                if triple.predicate.endswith('unstructured'):
                    name_triples = sc.query(Triple(None,
                        '{0}#name'.format(PEOPLE_BASE_URI),
                        triple.subject))
                    user_uri = name_triples[0].subject
                else:
                    user_uri = triple.subject

                namespace, uid = user_uri.split('#')
                user_ids.add(uid)

        return list(user_ids)
