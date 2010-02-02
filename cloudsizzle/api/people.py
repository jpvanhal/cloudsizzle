import time
from cloudsizzle.kp import SIBConnection, Triple, bnode, uri, literal
from cloudsizzle.asi import sib_agent
from cloudsizzle import pool
from cloudsizzle.singletonmixin import Singleton
import collections,threading
from cloudsizzle.utils import make_graph
from cloudsizzle.api.ResponseHandler import RegisterResponseHandler

RDF_BASE_URI = 'http://cos.alpha.sizl.org/people/'

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
    token = handler.do_request(request_type= 'RegisterRequest', username = username,password = password,email = email)
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

    Example:
    >>> get("azZ1LaRdCr3OiIaaWPfx7J")
    {
                'website': 'None',
                'username': 'pang1',
                'name': 'None',
                'gender': 'None',
                'is_association': 'None',
                'updated_at': '2009-11-30T08:46:58Z',
                'birthdate': 'None',
                'msn_nick': 'None',
                'status': {'message': 'None', 'changed': 'None'},
                'irc_nick': 'None',
                'connection': 'you',
                'role': 'user',
                'avatar': {'status': 'not_set', 'link': {'href': '/people/dRq9He3yWr3QUKaaWPEYjL/@avatar', 'rel': 'self'}},
                'address': None,
                'phone_number': 'None',
                'email': 'testman1@example.com',
                'description': 'None'
    }


    """
    QUERY_WITH_UID = Triple(uri(RDF_BASE_URI+'ID#'+str(user_id)),
                           None,
                           None)
    with pool.get_connection() as querySc:
        all_information = querySc.query(QUERY_WITH_UID)
    if not all_information:
        raise UserDoesNotExist
    informationDic = sib_agent.to_struct(all_information)
    return informationDic
    pass

def get_all():
    """Return all the users' uid.

    Example:
    >>> get_all()
    """
    QUERY_USERS = Triple(None,
                           None,
                           uri('http://cos.alpha.sizl.org/people#Person'))
    with pool.get_connection() as querySc:
        all_users = querySc.query(QUERY_USERS)
    if all_users:
        uids = []
        for user in all_users:
            uid = user.subject.split('http://cos.alpha.sizl.org/people/ID#')[1]
            uids.append(uid)
        return uids
    return None
    pass

def get_friends(user_id):
    """Get a list of user's friends.

    Arguments:
    user_id -- The user id of the user.

    """
    COS_ALPHA_URI_BASE = "http://cos.alpha.sizl.org/people/"
    # This needs to go, but at least it is contained within API
    SIZZLE_PEOPLE_BASE = "http://cloudsizzle.cs.hut.fi/onto/people/"

    with SIBConnection('People gatherer', method='preconfigured') as sc:
      t1 = time.time()
      friend_ids = [ str(triple.object)[len(SIZZLE_PEOPLE_BASE):] for triple in sc.query(Triple(SIZZLE_PEOPLE_BASE + user_id, "has_friend",None)) ]
      t2 = time.time()

    print 'SIB took %0.3f ms' % ((t2-t1)*1000.0)

    return friend_ids

def search(query):
    """Return users based on their real names and usernames.

    Arguments:
    query -- The search term. Every user whose name or user name contains the
             query string will be returned.

    """
    with SIBConnection('People gatherer', method='preconfigured') as sc:
        query = query.lower()

      # This duplicates users (it looks both in name & username). FIXME
        t1 = time.time()
        usernames = sc.query(Triple(None,"http://cos.alpha.sizl.org/people#username",None))
        usernames.extend(sc.query(Triple(None,"http://cos.alpha.sizl.org/people#name",None)))
        t2 = time.time()
        asi_ids = [ str(user.subject) for user in usernames if query in user.object.lower() ]
        t3 = time.time()

    print 'SIB took %0.3f ms' % ((t2-t1)*1000.0)
    print 'Python combine & search took %0.3f ms' % ((t3-t2)*1000.0)

    return asi_ids
if __name__ == '__main__':
    # for test
    print(create(username = 'Pang142',password = '1234567',email = "d2s@hot.com"))
