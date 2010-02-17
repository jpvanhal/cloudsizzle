from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
from threading import Condition
from cloudsizzle.kp import SIBConnection


class ObjectPool(object):
    """A cache for objects so that they can be reused."""

    __meta__ = ABCMeta

    def __init__(self):
        self._lock = Condition()
        self._unlocked = set()
        self._locked = set()

    @abstractmethod
    def _create(self):
        """Return a new instance of object."""
        pass

    @abstractmethod
    def _expire(self, obj):
        """Destroy an old instance of object."""
        pass

    @abstractmethod
    def _validate(self, obj):
        """Validate if the given object is still usable."""
        pass

    def acquire(self):
        """Acquire an object for use.

        If there are any objects available in the pool, removes one
        from the pool and returns it. Otherwise creates a new object
        and returns it.

        Acquired object must be released back to the pool with the
        release() method.

        """
        with self._lock:
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

    def _expire(self, conn):
        conn.close()

    def _validate(self, conn):
        return True


POOL = ConnectionPool()


@contextmanager
def get_connection():
    """Use this context manager to get an open SIB connection instance.

    An connection instance is automatically acquired from the connection pool
    and then automatically released when you are done with it.

    Example:
    >>> from cloudsizzle import pool
    >>> with pool.get_connection() as sc:
    >>>     # do something with the connection sc

    """
    conn = POOL.acquire()
    yield conn
    POOL.release(conn)
