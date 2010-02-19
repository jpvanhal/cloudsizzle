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
import threading
import time
from cloudsizzle.asi.service import AbstractService
from cloudsizzle.kp import Triple, bnode

LOG = logging.getLogger('cloudsizzle.asi.client')


class TimeOutError(Exception):
    """Raised if a service request is not responded after a certain time
    period.

    """
    pass


class AbstractClient(AbstractService):
    """Abstract base class for building the client side of a request-response
    type service.

    AbstractClient subscribes to service responses and provides a method for
    making service requests.

    """
    def __init__(self, sc, timeout=30):
        super(AbstractClient, self).__init__(sc)
        self.responses = {}
        self.condition = threading.Condition()
        self.timeout = timeout

    @property
    def query_triple(self):
        return Triple(None, 'rdf:type', self.response_type)

    @property
    def needs_response(self):
        """A boolean value indicating if this service request needs to wait
        for a response.

        """
        return True

    def process(self, id_, data):
        with self.condition:
            self.responses[data['response_to']] = data
            self.condition.notify_all()

    def request(self, **params):
        """Make a service request with the given data.

        Arguments:
        params -- A dict containing the request data.

        """
        request = params
        request['rdf:type'] = self.request_type

        LOG.debug('Making a {0} with parameters {1}.'.format(
            self.request_type, request))

        triples = []
        for key, value in request.iteritems():
            triples.append(Triple(bnode('id'), key, value))

        self.sc.insert(triples)

        request_id = self.sc.last_result[1]['id']
        if self.needs_response:
            return self._get_response(request_id)

    def _get_response(self, request_id):
        wait_start_time = time.time()
        with self.condition:
            while request_id not in self.responses:
                wait_time = time.time() - wait_start_time
                if wait_time > self.timeout:
                    raise TimeOutError
                self.condition.wait(self.timeout)

            response = self.responses.pop(request_id)

            return response


class LoginClient(AbstractClient):

    @property
    def name(self):
        return 'Login'


class LogoutClient(AbstractClient):

    @property
    def name(self):
        return 'Logout'

    @property
    def needs_response(self):
        return False


class RegisterClient(AbstractClient):

    @property
    def name(self):
        return 'Register'


class AddFriendsClient(AbstractClient):

    @property
    def name(self):
        return 'AddFriends'

    def request(self, user_id, friend_id):
        AbstractClient.request(self, user_id=user_id, friend_id=friend_id)


class RemoveFriendsClient(AbstractClient):

    @property
    def name(self):
        return 'RemoveFriends'

    def request(self, user_id, friend_id):
        AbstractClient.request(self, user_id=user_id, friend_id=friend_id)


class RejectFriendRequestClient(AbstractClient):

    @property
    def name(self):
        return 'RejectFriendRequest'

    def request(self, user_id, friend_id):
        AbstractClient.request(self, user_id=user_id, friend_id=friend_id)
