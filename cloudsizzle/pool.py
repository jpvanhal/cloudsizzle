from threading import Condition
from kpwrapper import SIBConnection
from contextlib import contextmanager

class ConnectionPool(object):
    """A cache for SIB connections so that the connections can be reused."""

    def __init__(self):
        self._lock = Condition()
        self._unlocked = set()
        self._locked = set()
    
    def _create(self):
        conn = SIBConnection(method='preconfigured')
        conn.open()
        return conn
    
    def _expire(self, connection):
        connection.close()

    def _validate(self, connection):
        return True

    def acquire(self):
        """Acquire a connection object for use.
        
        If there are any connections available in the pool, removes one 
        from the pool and returns it. Otherwise creates a new connection 
        and returns it.

        Acquired connections must be released back to the pool with the 
        release() method.

        """
        with self._lock:
            if self._unlocked:
                while self._unlocked:
                    conn = self._unlocked.pop()
                    if self._validate(conn):
                        self._locked.add(conn)
                        return conn
                    else:
                        self._expire(conn)
            conn = self._create()
            self._locked.add(conn)
            return conn        
    
    def release(self, connection):
        """Release a connection in use back to the pool for reuse.
        
        Arguments:
        connection -- connection to be released

        """
        with self._lock:
            self._locked.remove(connection)
            self._unlocked.add(connection)

_pool = ConnectionPool()

@contextmanager
def get_connection():
    conn = _pool.acquire()
    yield conn
    _pool.release(conn)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
