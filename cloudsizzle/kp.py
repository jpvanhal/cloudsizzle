import kpwrapper
from kpwrapper import Triple as _Triple, SIBConnection, bnode, literal, uri, \
                      wrap_if_not_none

__all__ = ['Triple', SIBConnection, bnode, literal, uri]

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
    >>> escape('<a href="/foo?a=1&b=2">Hello \\'world\\'!</a>')
    '%3Ca href=%22/foo?a=1%26b=2%22%3EHello %27world%27!%3C/a%3E'

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
    >>> unescape('%3Ca href=%22/foo?a=1%26b=2%22%3EHello %27world%27!%3C/a%3E')
    '<a href="/foo?a=1&b=2">Hello \\'world\\'!</a>'

    Percent sign is also unescaped:
    >>> unescape('%25')
    '%'

    """
    for char, escaped in reversed(ESCAPE_CHARS):
        string = string.replace(escaped, char)
    return string


class Triple(_Triple):
    """
    Wraps the Triple class and adds escaping and unescaping of XML special
    characters to it.

    >>> triple = Triple('foo', 'bar', '<A & B>')
    >>> tuple = triple.to_tuple()
    >>> tuple
    (('foo', 'bar', '%3CA %26 B%3E'), 'uri', 'literal')
    >>> triple == Triple.from_tuple(tuple)
    True
    >>> triple = Triple(None, None, None)
    >>> triple.to_tuple()
    ((None, None, None), 'uri', 'literal')
    >>> Triple.from_tuple(_)
    Triple(None, None, None)

    """

    @staticmethod
    def from_tuple(tuple_):
        subject, predicate, object_ = tuple_[0]
        triple = (
            wrap_if_not_none(unescape, subject),
            wrap_if_not_none(unescape, predicate),
            wrap_if_not_none(unescape, object_)
        )
        tuple_ = (triple, ) + tuple_[1:]
        return _Triple.from_tuple(tuple_)

    def to_tuple(self, default_stype='uri', default_otype='literal'):
        tuple_ = _Triple.to_tuple(self, default_stype, default_otype)
        subject, predicate, object_ = tuple_[0]
        triple = (
            wrap_if_not_none(escape, subject),
            wrap_if_not_none(escape, predicate),
            wrap_if_not_none(escape, object_)
        )
        tuple_ = (triple, ) + tuple_[1:]
        return tuple_


class MockSIBConnection(object):
    """A fake SIBConnection class that implement the basic API of SIBConnection
    and does not connect to SIB at all.

    """
    NAMESPACES = {
        'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
        'owl': 'http://www.w3.org/2002/07/owl#',
        'xsd': 'http://www.w3.org/2001/XMLSchema#',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'sib': 'http://www.nokia.com/NRC/M3/sib#',
        'daml': 'http://www.daml.org/2000/12/daml+oil#',
    }

    def __init__(self, node_name='Node', method='Manual'):
        self.triple_store = set()

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        pass

    def open(self):
        pass

    def close(self):
        pass

    def insert(self, triples, **kwargs):
        for triple in triples:
            self.triple_store.add(triple)

    def __expand_namespace(self, node):
        if isinstance(node, uri) and ':' in node:
            namespace, value = node.split(':')
            try:
                return uri(self.NAMESPACES[namespace] + value)
            except KeyError:
                return node
        else:
            return node

    def __node_matches(self, pattern, node):
        if not pattern:
            return True
        return self.__expand_namespace(pattern) == node

    def __matches(self, pattern, triple):
        return self.__node_matches(pattern.subject, triple.subject) and \
            self.__node_matches(pattern.predicate, triple.predicate) and \
            self.__node_matches(pattern.object, triple.object)

    def query(self, query):
        result = []
        for triple in self.triple_store:
            if self.__matches(query, triple):
                result.append(triple)
        return result

    def update(self, r_triples, i_triples):
        self.remove(r_triples)
        self.insert(i_triples)

    def remove(self, triples):
        for triple in triples:
            self.triple_store.remove(triple)
        return True


kpwrapper.Triple = Triple
