'''
usage:
    
    send any parameters to ASI by the dictionary format of 'do_request' function's parameters
    return a list, whose first item is the request_id and second item is lock
    acquire the lock, then get response by get_answer function. return a answerset dictionary.
    
    handler = ResponseHandler.getInstance()
    token = handler.do_request(username = 'Pang1',password = '123456')
    request_id = token[0]

    lock = token[1]
    lock.acquire()
    handler.get_answer(request_id)

@author: pb
'''
from cloudsizzle import pool
from cloudsizzle.singletonmixin import Singleton
from cloudsizzle.kp import SIBConnection, Triple, bnode, uri, literal
import collections,threading
from cloudsizzle.utils import make_graph

class ResponseHandler(threading.Thread,Singleton):
    QUERY_TRIPLE = Triple(None, 'rdf:type', 'Response')
    
    def __init__(self):
        print('backends')
        threading.Thread.__init__(self)
        self.locks = {}  
        self.answers = {}
        self.subscribe_tx = None
    def do_request(self,request_type = 'LoginRequest',**keywords):
        self.run()      # prevent developer forgeting run()
        triples = [Triple(bnode('id'), 'rdf:type', request_type),]
        keys = keywords.keys()
        keys.sort()
        for key in keys:
            triple = Triple(bnode('id'), key, keywords[key])
            triples.append(triple)
        lock  = threading.Lock() # before inserting happen
        lock.acquire()
        self.sc.insert(triples)
        request_id = self.sc.last_result[1]['id']  
        self.locks[str(request_id)]=lock
        
        
        
        return [request_id,self.locks[str(request_id)],]

    def callback(self, added, removed):
        for triple in added:
            response_triples = self.sc.query(Triple(triple.subject, None, None))
            g = make_graph(response_triples)
            
            self.sc.remove(response_triples) #garbage collected
            
            response_id = triple.subject
            request_id = str(g[response_id][uri('response_to')])
            if request_id in self.locks.keys():
                del g[response_id][uri('response_to')]
                self.answers[request_id] = g[response_id]
                self.locks[request_id].release()
    def get_answer(self,request_id):
        if request_id in self.answers.keys():
            answer = self.answers[request_id]
            del self.answers[request_id]
            del self.locks[request_id]     #garbage collected
            return answer
        return None
    def run(self):
        if not self.subscribe_tx:
            with pool.get_connection() as self.sc:
                self.subscribe_tx = self.sc.subscribe(self.QUERY_TRIPLE, self)
class LoginResponseHandler(ResponseHandler):
    def get_result(self,request_id):
        answer = self.get_answer(request_id)
        if answer:   
            return answer[uri('user_id')]
        return None
if __name__ == '__main__':
    # for test
    handler = LoginResponseHandler.getInstance()
    token = handler.do_request(username = 'Pang1',password = '123456')
    request_id = token[0]

    lock = token[1]
    lock.acquire()
    print (handler.get_result(request_id))
        