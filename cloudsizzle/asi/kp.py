from asi import ASIConnection
from cloudsizzle.kp import SIBConnection, Triple, bnode, uri, literal
from cloudsizzle import settings
from cloudsizzle.utils import make_graph

class kp():
    QUERY_TRIPLE = Triple(None, 'rdf:type', 'LoginRequest') # should be overrided

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
    def execute(self,**keywords):
        response = {}
        return response
    def callback(self, added, removed):
        for triple in added:
            print (triple)
            request_triples = self.sc.query(Triple(triple.subject, None, None))
            self.sc.remove(request_triples)

            g = make_graph(request_triples)
            request_id = triple.subject
            
            result = self.execute(g[request_id])
            
            response_triples = [
                Triple(bnode('id'), 'rdf:type', 'Response'),
                Triple(bnode('id'), 'response_to', triple.subject),]
            for key in result.keys():
                response_triples.append(Triple(bnode('id'), str(key), result[key]))

            self.sc.insert(response_triples)    
class ASIKnowledgeProcessor(kp):
    QUERY_TRIPLE = Triple(None, 'rdf:type', 'LoginRequest')

    def execute(self,keywords):
            params = {
                'base_url': settings.ASI_BASE_URL,
                'app_name': settings.ASI_APP_NAME,
                'app_password': settings.ASI_APP_PASSWORD,
                'username': str(keywords[uri('username')]),
                'password': str(keywords[uri('password')]),
            }

            with ASIConnection(**params) as ac:
                try:
                    user_id = ac.session['entry']['user_id']
                except KeyError:
                    user_id = None
            return {'user_id':user_id}


if __name__ == '__main__':
    kp = ASIKnowledgeProcessor()
    kp.start()
 #   kp.sc.insert([Triple(bnode('id'), uri('rdf:type'), literal('LoginRequest')), Triple(bnode('id'), uri('password'), literal('123456')), Triple(bnode('id'), uri('username'), literal('Pang1'))])
