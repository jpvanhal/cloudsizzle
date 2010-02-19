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
from abc import ABCMeta, abstractproperty, abstractmethod
from cloudsizzle.kp import Triple
from cloudsizzle.utils import make_graph

LOG = logging.getLogger('cloudsizzle.asi.service')

class AbstractService(object):
    """Abstract base class for building request-response type services through
    SIB.

    """
    __metaclass__ = ABCMeta

    def __init__(self, sc):
        self.responses = {}
        self.sc = sc
        self.subscription = None

    @abstractproperty
    def name(self):
        """Name of the service.

        This is used for construction the RDF types for the service requests
        and response. See request_type and response_type properties.

        """
        pass

    @abstractproperty
    def query_triple(self):
        """The triple that this service subscribes to in SIB."""
        pass

    @property
    def request_type(self):
        """The RDF type for service requests."""
        return '{0}Request'.format(self.name)

    @property
    def response_type(self):
        """The RDF type for service responses."""
        return '{0}Response'.format(self.name)

    @abstractmethod
    def process(self, id_, data):
        """This method is called when service request or response is made.

        Arguments:
        id_ -- The ID of the response or request that was made.
        data -- A dict containing the data of the response or request that was
                made.

        """
        pass

    def callback(self, added, removed):
        """The callback function that is called when triples matching
        query_triple are added or removed to SIB.

        Processes added triples in to clean dict format and hands them over
        to process() method for processing. Also does some garbage collection
        by removing the added triples from SIB.

        """
        for triple in added:
            id_ = str(triple.subject)
            triples = self.sc.query(Triple(id_, None, None))
            self.sc.remove(triples)
            data = make_graph(triples)
            if 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' in data[id_]:
                del data[id_]['http://www.w3.org/1999/02/22-rdf-syntax-ns#type']
            LOG.debug('Received data with id {0} containing {1}.'.format(
                id_, data))

            self.process(id_, data[id_])

    def subscribe(self):
        """Subscribes this service to the query_triple."""
        LOG.debug('Subscribing to {0}.'.format(self.query_triple))
        self.subscription = self.sc.subscribe(self.query_triple, self)
        if not self.subscription:
            LOG.error('Subscribing to {0} failed.'.format(self.query_triple))
        else:
            LOG.info('Subscribed to {0}.'.format(self.query_triple))

    def unsubscribe(self):
        """Unsubscribes this service from the query_triple."""
        if self.subscription:
            self.subscription.close()
            self.subscription = None
            LOG.debug('Unsubscribed from {0}.'.format(self.query_triple))


class ASIServiceKnowledgeProcessor(object):

    def __init__(self, services):
        """Creates a new knowledge processor with the given services."""
        self._services = {}
        for service in services:
            self._services[service.name] = service
        self._is_running = False

    def __getitem__(self, key):
        """Return a service with the given name."""
        self.start()
        return self._services[key]

    def start(self):
        """Start the knowledge processor if not already running."""
        if not self._is_running:
            for service in self._services.itervalues():
                service.subscribe()
            self._is_running = True

    def stop(self):
        """Stop the knowledge processor if it is running."""
        if self._is_running:
            for service in self._services.itervalues():
                service.unsubscribe()
            self._is_running = False
