from abc import ABCMeta, abstractproperty, abstractmethod
import logging

from asilib import ASIConnection
from cloudsizzle.kp import SIBConnection, Triple, bnode, uri, literal
from cloudsizzle import settings
from cloudsizzle.asi.service import AbstractService, ASIServiceKnowledgeProcessor

log = logging.getLogger('cloudsizzle.asi.server')

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
        response = ac.open()

        try:
            user_id = response['entry']['user_id']
            self._sessions[user_id] = ac
            log.debug("Logged in with user_id {0}!".format(user_id))
            return ac.session['entry']
        except KeyError:
            ac.close()
            log.debug("Logging in failed: {0}".format(response['messages']))
            return response

    def logout(self, user_id):
        log.debug('Logging out user with user_id {0}.'.format(user_id))
        try:
            ac = self._sessions[user_id]
            ac.close()
            del self._sessions[user_id]
        except KeyError:
            log.warning('Logging out failed: user {0} was not logged in.'.format(user_id))

class AbstractServer(AbstractService):
    def __init__(self, sc):
        super(AbstractServer, self).__init__(sc)

    @property
    def query_triple(self):
        return Triple(None, 'rdf:type', self.request_type)

    def respond(self, request_id, response):
        response['rdf:type'] = self.response_type
        response['response_to'] = uri(request_id)

        log.debug(
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

def main():
    session_store = SessionStore()
    with SIBConnection('ASI service server', method='preconfigured') as sc:
        services = (
            LoginServer(sc, session_store),
            LogoutServer(sc, session_store),
        )

        asi_server_kp = ASIServiceKnowledgeProcessor(services)
        asi_server_kp.start()

        try:
            raw_input('Press enter to stop.\n')
        finally:
            asi_server_kp.stop()

if __name__ == '__main__':
    main()
