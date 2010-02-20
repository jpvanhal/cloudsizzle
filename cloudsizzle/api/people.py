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
This module contains CloudSizzle API functions related to people.

"""
from itertools import chain
from cloudsizzle.kp import Triple, uri
from cloudsizzle import pool
from cloudsizzle.utils import fetch_rdf_graph, listify
from cloudsizzle.api.asi_client import get_service

PEOPLE_BASE_URI = 'http://cos.alpha.sizl.org/people'


class UserDoesNotExist(Exception):
    """This exception is raised, when an API function tries do something with
    a user that does not exist.

    """
    pass


def create(username, password, email):
    """Create a new user.

    Returns the user id of the new user, if everything goes well.

    Arguments:
    username -- The desired username. Must be unique in the system. Length
                4-20 characters.
    password -- User's password.
    email -- User's email address.

    Exceptions:
    ValueError -- Given parameters were invalid.

    """
    register_service = get_service('Register')
    response = register_service.request(
        username=username, password=password, email=email)

    if 'messages' in response:
        messages = listify(response['messages'])
        raise ValueError(*messages)

    return response['user_id']


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
    user['user_id'] = user_id
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

def get_mutual_friends(user_id1, user_id2):
    """Get list of mutual friends between two users
    
    Arguments:
    user_id1, user_id2: ASI ids for the people whose mutual friends are wanted
    
    """
    friend_ids1 = get_friends(user_id1)
    friend_ids2 = get_friends(user_id2)
    
    # According to Python docs, I should not need to cast the lists to sets
    # still I do.
    return set.intersection(set(friend_ids1), set(friend_ids2))
    
def search(query):
    """Return users based on their real names and usernames.

    Arguments:
    query -- The search term. Every user whose name or user name contains the
             query string will be returned.

    """
    with pool.get_connection() as sc:
        query = query.lower()
        if isinstance(query, unicode):
            query = query.encode('utf8')

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

def get_completed_courses(user_id):
    """Returns the completed courses for the given user sorted by most recent
    completion first.

    """
    user_uri = '{0}/ID#{1}'.format(PEOPLE_BASE_URI, user_id)

    with pool.get_connection() as sc:
        all_completed_course_uris = set(triple.subject
            for triple in sc.query(
                Triple(None, 'rdf:type', 'CompletedCourse')))
        all_user_uris = set(triple.subject
            for triple in sc.query(Triple(None, 'user', uri(user_uri))))
        completed_course_uris = all_completed_course_uris & all_user_uris

        completed_courses = []
        for subject in completed_course_uris:
            completed_course = fetch_rdf_graph(
                subject, dont_follow=['user'])
            del completed_course['user']
            completed_courses.append(completed_course)

        return sorted(completed_courses, key=lambda item: item['date'],
            reverse=True)
