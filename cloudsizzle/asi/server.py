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

import logging

from cloudsizzle.kp import SIBConnection, Triple, bnode, uri
from cloudsizzle import settings
from cloudsizzle.asi.importer import user_to_rdf
from cloudsizzle.asi.service import AbstractService, \
    ASIServiceKnowledgeProcessor
from cloudsizzle.asi.asi_friends_connection import \
    ASIFriendsConnection as ASIConnection

LOG = logging.getLogger('cloudsizzle.asi.server')
PEOPLE_BASE_URI = 'http://cos.alpha.sizl.org/people/'


class SessionStore(object):

    def __init__(self):
        self._sessions = {}

    def __del__(self):
        for ac in self._sessions.itervalues():
            ac.close()

    def __getitem__(self, key):
        return self._sessions[key]

    def login(self, username, password):
        msg = "Logging in to ASI with username '{0}' and password '{1}'."
        LOG.debug(msg.format(username, password))
        ac = ASIConnection(
            base_url=settings.ASI_BASE_URL,
            app_name=settings.ASI_APP_NAME,
            app_password=settings.ASI_APP_PASSWORD,
            username=username,
            password=password)
        response = ac.open()

        try:
            user_id = response['entry']['user_id']
            self._sessions[user_id] = ac
            LOG.debug("Logged in with user_id {0}!".format(user_id))
            return ac.session['entry']
        except KeyError:
            ac.close()
            LOG.warning("Logging in failed: {0}".format(response['messages']))
            return response

    def logout(self, user_id):
        LOG.debug('Logging out user with user_id {0}.'.format(user_id))
        try:
            ac = self._sessions[user_id]
            ac.close()
            del self._sessions[user_id]
        except KeyError:
            msg = 'Logging out failed: user {0} was not logged in.'
            LOG.warning(msg.format(user_id))


class AbstractServer(AbstractService):
    """Abstract base class for building the server side of a request-response
    type service.

    AbstractServer subscribes to service requests and provides a method for
    responding to these requests.

    """
    def __init__(self, sc):
        super(AbstractServer, self).__init__(sc)

    @property
    def query_triple(self):
        return Triple(None, 'rdf:type', self.request_type)

    def respond(self, request_id, response):
        """Respond to a service request.

        request_id -- The ID of the service request.
        response -- A dict containing the response data.

        """
        response['rdf:type'] = self.response_type
        response['response_to'] = uri(request_id)

        LOG.debug(
            'Responding to request {0} with {1}.'.format(request_id, response))

        response_triples = []
        for key, values in response.iteritems():
            if not isinstance(values, list):
                values = [values]
            for value in values:
                response_triples.append(Triple(bnode('id'), key, value))

        self.sc.insert(response_triples)


class LoginServer(AbstractServer):

    def __init__(self, sc, session_store):
        super(LoginServer, self).__init__(sc)
        self.session_store = session_store

    @property
    def name(self):
        return 'Login'

    def process(self, id_, data):
        response = self.session_store.login(data['username'],
            data['password'])
        self.respond(id_, response)


class LogoutServer(AbstractServer):

    def __init__(self, sc, session_store):
        super(LogoutServer, self).__init__(sc)
        self.session_store = session_store

    @property
    def name(self):
        return 'Logout'

    def process(self, id_, data):
        self.session_store.logout(data['user_id'])


class RegisterServer(AbstractServer):

    def __init__(self, sc):
        super(RegisterServer, self).__init__(sc)

    @property
    def name(self):
        return 'Register'

    def process(self, id_, data):
        with ASIConnection(
                base_url=settings.ASI_BASE_URL,
                app_name=settings.ASI_APP_NAME,
                app_password=settings.ASI_APP_PASSWORD) as ac:

            user_info = ac.create_user(
                username=data['username'],
                password=data['password'],
                email=data['email'])

        if 'messages' not in user_info:
            # Copy user info from ASI to SIB.
            triples = user_to_rdf(user_info)
            self.sc.insert(triples)

            user_id = user_info['id']
            response = {'user_id': user_id}
        else:
            messages = user_info['messages']
            response = {'messages': messages}

        self.respond(id_, response)


class RejectFriendRequestServer(AbstractServer):

    def __init__(self, sc, session_store):
        super(RejectFriendRequestServer, self).__init__(sc)
        self.session_store = session_store

    @property
    def name(self):
        return 'RejectFriendRequest'

    def process(self, id_, data):
        user_id = str(data['user_id'])
        friend_id = str(data['friend_id'])
        try:
            ac = self.session_store[user_id]
        except KeyError, e:
            print e
            response = {'messages': 'did not login ASi'}
        else:
            result = ac.reject_friend_request(friend_id)
            user_uri = '%sID#%s' % (PEOPLE_BASE_URI, user_id)
            friend_uri = '%sID#%s' % (PEOPLE_BASE_URI, friend_id)

            # Remove from my view
            remove_triple = Triple(
                user_uri,
                uri('http://cos.alpha.sizl.org/people#PendingFriend'),
                friend_uri)
            self.sc.remove(remove_triple)

            response = {'result': str(result)}

        self.respond(id_, response)


class RemoveFriendsServer(AbstractServer):

    def __init__(self, sc, session_store):
        super(RemoveFriendsServer, self).__init__(sc)
        self.session_store = session_store

    @property
    def name(self):
        return 'RemoveFriends'

    def process(self, id_, data):
        user_id = str(data['user_id'])
        friend_id = str(data['friend_id'])

        try:
            ac = self.session_store[user_id]
        except KeyError, e:
            print e
            response = {'messages': 'did not login ASi'}
        else:
            ac.remove_friend(friend_id)
            user_uri = '%sID#%s' % (PEOPLE_BASE_URI, user_id)
            friend_uri = '%sID#%s' % (PEOPLE_BASE_URI, friend_id)

            # Remove from my view
            remove_triple1 = Triple(
                user_uri,
                uri('http://cos.alpha.sizl.org/people#Friend'),
                friend_uri)

            # Remove from my friend's view
            remove_triple2 = Triple(
                friend_uri,
                uri('http://cos.alpha.sizl.org/people#Friend'),
                user_uri)
            result = self.sc.remove([remove_triple1, remove_triple2])

            response = {'result': str(result)}

        self.respond(id_, response)


class AddFriendsServer(AbstractServer):

    def __init__(self, sc, session_store):
        super(AddFriendsServer, self).__init__(sc)
        self.session_store = session_store

    @property
    def name(self):
        return 'AddFriends'

    def process(self, id_, data):
        user_id = str(data['user_id'])
        friend_id = str(data['friend_id'])
        try:
            ac = self.session_store[user_id]
        except KeyError, e:
            print e
            response = {'messages': 'did not login ASi'}
        else:
            pending_friends = ac.get_pending_friend_requests()
            my_pending_friend_list = []
            try:
                for pending_friend in pending_friends['entry']:
                    my_pending_friend_list.append(pending_friend['id'])
            except KeyError, e:
                print e
            result = ac.add_friend(friend_id)
            response = {'result': str(result)}

            if friend_id in my_pending_friend_list:
                user_uri = '%sID#%s' % (PEOPLE_BASE_URI, user_id)
                friend_uri = '%sID#%s' % (PEOPLE_BASE_URI, friend_id)

                # Remove from my view
                remove_triple = Triple(
                    user_uri,
                    uri('http://cos.alpha.sizl.org/people#PendingFriend'),
                    friend_uri)

                self.sc.remove(remove_triple)

                # Add to friend's view
                insert_triple1 = Triple(
                    friend_uri,
                    uri('http://cos.alpha.sizl.org/people#Friend'),
                    user_uri)

                # Add to my view
                insert_triple2 = Triple(
                    user_uri,
                    uri('http://cos.alpha.sizl.org/people#Friend'),
                    friend_uri)
                self.sc.insert([insert_triple1, insert_triple2])
            else:
                user_uri = '%sID#%s' % (PEOPLE_BASE_URI, user_id)
                friend_uri = '%sID#%s' % (PEOPLE_BASE_URI, friend_id)

                # Add to friend's view
                insert_triple = Triple(
                    friend_uri,
                    uri('http://cos.alpha.sizl.org/people#PendingFriend'),
                    user_uri)
                self.sc.insert(insert_triple)

        self.respond(id_, response)


def main():
    session_store = SessionStore()
    with SIBConnection('ASI service server', method='preconfigured') as sc:
        services = (
            LoginServer(sc, session_store),
            LogoutServer(sc, session_store),
            RegisterServer(sc),
            AddFriendsServer(sc, session_store),
            RemoveFriendsServer(sc, session_store),
            RejectFriendRequestServer(sc, session_store),
        )

        asi_server_kp = ASIServiceKnowledgeProcessor(services)
        asi_server_kp.start()

        try:
            raw_input('Press enter to stop.\n')
        finally:
            asi_server_kp.stop()

if __name__ == '__main__':
    main()
