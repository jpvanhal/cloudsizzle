from kpwrapper import Triple
import loginHandler
import threading
from asi import ASIConnection
class LoginHandler(threading.Thread):

    def __init__(self, kp, username_pw):
        
	
        super(LoginHandler, self).__init__()
        self.kp = kp
        self.username = str(username_pw).split(' ')[0]
        self.pw = str(username_pw).split(' ')[1]
     
        print('password '+self.pw)
    def run(self):
        conf = {
        'base_url': 'http://cos.alpha.sizl.org',
        'app_name': 'cloudsizzle02',
        'app_password': 'aIR23eaiaJBR',		
         }
        conf.update({
        'username': self.username,
        'password': self.pw,
        })
	
        with ASIConnection(**conf) as ac:
	
            uid = ac.session['entry']['user_id']
            print 'uid ', uid

        if uid != 'null' or uid != None:
            print self.username, " logged in"
            self.kp.remove(Triple('users', 'updated', 'pang1 123456'))#remove(Triple('users', 'updated', self.username+" "+self.pw)) 
            print self.username, 'authenticate', 'succeed'
            self.kp.insert(Triple(self.username, 'authenticate', 'succeed')) 
				
        else:
            print(self.username+" authenticate failed")
            self.kp.insert(Triple(self.username, 'authenticate', 'failed')) 


