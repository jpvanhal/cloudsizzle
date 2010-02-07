from abc import ABCMeta, abstractproperty, abstractmethod
import logging

from cloudsizzle import pool
from asibsync.sib_agent import to_rdf_instance
from asilib import ASIConnection
from cloudsizzle.kp import SIBConnection, Triple, bnode, uri, literal
from cloudsizzle import settings
from cloudsizzle.asi import sib_agent
from cloudsizzle.asi.service import AbstractService, ASIServiceKnowledgeProcessor
from cloudsizzle.asi.asi_friends_connection import ASIFriendsConnection as new_ASIConnection
log = logging.getLogger('cloudsizzle.asi.server')

PEOPLE_BASE_URI = 'http://cos.alpha.sizl.org/people/'

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
        ac = new_ASIConnection(                                   #use extended asiConnection to replace the old one
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
        
class RegisterServer(AbstractServer):
    def __init__(self, sc):
        super(RegisterServer, self).__init__(sc)

    @property
    def name(self):
        return 'Register'

    def process(self, id_, data):
        params = {                                   #use extended asiConnection to replace the old one
                'base_url': settings.ASI_BASE_URL,
                'app_name': settings.ASI_APP_NAME,
                'app_password': settings.ASI_APP_PASSWORD,
        }
        username = str(data['username'])
        password = str(data['password'])
        email    = str(data['email'])
        with ASIConnection(**params) as ac:
            try:
                user_info = ac.create_user(username=username, password=password, email=email)
                if 'messages' not in user_info.keys():
                    user_id = user_info['id']  #succeed
                    user = ac.get_user(user_id)
                    new = to_rdf_instance(user)
                    with pool.get_connection() as self.sc:
                        self.sc.insert(new)        # copy user info from asi to sib
                    response = {'user_id':user_id}
                else:
                    messages = user_info['messages']
                    response = {'messages':messages}
            except KeyError:
                user_id = None
        self.respond(id_, response)

class RejectFriendsRequestServer(AbstractServer):
    def __init__(self, sc, session_store):
        super(RejectFriendsRequestServer, self).__init__(sc)
        self.session_store = session_store

    @property
    def name(self):
        return 'RejectFriendsRequest'

    def process(self, id_, data):
        user_id = str(data['user_id'])
        friend_id = str(data['friend_id'])
        try:
            ac = self.session_store._sessions[user_id]    
        except KeyError, e:
            print e
            response = {'messages': 'did not login ASi'} 
        else:
            result = ac.reject_friend_request(user_id, friend_id)
            user_uri = '%sID#%s' % (PEOPLE_BASE_URI, user_id)
            friend_uri = '%sID#%s' % (PEOPLE_BASE_URI, friend_id)                
            remove_triple = Triple(user_uri,                                        #remove from my view
                            uri('http://cos.alpha.sizl.org/people#PendingFriend'),
                               friend_uri)
            self.sc.remove(remove_triple)           
            response = {'result': str(result)}   


        self.respond(id_, response)

class RemoveFriendsRequestServer(AbstractServer):
    def __init__(self, sc, session_store):
        super(RemoveFriendsRequestServer, self).__init__(sc)
        self.session_store = session_store

    @property
    def name(self):
        return 'RemoveFriendsRequest'

    def process(self, id_, data):
        user_id = str(data['user_id'])
        friend_id = str(data['friend_id'])

        try:
            ac = self.session_store._sessions[user_id]    
        except KeyError, e:
            print e
            response = {'messages': 'did not login ASi'} 
        else:
            ac.remove_friend(friend_id)
            user_uri = '%sID#%s' % (PEOPLE_BASE_URI, user_id)
            friend_uri = '%sID#%s' % (PEOPLE_BASE_URI, friend_id)
            remove_triple = Triple(user_uri, 
                uri('http://cos.alpha.sizl.org/people#Friend'),
                                   friend_uri)
            result = self.sc.remove(remove_triple)
            response = {'result': str(result)}    

        self.respond(id_, response)

class AddFriendsRequestServer(AbstractServer):
    def __init__(self, sc, session_store):
        super(AddFriendsRequestServer, self).__init__(sc)
        self.session_store = session_store

    @property
    def name(self):
        return 'AddFriendsRequest'

    def process(self, id_, data):
        user_id = str(data['user_id'])
        friend_id = str(data['friend_id'])
        try:
            ac = self.session_store._sessions[user_id]    
        except KeyError, e:
            print e
            response = {'messages': 'did not login ASi'} 
        else:
            pending_friends = ac.get_pending_friend_requests()
            my_pending_friend_list = []
            try:
                for pending_friend in pending_friends['entry']:
                    my_pending_friend_list.append(pending_friend['id'])
            except KeyError, e:
                print e
            result = ac.add_friend(friend_id)
            response = {'result': str(result)}  
            
            if friend_id in my_pending_friend_list:
                user_uri = '%sID#%s' % (PEOPLE_BASE_URI, user_id)
                friend_uri = '%sID#%s' % (PEOPLE_BASE_URI, friend_id)                
                remove_triple = Triple(friend_uri,                                        #remove from friend's view
                                uri('http://cos.alpha.sizl.org/people#PendingFriend'),
                                   user_uri)
                self.sc.remove(remove_triple)
            else:
                user_uri = '%sID#%s' % (PEOPLE_BASE_URI, user_id)
                friend_uri = '%sID#%s' % (PEOPLE_BASE_URI, friend_id)                
                insert_triple = Triple(friend_uri,                                        #add from friend's view
                                uri('http://cos.alpha.sizl.org/people#PendingFriend'),
                                   user_uri)
                self.sc.insert(insert_triple)                
  


        self.respond(id_, response)
    
def main():
    session_store = SessionStore()
    with SIBConnection('ASI service server', method='preconfigured') as sc:
        services = (
            LoginServer(sc, session_store),
            LogoutServer(sc, session_store),
            RegisterServer(sc),
            AddFriendsRequestServer(sc, session_store),
            RemoveFriendsRequestServer(sc, session_store),
            RejectFriendsRequestServer(sc, session_store),
        )

        asi_server_kp = ASIServiceKnowledgeProcessor(services)
        asi_server_kp.start()

        try:
            raw_input('Press enter to stop.\n')
        finally:
            asi_server_kp.stop()

if __name__ == '__main__':
    main()
