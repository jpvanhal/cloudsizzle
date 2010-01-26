from threading import Condition
from kpwrapper import SIBConnection
from contextlib import contextmanager

class ObjectPool(object):
    """A cache for objects so that they can be reused."""

    def __init__(self):
        self._lock = Condition()
        self._unlocked = set()
        self._locked = set()
    
    def _create(self):
        raise NotImplemented
    
    def _expire(self, obj):
        raise NotImplemented

    def _validate(self, obj):
        raise NotImplemented

    def acquire(self):
        """Acquire an object for use.
        
        If there are any objects available in the pool, removes one 
        from the pool and returns it. Otherwise creates a new object 
        and returns it.

        Acquired object must be released back to the pool with the 
        release() method.

        """
        with self._lock:
            if self._unlocked:
                while self._unlocked:
                    obj = self._unlocked.pop()
                    if self._validate(obj):
                        self._locked.add(obj)
                        return obj
                    else:
                        self._expire(obj)
            obj = self._create()
            self._locked.add(obj)
            return obj
    
    def release(self, obj):
        """Release a used object back to the pool for reuse.
        
        Arguments:
        obj -- object to be released

        """
        with self._lock:
            self._locked.remove(obj)
            self._unlocked.add(obj)

class ConnectionPool(ObjectPool):
    """A cache for SIB connections so that they can be reused."""

    def _create(self):
        conn = SIBConnection(method='preconfigured')
        conn.open()
        return conn
    
    def _expire(self, connection):
        connection.close()

    def _validate(self, connection):
        return True

_pool = ConnectionPool()

@contextmanager
def get_connection():
    conn = _pool.acquire()
    yield conn
    _pool.release(conn)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
