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

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cloudsizzle.studyplanner.settings'

from cloudsizzle.api.asi_client import get_service
from cloudsizzle.kp import Triple
from cloudsizzle import pool
from cloudsizzle.utils import listify
from cloudsizzle.api import people
from cloudsizzle.studyplanner.events.models import Event

PEOPLE_BASE_URI = 'http://cos.alpha.sizl.org/people'
CLOUDSIZZLE_RDF_BASE = 'http://cloudsizzle.cs.hut.fi/ontology/'

class LoginFailed(Exception):
    """Raised when logging in with ASI fails for any reason."""
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
            messages = listify(response['messages'])
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
        service = get_service('AddFriends')
        result = service.request(user_id=self.user_id, friend_id=friend_id)
        return result

    def remove_friend(self, friend_id):
        """Removes a friend connection.

        Arguments:
        friend_id -- The user id of the friend being broken up with.

        """
        service = get_service('RemoveFriends')
        result = service.request(user_id=self.user_id, friend_id=friend_id)
        try:
            return result['result']
        except TypeError:
            return None

    def get_pending_friend_requests(self):
        """Returns a list of people who have requested to connect to this user.

        A friend request is accepted by making the same request in the opposite
        direction.

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
        service = get_service('RejectFriendRequest')
        result = service.request(user_id=self.user_id, friend_id=friend_id)
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
            try:
                events.extend(Event.objects.get(user_id=friend))
            except Event.DoesNotExist:
                print 'No event'
        return events

    def get_planned_courses(self):
        """Returns the planned courses of this user."""
        pass

    def get_completed_courses(self):
        """Returns the completed courses for this user sorted by most recent
        completion first.

        """
        return people.get_completed_courses(self.user_id)

    def is_planned_course(self, course_code):
        pass

    def is_completed_course(self, course_code):
        subject = '{0}people/{1}/courses/completed/{2}'.format(
            CLOUDSIZZLE_RDF_BASE, self.user_id, course_code)
        triple = Triple(subject, 'rdf:type', 'CompletedCourse')
        with pool.get_connection() as sc:
            return len(sc.query(triple)) > 0
