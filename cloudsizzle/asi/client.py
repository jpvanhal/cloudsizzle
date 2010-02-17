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
