import logging
from abc import ABCMeta, abstractproperty, abstractmethod
from cloudsizzle.kp import Triple
from cloudsizzle.utils import make_graph

log = logging.getLogger('cloudsizzle.asi.service')

class AbstractService(object):
    __metaclass__ = ABCMeta

    def __init__(self, sc):
        self.responses = {}
        self.sc = sc
        self.subscription = None

    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def query_triple(self):
        pass

    @property
    def request_type(self):
        return '{0}Request'.format(self.name)

    @property
    def response_type(self):
        return '{0}Response'.format(self.name)

    @abstractmethod
    def process(self, id_, data):
        pass

    def callback(self, added, removed):
        for triple in added:
            id_ = str(triple.subject)
            triples = self.sc.query(Triple(id_, None, None))
            self.sc.remove(triples)
            data = make_graph(triples)
            if 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' in data[id_].keys():
                del data[id_]['http://www.w3.org/1999/02/22-rdf-syntax-ns#type']
            log.debug('Received data with id {0} containing {1}.'.format(
                id_, data))

            self.process(id_, data[id_])

    def subscribe(self):
        log.debug('Subscribing to {0}.'.format(self.query_triple))
        self.subscription = self.sc.subscribe(self.query_triple, self)
        if not self.subscription:
            log.error('Subscribing to {0} failed.'.format(self.query_triple))
        else:
            log.info('Subscribed to {0}.'.format(self.query_triple))

    def unsubscribe(self):
        if self.subscription:
            self.subscription.close()
            self.subscription = None
            log.debug('Unsubscribed from {0}.'.format(self.query_triple))

class ASIServiceKnowledgeProcessor(object):
    def __init__(self, services):
        self._services = {}
        for service in services:
            self._services[service.name] = service
        self._is_running = False

    def __getitem__(self, key):
        self.start()
        return self._services[key]

    def start(self):
        if not self._is_running:
            for service in self._services.itervalues():
                service.subscribe()
            self._is_running = True

    def stop(self):
        if self._is_running:
            for service in self._services.itervalues():
                service.unsubscribe()
            self._is_running = False
