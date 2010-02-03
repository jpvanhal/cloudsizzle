from asi import ASIConnection
from cloudsizzle.asi import sib_agent
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
                values = result[key]
                if not isinstance(values, list):
                    values = [values]
                for value in values:
                    response_triples.append(Triple(bnode('id'), str(key), value))

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
class UserInfKnowledgeProcessor(kp):
    QUERY_TRIPLE = Triple(None, 'rdf:type', 'RegisterRequest')

    def execute(self,keywords):
            params = {
                'base_url': settings.ASI_BASE_URL,
                'app_name': settings.ASI_APP_NAME,
                'app_password': settings.ASI_APP_PASSWORD,

            }
            username = str(keywords[uri('username')])
            password = str(keywords[uri('password')])
            email    = str(keywords[uri('email')])
            with ASIConnection(**params) as ac:
                try:
                    user_info = ac.create_user(username = username,password=password,email=email)
                    if 'messages' not in user_info.keys():
                        user_id = user_info['id'] #succeed
                        user = ac.get_user(user_id)
                        sib = sib_agent.SIBAgent()
                        sib.receive(user)        # copy user info from asi to sib
                        return {'user_id':user_id}
                    else:
                        messages = user_info['messages']
                except KeyError:
                    user_id = None

            return {'messages':messages}

if __name__ == '__main__':
 #   kp = ASIKnowledgeProcessor()
 #  kp.start()
 #   kp.sc.insert([Triple(bnode('id'), uri('rdf:type'), literal('LoginRequest')), Triple(bnode('id'), uri('password'), literal('123456')), Triple(bnode('id'), uri('username'), literal('Pang1'))])
    kp = UserInfKnowledgeProcessor()
    kp.start()
 #   kp.execute({uri('username'):'pbpb2',uri('password'):123456,uri('email'):"pbpb@c1.com"})