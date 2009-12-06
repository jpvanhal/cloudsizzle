import threading
from kpwrapper import SIBConnection, Triple, bnode, uri, literal
from cloudsizzle.utils import make_graph

class LoginResponseHandler(threading.Thread):
    QUERY_TRIPLE = Triple(None, 'rdf:type', 'LoginResponse')

    def __init__(self, sc, request_id):
        threading.Thread.__init__(self)
        self.sc = sc
        self.request_id = literal(request_id)
        self.subscribe_tx = None
        self.lock = threading.Lock()
        self.lock.acquire()

    def callback(self, added, removed):
        for triple in added:
            response_triples = self.sc.query(Triple(triple.subject, None, None))
            g = make_graph(response_triples)
            response_id = triple.subject
            if g[response_id][uri('response_to')] == self.request_id:
                self.user_id = g[response_id][uri('user_id')]
                self.subscribe_tx.close()
                self.lock.release()
                break

    def run(self):
        self.subscribe_tx = self.sc.subscribe(self.QUERY_TRIPLE, self)

class SIBBackend:
    def authenticate(self, username, password):
        with SIBConnection(method='preconfigured') as sc:
            sc.insert([
                Triple(bnode('id'), 'rdf:type', 'LoginRequest'),
                Triple(bnode('id'), 'username', username),
                Triple(bnode('id'), 'password', password)
            ])
            request_id = sc.last_result[1]['id']
            handler = LoginResponseHandler(sc, request_id)
            handler.run()
            handler.lock.acquire()
            print "User ID:", handler.user_id

if __name__ == '__main__':
    backend = SIBBackend()
    for username, password in (('pang1', '12346'), ('foobar', '12346')):
        print username, password
        backend.authenticate(username, password)
