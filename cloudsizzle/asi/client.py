import logging
import threading
import time
from cloudsizzle.asi.service import AbstractService, ASIServiceKnowledgeProcessor
from cloudsizzle.kp import Triple, bnode

log = logging.getLogger('cloudsizzle.asi.client')

class TimeOutError(Exception):
    pass

class AbstractClient(AbstractService):
    def __init__(self, sc, timeout=10):
        super(AbstractClient, self).__init__(sc)
        self.responses = {}
        self.condition = threading.Condition()
        self.timeout = timeout

    @property
    def query_triple(self):
        return Triple(None, 'rdf:type', self.response_type)

    def process(self, id_, data):
        with self.condition:
            self.responses[data['response_to']] = data
            self.condition.notify_all()

    def request(self, **params):
        request = params
        request['rdf:type'] = self.request_type

        log.debug('Making a {0} with parameters {1}.'.format(
            self.request_type, request))

        triples = []
        for key, value in request.iteritems():
            triples.append(Triple(bnode('id'), key, value))

        self.sc.insert(triples)

        request_id = self.sc.last_result[1]['id']
        return self.get_response(request_id)

    def get_response(self, request_id):
        wait_start_time = time.time()
        with self.condition:
            while request_id not in self.responses:
                wait_time = time.time() - wait_start_time
                if wait_time > self.timeout:
                    raise TimeOutError
                self.condition.wait(self.timeout)

            response = self.responses[request_id]
            return response

class LoginClient(AbstractClient):
    @property
    def name(self):
        return 'Login'

class LogoutClient(AbstractClient):
    @property
    def name(self):
        return 'Logout'
