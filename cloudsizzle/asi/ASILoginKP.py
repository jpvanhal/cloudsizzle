

from __future__ import with_statement # for Python 2.5

__author__ = 'bpang@cc.hut.fi (Pang Bo)'


import asi
import kpwrapper
import loginHandler
from kpwrapper import Triple


debug = True
def debug_print(str):
    if debug:
        print('ASILoginKP: %s' % str)


class ASILoginKP:

    QUERY_TRIPLE = Triple('users', 'login', None)

    def __init__(self):

        self.sc = kpwrapper.SIBConnection('subscribe1', method='preconfigured')
        self.sc1 = kpwrapper.SIBConnection('query1', method='preconfigured')
        self.subscribe_tx = None

    def __del__(self):
        self.stop()
        if hasattr(self, 'sc'):  # to handle cases where an exception is raised in constructor
            self.sc.close()
        if hasattr(self, 'sc1'):
            self.sc1.close()


    
    def start(self):   
        self.subscribe_tx = self.sc.subscribe(ASILoginKP.QUERY_TRIPLE, self)

        debug_print("ASILoginKP start working")

    def stop(self):
        if self.subscribe_tx:
            self.subscribe_tx.close()
            self.subscribe_tx = None
    
    def callback(self, added, removed):
        try:
            if added:
            # TODO What about multiple additions?   
                debug_print("add "+ added[0].subject+added[0].predicate+added[0].object)
                if added[0].predicate == 'login':
            
                   handler = loginHandler.LoginHandler(self.sc1,added[0].object)
                   debug_print('going to start')
                   handler.start()
                else:
                   debug_print('not match')
                   self.stop()
            if removed:
                print removed
                print 'remove'
            
            # TODO What about multiple additions?
            #print ('remove'+removed[0].object)
        except Exception: 
            print 'exception'


if __name__ == '__main__':
    ASILoginKP = ASILoginKP()
    ASILoginKP.start()        
 
