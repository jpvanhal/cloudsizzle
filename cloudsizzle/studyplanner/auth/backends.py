import threading
from django.contrib.auth.models import User
from cloudsizzle.kp import SIBConnection, Triple, bnode, uri, literal
from cloudsizzle.utils import make_graph

from cloudsizzle.api.ResponseHandler import LoginResponseHandler

class LoginResponseHandler1(threading.Thread):
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
        

        handler = LoginResponseHandler.getInstance()
        token = handler.do_request(username = username, password = password)
        request_id = token[0]
        lock = token[1]
        lock.acquire()
        user_id = str(handler.get_result(request_id))
        login_valid = user_id != "None"
        if login_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username)
                user.save()
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
