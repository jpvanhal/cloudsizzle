from kpwrapper import Triple
import loginHandler
import threading
from asi import ASIConnection

debug = True
def debug_print(str):
    if debug:
        print('LoginHandler: %s' % str)


class LoginHandler(threading.Thread):

    def __init__(self, kp, username_pw):
        
	
        super(LoginHandler, self).__init__()
        self.kp = kp
        self.username = str(username_pw).split(' ')[0]
        self.pw = str(username_pw).split(' ')[1]
     
        debug_print('password '+self.pw)
    def run(self):
        conf = {}
        import os
        execfile(os.getenv('HOME', '.') + '/.asirc', conf)
        conf['asi_app_params'].update({
        'username': self.username,
        'password': self.pw,
        })
	
        with ASIConnection(**conf['asi_app_params']) as ac:
            try:
                if 'messages' in ac.session:
                    debug_print(self.username+" authenticate failed "+ac.session['messages'])
                    self.kp.insert(Triple(self.username, 'authenticate', 'failed')) 
                    return
                uid = ac.session['entry']['user_id']
                debug_print( 'uid :'+ uid)

                if uid != 'null' or uid != None:
                    debug_print( self.username + " logged in" )
                    self.kp.remove(Triple('users', 'login', self.username+" "+self.pw)) 
                    debug_print( self.username+ 'authenticate'+ 'succeed')
                    self.kp.remove(Triple(self.username, 'authenticate', 'succeed'))
                    self.kp.insert(Triple(self.username, 'authenticate', 'succeed')) 
				
            except Exception:
                debug_print(self.username+" authenticate failed")
                self.kp.insert(Triple(self.username, 'authenticate', 'failed')) 


