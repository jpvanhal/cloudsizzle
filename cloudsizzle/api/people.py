"""
This module contains CloudSizzle API functions related to people.

"""
from itertools import chain
from cloudsizzle.kp import Triple, uri
from cloudsizzle import pool
from cloudsizzle.utils import fetch_rdf_graph
from cloudsizzle.api.ResponseHandler import RegisterResponseHandler

PEOPLE_BASE_URI = 'http://cos.alpha.sizl.org/people/'

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
    user_uri = '%sID#%s' % (PEOPLE_BASE_URI, user_id)
    user = fetch_rdf_graph(user_uri)
    if not user:
        raise UserDoesNotExist(user_id)
    return user

def get_all():
    """Return a list of user_ids of all users.

    """
    uids = []
    with pool.get_connection() as sc:
        triples = sc.query(Triple(None, 'rdf:type',
            uri('http://cos.alpha.sizl.org/people#Person')))
        for triple in triples:
            uid = triple.subject.split('#')[-1]
            uids.append(uid)
    return uids


def get_friends(user_id):
    """Get a list of user's friends.

    Arguments:
    user_id -- The user id of the user.

    """
    # This needs to go, but at least it is contained within API
    SIZZLE_PEOPLE_BASE = "http://cloudsizzle.cs.hut.fi/onto/people/"

    with pool.get_connection() as sc:
        friend_triplets = sc.query(Triple(SIZZLE_PEOPLE_BASE + user_id,
            'has_friend', None))
        friend_ids = [str(triplet.object)[len(SIZZLE_PEOPLE_BASE):]
            for triplet in friend_triplets]

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
            Triple(None, 'http://cos.alpha.sizl.org/people#username', None))
        unstructured_triples = sc.query(
            Triple(None, 'http://cos.alpha.sizl.org/people#unstructured', None))

        for triple in chain(username_triples, unstructured_triples):
            name = str(triple.object)
            if query in name.lower():
                if triple.predicate.endswith('unstructured'):
                    name_triples = sc.query(Triple(None,
                        'http://cos.alpha.sizl.org/people#name',
                        triple.subject))
                    user_uri = name_triples[0].subject
                else:
                    user_uri = triple.subject

                namespace, uid = user_uri.split('#')
                user_ids.add(uid)

        return list(user_ids)
    
    """
    Friends are stored in ASI and moved through SIB
    """

    def add_friend(self, friend_id):
        """Adds a new friend connection to this user.

        Arguments:
        friend_id -- The user id of the friend being requested.

        """
        pass

    def remove_friend(self, friend_id):
        """Removes a friend connection.

        Arguments:
        friend_id -- The user id of the friend being broken up with.

        """
        pass
    def get_friend_uids(self, user_id):
        """
        get all friends' uids.
        return a list of friend_uids:
               
        """
        friend_uids = []
        with pool.get_connection() as sc:
            user_uri = '%sID#%s' % (PEOPLE_BASE_URI, user_id)
            triples = sc.query(Triple(user_uri, 'rdf:type',
                uri('http://cos.alpha.sizl.org/people#Friend'),None))
            for triple in triples:
                uid = triple.subject.split('#')[-1]
                friend_uids.append(uid)
        return friend_uids
        
    def get_pending_friend_requests(self):
        """Returns a list of people who have requested to connect to this user.

        A friend request is accepted by making the same request in the opposite
        direction.

        Example:
        #>>> with Session("pang1", "123456") as session:
        #...     session.get_pending_friend_requests()
        #...
        ["azAC7-RdCr3OiIaaWPfx7J", "azEe6yRdCr3OiIaaWPfx7J"]

        """
        pass

    def reject_friend_request(self, friend_id):
        """Rejects a friend request.

        Arguments:
        friend_id -- User id of the friend whose request this user is rejecting

        """
        pass