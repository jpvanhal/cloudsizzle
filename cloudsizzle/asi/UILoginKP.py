

from __future__ import with_statement # for Python 2.5

__author__ = 'bpang@cc.hut.fi (Pang Bo)'


import kpwrapper
from kpwrapper import Triple


debug = True
def debug_print(str):
    if debug:
        print('sib_agent: %s' % str)


class UIKP:

    RESULT_TRIPLE = Triple(None, 'authenticate', None)
    def __init__(self, callback):

        self.sc = kpwrapper.SIBConnection('subscribe', method='preconfigured')
        self.sc1 = kpwrapper.SIBConnection('query', method='preconfigured')
        self.subscribe_result = None
        self.call_back = callback

    def __del__(self):
        self.stop()
        if hasattr(self, 'sc'):  # to handle cases where an exception is raised in constructor
            self.sc.close()
        if hasattr(self, 'sc1'):
            self.sc1.close()


    
    def Login(self,username_password):
        self.subscribe_result = self.sc.subscribe(UIKP.RESULT_TRIPLE, self)     
        if self.sc1.remove(Triple('users', 'login', 'pang1 123456')) :
            debug_print('already deleted'+username_password) 
        self.sc1.insert(Triple('users', 'login', username_password)) 
        debug_print('logging')

    def stop(self):
        if self.subscribe_result: 
            self.subscribe_result.close()
            self.subscribe_result = None
        exit()
    
    def callback(self, added, removed):
        try:
            if added:  
                debug_print("add "+ added[0].subject+added[0].predicate+added[0].object)
                if added[0].predicate == 'authenticate':                   
                    self.sc1.remove(Triple(added[0].subject, added[0].predicate, added[0].object)) 
                    self.call_back(added[0].object)
                    self.stop()
                else:
                   debug_print('not match')
                   self.stop()
            if removed:
                debug_print('remove '+removed[0].subject+removed[0].predicate+removed[0].object)
            
            # TODO What about multiple additions?
            #print ('remove'+removed[0].object)
        except Exception: 
            print 'exception'
            self.stop()


if __name__ == '__main__':
    def callback(result):
        print result
    UIKP(callback).Login('pang1 12345622')     
 
