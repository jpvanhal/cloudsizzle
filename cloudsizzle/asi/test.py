

from __future__ import with_statement # for Python 2.5

__author__ = 'eemeli.kantola@iki.fi (Eemeli Kantola)'

import asi
import time
import kpwrapper
import loginHandler
from kpwrapper import Triple
from asi.util import XSDateTime

debug = True
def debug_print(str):
    if debug:
        print('sib_agent: %s' % str)


class SIBAgent:
    '''Usage:
    
    sa = SIBAgent()
    sa.set_asi_agent(aa)
    sa.start()
    '''

    QUERY_TRIPLE = Triple('users', 'updated', None)
    RESULT_TRIPLE = Triple(None, 'authenticate', None)
    def __init__(self, asi_updated=None):

        self.sc = kpwrapper.SIBConnection('SIB to ASI', method='preconfigured')
        self.sc2 = kpwrapper.SIBConnection('SIB to ASI ', method='preconfigured')
        self.sc1 = kpwrapper.SIBConnection('ui to SIB ', method='preconfigured')
        self.sc4 = kpwrapper.SIBConnection('ASI to SIB', method='preconfigured')
        self.subscribe_tx = None
        self.subscribe_result = None

    def __del__(self):
        self.stop()
        if hasattr(self, 'sc'):  # to handle cases where an exception is raised in constructor
            self.sc.close()
        if hasattr(self, 'sc2'):     
            self.sc2.close()
        if hasattr(self, 'sc1'):
            self.sc1.close()
        if hasattr(self, 'sc4'):
            self.sc4.close()

    
    def start(self):
        self.subscribe_result = self.sc2.subscribe(SIBAgent.RESULT_TRIPLE, self)      
        self.subscribe_tx = self.sc.subscribe(SIBAgent.QUERY_TRIPLE, self)
        if self.sc1.remove(Triple('users', 'updated', 'pang1 123456')) :
            debug_print('already deleted')
        self.sc1.insert(Triple('users', 'updated', 'pang1 123456')) 

    def stop(self):
        if self.subscribe_tx:
            self.subscribe_tx.close()
            self.subscribe_tx = None
        if self.subscribe_result: 
            self.subscribe_result.close()
            self.subscribe_result = None
    
    def callback(self, added, removed):
        try:
            if added:
            # TODO What about multiple additions?   
                print added
                if added[0].predicate == 'updated':
            
                   handler = loginHandler.LoginHandler(self.sc4,added[0].object)
                   debug_print('going to start')
                   handler.start()
                elif added[0].predicate == 'authenticate':
                   print(added[0].subject+added[0].predicate+added[0].object)
                   self.sc1.remove(added[0]) 
                   self.stop()
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
    sa = SIBAgent()
    sa.start()        
 
