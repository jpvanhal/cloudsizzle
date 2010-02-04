import kpwrapper
from kpwrapper import Triple, SIBConnection, bnode, literal, uri

__all__ = [Triple, SIBConnection, bnode, literal, uri]

ESCAPE_CHARS = (
    ('%', '%25'), # must be escaped first, and unescaped last
    ('<', '%3C'),
    ('>', '%3E'),
    ('&', '%26'),
    ('"', '%22'),
    ("'", '%27'),
)

def escape(string):
    """Escape XML special characters with hexadecimal codes.

    For example:
    >>> escape('<a href="/somepage?a=1&b=2">Hello \\'world\\'!</a>')
    '%3Ca href=%22/somepage?a=1%26b=2%22%3EHello %27world%27!%3C/a%3E'

    Percent sign is also escaped:
    >>> escape('%')
    '%25'

    """
    for char, escaped in ESCAPE_CHARS:
        string = string.replace(char, escaped)
    return string

def unescape(string):
    """Unescape XML special characters escaped with hexadecimal codes.

    For example:
    >>> unescape('%3Ca href=%22/somepage?a=1%26b=2%22%3EHello %27world%27!%3C/a%3E')
    '<a href="/somepage?a=1&b=2">Hello \\'world\\'!</a>'

    Percent sign is also unescaped:
    >>> unescape('%25')
    '%'

    """
    for char, escaped in reversed(ESCAPE_CHARS):
        string = string.replace(escaped, char)
    return string

class WrappedTriple(Triple):
    """
    >>> triple = WrappedTriple('foo', 'bar', '<A & B>')
    >>> tuple = triple.to_tuple()
    >>> tuple
    (('foo', 'bar', '%3CA %26 B%3E'), 'uri', 'literal')
    >>> triple == WrappedTriple.from_tuple(tuple)
    True

    """
    @staticmethod
    def from_tuple(tuple_):
        subject, predicate, object_ = tuple_[0]
        triple = unescape(subject), unescape(predicate), unescape(object_)
        tuple_ = (triple, ) + tuple_[1:]
        return Triple.from_tuple(tuple_)

    def to_tuple(self, default_stype='uri', default_otype='literal'):
        tuple_ = Triple.to_tuple(self, default_stype, default_otype)
        subject, predicate, object_ = tuple_[0]
        triple = escape(subject), escape(predicate), escape(object_)
        tuple_ = (triple, ) + tuple_[1:]
        return tuple_

kpwrapper.Triple = WrappedTriple
