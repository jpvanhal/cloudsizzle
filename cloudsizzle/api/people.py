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
    pass

def search(query):
    """Return users based on their real names and usernames.

    Arguments:
    query -- The search term. Every user whose name or user name contains the
             query string will be returned.

    """
    pass

def add_friend(user_id, friend_id):
    """Adds a new friend connection to a user.

    Arguments:
    user_id -- The user id of the user who adds the new friend connection.
    friend_id -- The user id of the friend being requested.

    """
    pass

def delete_friend(user_id, friend_id):
    """Removes a friend connection.

    Arguments:
    user_id -- User's user id
    friend_id -- The user id of the friend being broken up with.

    """
    pass

def get_pending_friend_requests(user_id):
    """Returns a list of people who have requested to connect to this user.

    A friend request is accepted by making the same request in the opposite
    direction.

    Arguments:
    user_id -- User's user id

    Example:
    >>> get_pending_friend_requests("azZ1LaRdCr3OiIaaWPfx7J")
    ["azAC7-RdCr3OiIaaWPfx7J", "azEe6yRdCr3OiIaaWPfx7J"]

    """
    pass

def reject_friend_request(user_id, friend_id):
    """Rejects a friend request.

    Arguments:
    user_id -- User id of the user who is rejecting a friend request
    friend_id -- User id of the friend whose request the user is rejecting

    """
    pass

def mark_as_planned_course(user_id, coursecode):
    """ adds a course to the user """
    pass

def add_to_planned_courses(user_id, coursecode):
    """ adds a course to the user """
    pass

def remove_from_planned_courses(user_id, coursecode):
    """ adds a course to the user """
    pass

def get_events(user_id):
    """Returns the events of this user."""
    pass

def get_planned_courses(user_id):
    """Returns the planned courses for this user """
    pass

def get_completed_courses(user_id):
    """Returns the completed courses for this user """
    pass

def is_planned_course(user_id, course_code):
    pass

def is_completed_course(user_id, course_code):
    pass
