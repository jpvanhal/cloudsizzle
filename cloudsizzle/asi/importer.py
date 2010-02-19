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
This module contains a knowledge processor for importing people and their
friends from ASI to SIB.

"""
from asilib import ASIConnection
# This probably not a public interface, but we need to use it
# because we want to copy all users not synchronize a single user
from asibsync.sib_agent import to_rdf_instance
from cloudsizzle.kp import SIBConnection, Triple, uri
from cloudsizzle import settings


# These are used to construct the URIs in RDF
RDF_BASE_URI = 'http://cos.alpha.sizl.org/people'
RDF_BASE_TYPE = 'Person'


def user_to_rdf(user):
    """Convert a user dict to a list of RDF triples.

    Arguments:
    user -- A dictionary representing user as returned by asilib or
            cloudsizzle.api.people.get()

    """
    return to_rdf_instance(user, RDF_BASE_URI, RDF_BASE_TYPE, 'id')


def friends_to_rdf(user, friends):
    """Convert user's friends to a list of RDF triples.

    Arguments:
    user -- A dictionary representing user.
    friends -- List of dictionaries representing user's friends.

    Both user and friend dictionaries should be similar to those returned by
    asilib or cloudsizzle.api.people.get()

    """
    triples = []
    for friend in friends:
        triples.append(Triple(
            '{0}/ID#{1}'.format(RDF_BASE_URI, user['id']),
            '{0}#Friend'.format(RDF_BASE_URI),
            uri('{0}/ID#{1}'.format(RDF_BASE_URI, friend['id']))
        ))
    return triples


def import_asi():
    """Import people and their friends from ASI to SIB.

    Note that this method does not update people that are already in SIB
    correctly (old people triples are not removed).

    """
    with SIBConnection('ASI to SIB dump', method='preconfigured') as sc:

        with ASIConnection(base_url=settings.ASI_BASE_URL,
            app_name=settings.ASI_APP_NAME,
            app_password=settings.ASI_APP_PASSWORD) as ac:

            print "Fetching users from ASI"
            users = ac.find_users()
            # This will choke on users that do not have an id
            # All users should probably have one, but we need to work
            # nevertheless.
            # Either need to convert the triplets one by one or patch
            # asibsync
            print "Converting ASI output to Triplets"
            for index, user in enumerate(users):
                print index, len(users), "\r"
                try:
                    triples = user_to_rdf(user)
                    friends = ac.get_friends(user['id'])
                    triples.extend(friends_to_rdf(user, friends))
                except KeyError:
                    print "Faulty userdata for ASI:"
                    print user
                else:
                    print "Inserting the following triples:"
                    print triples
                    sc.insert(triples)


if __name__ == '__main__':
    import_asi()
