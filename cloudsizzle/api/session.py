from cloudsizzle.api.asi_client import get_service
from cloudsizzle.kp import Triple, uri
from cloudsizzle import pool
from cloudsizzle.api import people
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cloudsizzle.studyplanner.settings'
from cloudsizzle.studyplanner.events.models import Event

PEOPLE_BASE_URI = 'http://cos.alpha.sizl.org/people'


class LoginFailed(Exception):
    pass

class Session(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.user_id = None

    def open(self):
        """Open a new session and log in with given username and password."""
        response = get_service('Login').request(
            username=self.username, password=self.password)
        try:
            self.user_id = response['user_id']
        except KeyError:
            messages = response['messages']
            if not isinstance(messages, list):
                messages = [messages]
            raise LoginFailed(*messages)

    def close(self):
        """Close the current session and log out."""
        get_service('Logout').request(user_id=self.user_id)
        self.user_id = None

    def add_friend(self, friend_id):
        """Adds a new friend connection to this user.

        Arguments:
        friend_id -- The user id of the friend being requested.

        """
        result = get_service('AddFriendsRequest').request(user_id=self.user_id, friend_id=friend_id)
        return result
        
    def remove_friend(self, friend_id):
        """Removes a friend connection.

        Arguments:
        friend_id -- The user id of the friend being broken up with.

        """
        result = get_service('RemoveFriendsRequest').request(user_id=self.user_id, friend_id=friend_id)
        try:
            return result['result']
        except KeyError:
            return None

    def get_pending_friend_requests(self):
        """Returns a list of people who have requested to connect to this user.

        A friend request is accepted by making the same request in the opposite
        direction.

        Example:
        #>>> with Session("pang1", "123456") as session:
        #...     session.get_pending_friend_requests()
        #...
        #["azAC7-RdCr3OiIaaWPfx7J", "azEe6yRdCr3OiIaaWPfx7J"]

        """
        pending_friend_ids = []
        with pool.get_connection() as sc:
            friend_triples = sc.query(Triple(
                '{0}/ID#{1}'.format(PEOPLE_BASE_URI, self.user_id),
                '{0}#PendingFriend'.format(PEOPLE_BASE_URI), None))
            for triple in friend_triples:
                friend_id = triple.object.split('#')[-1]
                pending_friend_ids.append(friend_id)

        return pending_friend_ids


    def reject_friend_request(self, friend_id):
        """Rejects a friend request.

        Arguments:
        friend_id -- User id of the friend whose request this user is rejecting

        """
        result = get_service('RejectFriendsRequest').request(user_id=self.user_id, friend_id=friend_id)
        return result

    def add_to_planned_courses(self, course_code):
        """Add a course to this user's planned courses."""
        pass

    def remove_from_planned_courses(self, course_code):
        """Remove a course from this user's planned courses."""
        pass

    def get_events(self):
        """Returns the events of this user."""
        friends = people.get_friends(self.user_id)
        events = []
        for friend in friends:
            events.extend(Event.objects.get(user_id=friend))
            
        return events 

    def get_planned_courses(self):
        """Returns the planned courses of this user."""
        pass

    def get_completed_courses(self):
        """Returns the completed courses for this user """
        pass

    def is_planned_course(self, course_code):
        pass

    def is_completed_course(self, course_code):
        pass
if __name__ == '__main__':
    '''
    test
    '''
    session = Session(username='pang3', password='123456')
    session.open()
    #session.user_id = 'aJVepae1Or35tGaaWPEYjL' #''
    # print session.add_friend(friend_id='aJVepae1Or35tGaaWPEYjL')
    print session.remove_friend('aJVepae1Or35tGaaWPEYjL')
    session.close()
    
