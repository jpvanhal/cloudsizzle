'''
Created on Feb 6, 2010

@author: pb
'''

__author__ = 'bpang@cc.hut.fi'

from asilib import ASIConnection, build_param_string
from cloudsizzle import settings

class ASI_Friends_connection(ASIConnection):
    def __init__(self, base_url, **session_params):
        
        ASIConnection.__init__(self, base_url = base_url, **session_params)
    
    def add_friend(self, uid, friend_id ):
        return self.do_request(ASIConnection.people_url + '/' + uid + '/@friends',
                               post_params = build_param_string(friend_id=friend_id),
                               method='POST')
    def remove_friend(self, uid, friend_id ):
        return self.do_request(ASIConnection.people_url + '/' + uid + '/@friends' +
                               '/' + friend_id ,
                               method='DELETE')
    def get_pending_friend_requests(self, uid):
        return self.do_request(ASIConnection.people_url + '/' + uid + '/@pending_friend_requests',
                               method='GET')
    def reject_friend_request(self,  uid, friend_id):
        return self.do_request(ASIConnection.people_url + '/' + uid + '/@pending_friend_requests' +
                               '/' + friend_id ,
                               method='DELETE')

def main():
    ''' for test '''
    username = 'Pang3' 
    password = '123456'
    try:
        
        ac = ASI_Friends_connection(
            base_url=settings.ASI_BASE_URL,
            app_name=settings.ASI_APP_NAME,
            app_password=settings.ASI_APP_PASSWORD,
            username=None,
            password=None)
        ac.open()
        uid = ac.session['entry']['user_id']
        friend_id = 'aJVepae1Or35tGaaWPEYjL'
        per_page = 5
        page = 1
        print ac.get_friends(uid)
        print ac.remove_friend(uid, friend_id)
        print ac.get_friends(uid)
        
        pass   
    except KeyError, e:
        print e
    finally:
        ac.close()
if __name__ == '__main__':
    main()