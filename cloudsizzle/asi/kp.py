from asi import ASIConnection
from kpwrapper import SIBConnection, Triple, bnode, uri, literal
from cloudsizzle import settings
from cloudsizzle.utils import make_graph

class ASIKnowledgeProcessor(object):
    QUERY_TRIPLE = Triple(None, 'rdf:type', 'LoginRequest')

    def __init__(self):
        self.sc = None
        self.subscribe_tx = None

    def start(self):
        self.sc = SIBConnection('asi', method='preconfigured')
        self.sc.open()
        self.subscribe_tx = self.sc.subscribe(self.QUERY_TRIPLE, self)

    def stop(self):
        if self.subscribe_tx:
            self.subscribe_tx.close()
            self.subscribe_tx = None
        if self.sc:
            self.sc.close()
            self.sc = None

    def callback(self, added, removed):
        for triple in added:
            request_triples = self.sc.query(Triple(triple.subject, None, None))
            self.sc.remove(request_triples)

            g = make_graph(request_triples)
            request_id = triple.subject

            params = {
                'base_url': settings.ASI_BASE_URL,
                'app_name': settings.ASI_APP_NAME,
                'app_password': settings.ASI_APP_PASSWORD,
                'username': str(g[request_id][uri('username')]),
                'password': str(g[request_id][uri('password')]),
            }

            with ASIConnection(**params) as ac:
                print ac.session
                user_id = ac.session.get('user_id', None)

            response_triples = [
                Triple(bnode('id'), 'rdf:type', 'LoginResponse'),
                Triple(bnode('id'), 'response_to', triple.subject),
                Triple(bnode('id'), 'user_id', user_id)]

            self.sc.insert(response_triples)

if __name__ == '__main__':
    kp = ASIKnowledgeProcessor()
    kp.start()
