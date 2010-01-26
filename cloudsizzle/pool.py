from threading import Condition
from kpwrapper import SIBConnection
from contextlib import contextmanager

"""
>>> pool = ConnectionPool()
>>> sc = pool.acquire()
>>> instanceof(sc, SIBConnection)
True
>>> sc2 = pool.acquire()
>>> id(sc) != id(sc2)
True
>>> pool.release(sc2)
>>> sc3 = pool.acquire()
>>> id(sc2) == id(sc3)
True

"""
class ConnectionPool(object):
    def __init__(self):
        self._lock = Condition()
        self._unlocked = set()
        self._locked = set()
    
    def _create(self):
        conn = WrappedSIBConnection(method='preconfigured')
        conn.open()
        return conn
    
    def _expire(self, connection):
        connection.close()

    def _validate(self, connection):
        return True

    def acquire(self):
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
