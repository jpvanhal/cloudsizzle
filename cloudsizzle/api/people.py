from kpwrapper import SIBConnection, Triple, bnode, uri, literal
import time

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
    UserAlreadyExists -- User with the given username already exists.

    """
    pass

def get(user_id):
    """Get the information of the user specified by user_id.

    Arguments:
    user_id -- User's user id

    Exceptions:
    UserDoesNotExist -- User with specified user_id does not exist.

    Example:
    >>> get("azZ1LaRdCr3OiIaaWPfx7J")
    {
        "name": {
          "unstructured": "Essi Esimerkki",
          "family_name": "Esimerkki",
          "given_name": "Essi"
        },
        "address": {
          "unstructured": "Yrj\u00f6-Koskisenkatu 42, 00170 Helsinki",
          "postal_code": "00170",
          "street_address": "Yrj\u00f6-Koskisenkatu 42",
          "locality": "Helsinki"
        },
        "birthdate": "1940-06-01",
        "updated_at": "2009-09-28T13:59:12Z",
        "is_association": null,
        "username": "8d6ofvkusti",
        "gender": {
          "displayvalue": "MALE",
          "key": "MALE"
        },
        "id": "azZ1LaRdCr3OiIaaWPfx7J",
        "avatar": {
          "link": {
            "href": "\/people\/azZ1LaRdCr3OiIaaWPfx7J\/@avatar",
            "rel": "self"
          },
          "status": "not_set"
        },
        "msn_nick": "maison",
        "phone_number": "+358 40 834 7176",
        "website": "http:\/\/example.com",
        "irc_nick": "pelle",
        "description": "About me",
        "status": {
          "changed": "2009-09-28T13:59:12Z",
          "message": "Valid person rocks."
        },
        "status_message": "Valid person rocks."
    }

    """
    
    sc = SIBConnection('ASI gatherer', method='preconfigured')
    
    
    pass

def get_all():
    """Return all the users.

    Example:
    >>> get_all()
      [
        {
          "name": {
            "unstructured": "Essi Esimerkki",
            "family_name": "Esimerkki",
            "given_name": "Essi"
          },
          "address": {
            "unstructured": "Yrj\u00f6-Koskisenkatu 42, 00170 Helsinki",
            "postal_code": "00170",
            "street_address": "Yrj\u00f6-Koskisenkatu 42",
            "locality": "Helsinki"
          },
          "birthdate": "1940-06-01",
          "updated_at": "2009-09-28T13:59:11Z",
          "is_association": null,
          "username": "2l6d6jkusti",
          "gender": {
            "displayvalue": "MALE",
            "key": "MALE"
          },
          "id": "azAC7-RdCr3OiIaaWPfx7J",
          "avatar": {
            "link": {
              "href": "\/people\/azAC7-RdCr3OiIaaWPfx7J\/@avatar",
              "rel": "self"
            },
            "status": "not_set"
          },
          "msn_nick": "maison",
          "phone_number": "+358 40 834 7176",
          "website": "http:\/\/example.com",
          "irc_nick": "pelle",
          "description": "About me",
          "status": {
            "changed": "2009-09-28T13:59:11Z",
            "message": "Valid person rocks."
          },
          "status_message": "Valid person rocks."
        },
        {
          "name": {
            "unstructured": "Essi Esimerkki",
            "family_name": "Esimerkki",
            "given_name": "Essi"
          },
          "address": {
            "unstructured": "Yrj\u00f6-Koskisenkatu 42, 00170 Helsinki",
            "postal_code": "00170",
            "street_address": "Yrj\u00f6-Koskisenkatu 42",
            "locality": "Helsinki"
          },
          "birthdate": "1940-06-01",
          "updated_at": "2009-09-28T13:59:11Z",
          "is_association": null,
          "username": "dv99s1kusti",
          "gender": {
            "displayvalue": "MALE",
            "key": "MALE"
          },
          "id": "azEe6yRdCr3OiIaaWPfx7J",
          "avatar": {
            "link": {
              "href": "\/people\/azEe6yRdCr3OiIaaWPfx7J\/@avatar",
              "rel": "self"
            },
            "status": "not_set"
          },
          "msn_nick": "maison",
          "phone_number": "+358 40 834 7176",
          "website": "http:\/\/example.com",
          "irc_nick": "pelle",
          "description": "About me",
          "status": {
            "changed": "2009-09-28T13:59:11Z",
            "message": "Valid person rocks."
          },
          "status_message": "Valid person rocks."
        }
      ]
    """
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
