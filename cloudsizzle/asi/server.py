import logging

from asilib import ASIConnection
from cloudsizzle.kp import SIBConnection, Triple, bnode, uri, literal
from cloudsizzle import settings
from cloudsizzle.utils import make_graph

log = logging.getLogger('cloudsizzle.asi.kp')

class SessionStore(object):
    def __init__(self):
        self._sessions = {}

    def __del__(self):
        for user_id, ac in self._sessions.iteritems():
            try:
                ac.close()
            except Exception:
                pass

    def login(self, username, password):
        log.debug("Logging in to ASI with username '{0}' and password '{1}'.".format(username, password))
        ac = ASIConnection(
            base_url=settings.ASI_BASE_URL,
            app_name=settings.ASI_APP_NAME,
            app_password=settings.ASI_APP_PASSWORD,
            username=username,
            password=password)
        ac.open()

        try:
            user_id = ac.session['entry']['user_id']
            self._sessions[user_id] = ac
            log.debug("Logged in with user_id {0}!".format(user_id))
            return user_id
        except KeyError:
            ac.close()
            log.debug("Logging in failed: {0}".format(ac.session['messages']))
            raise Exception(' '.join(ac.session['messages']))
            #except:
            #    raise Exception('User login failed for an unknown reason.')

    def logout(self, user_id):
        try:
            ac = self._sessions[user_id]
            ac.close()
            del self._sessions[user_id]
        except KeyError:
            raise Exception('User with the given user_id is not logged in.')

class AbstractService(object):
    def __init__(self, sc):
        self.sc = sc
        self.subscription = None

    def get_request_type(self):
        raise NotImplementedError

    def get_response_type(self):
        raise NotImplementedError

    def process_request(self, request_id, request):
        raise NotImplementedError

    def subscribe(self):
        query_triple = Triple(None, 'rdf:type', self.get_request_type())
        log.debug('Subscribing to {0}.'.format(query_triple))
        self.subscription = self.sc.subscribe(query_triple, self)
        if not self.subscription:
            log.warning('Subscribing to {0} failed!'.format(query_triple))
        else:
            log.info('Subscribed to {0}.'.format(query_triple))

    def unsubscribe(self):
        if self.subscription:
            self.subscription.close()
            self.subscription = None
            log.debug('Unsubscribed from {0}.'.format(self.get_request_type()))

    def callback(self, added, removed):
        for triple in added:
            request_id = str(triple.subject)
            request_triples = self.sc.query(Triple(request_id, None, None))
            self.sc.remove(request_triples)
            request_dict = make_graph(request_triples)

            log.debug('Received a request {0} containing {1}.'.format(
                request_id, request_dict))

            self.process_request(request_id, request_dict[request_id])

    def respond(self, request_id, response):
        response['rdf:type'] = self.get_response_type()
        response['response_to'] = uri(request_id)

        log.debug(
            'Responding to request {0} with {1}.'.format(request_id, response))

        response_triples = []
        for key, value in response.iteritems():
            response_triples.append(Triple(bnode('id'), key, value))

        self.sc.insert(response_triples)

class LoginService(AbstractService):
    def __init__(self, sc, session_store):
        AbstractService.__init__(self, sc)
        self.session_store = session_store

    def get_request_type(self):
        return 'LoginRequest'

    def get_response_type(self):
        return 'LoginResponse'

    def process_request(self, request_id, request):
        try:
            user_id = self.session_store.login(request['username'],
                request['password'])
            self.respond(request_id, {'user_id': user_id})
        except Exception, e:
            self.respond(request_id, {'messages': str(e.args)})

class LogoutService(AbstractService):
    def __init__(self, sc, session_store):
        AbstractService.__init__(self, sc)
        self.session_store = session_store

    def get_request_type(self):
        return 'LogoutRequest'

    def process_request(self, request_id, request):
        try:
            self.session_store.logout(request['user_id'])
        except Exception, e:
            pass

def main():
    session_store = SessionStore()
    with SIBConnection('ASI Services', method='preconfigured') as sc:
        services = (
            LoginService(sc, session_store),
            LogoutService(sc, session_store),
        )

        for service in services:
            service.subscribe()

        try:
            raw_input('Press enter to stop.\n')
        finally:
            for service in services:
                service.unsubscribe()

if __name__ == '__main__':
    main()
