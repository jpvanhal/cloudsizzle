"""Miscellaneous utility functions."""
from cloudsizzle import pool
from cloudsizzle.kp import Triple, uri, wrap_if_not_none

RDF_SCHEMA_URI = 'http://www.w3.org/2000/01/rdf-schema#'
RDF_SYNTAX_NS_URI = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'


def listify(object_):
    """Make the given object a list if it is not a list."""
    if isinstance(object_, list):
        return object_
    else:
        return [object_]


def fetch_rdf_graph(subject, dont_follow=None):
    """Fetch all triples related to a subject and transform them to a graph.

    First this function fetches all triples with the given subject. Then it
    calls itself recursively for all such triples that have an URI as their
    object. The end result is a clean graph of all these triples similar to
    the output of make_graph().

    Arguments:
    subject -- The subject of triples to fetch.
    dont_follow -- A list of predicates which are not followed recursively.
        This is useful if the RDF graph contains recursive references that
        cause infinite recursion in this function.

    """
    if dont_follow is None:
        dont_follow = []

    with pool.get_connection() as sc:
        triples = sc.query(Triple(subject, None, None))

    graph = {}
    if not triples:
        return graph

    for triple in triples:
        # Skip triples that define RDF ontology
        if triple.predicate.startswith(RDF_SYNTAX_NS_URI):
            continue

        subject = wrap_if_not_none(str, triple.subject)
        predicate = wrap_if_not_none(str, triple.predicate)
        object_ = wrap_if_not_none(str, triple.object)

        # Strip namespace uri from predicate
        if isinstance(triple.predicate, uri):
            predicate = predicate.split('#')[-1]

        # The last condition is there to prevent wandering into RDF
        # ontology definitions
        if isinstance(triple.object, uri) and \
                str(triple.predicate) not in dont_follow and \
                not object_.startswith(RDF_SCHEMA_URI):
            value = fetch_rdf_graph(object_, dont_follow)
        else:
            value = object_

        if subject not in graph:
            graph[subject] = {}
        if predicate not in graph[subject]:
            graph[subject][predicate] = value
        elif isinstance(graph[subject][predicate], list):
            graph[subject][predicate].append(value)
        else:
            graph[subject][predicate] = [graph[subject][predicate], value]

    return graph[subject]


def make_graph(triples):
    """Transforms a list of triples into a graph.

    >>> from cloudsizzle.kp import Triple, uri, literal
    >>> from pprint import pprint
    >>> triples = [Triple('T-76.4115', 'rdf:type', 'Course'),
    ...     Triple('T-76.4115', 'name', 'Software Development Project'),
    ...     Triple('T-76.4115', 'extent', '5-8')]
    >>> pprint(make_graph(triples))
    {'T-76.4115': {'extent': '5-8',
                   'name': 'Software Development Project',
                   'rdf:type': 'Course'}}

    When there are multiple triples with the same subject and predicate, the
    objects of the triples are put in a list:

    >>> triples = [
    ... Triple(
    ...     'http://cos.alpha.sizl.org/people/ID#dRq9He3yWr3QUKaaWPEYjL',
    ...     'rdf:type',
    ...     'http://cos.alpha.sizl.org/people#Person'),
    ... Triple(
    ...     'http://cos.alpha.sizl.org/people/ID#dRq9He3yWr3QUKaaWPEYjL',
    ...     'has_friend',
    ...     'http://cos.alpha.sizl.org/people/ID#azAC7-RdCr3OiIaaWPfx7J'),
    ... Triple(
    ...     'http://cos.alpha.sizl.org/people/ID#dRq9He3yWr3QUKaaWPEYjL',
    ...     'has_friend',
    ...     'http://cos.alpha.sizl.org/people/ID#azEe6yRdCr3OiIaaWPfx7J')]
    >>> pprint(make_graph(triples))
    {'http://cos.alpha.sizl.org/people/ID#dRq9He3yWr3QUKaaWPEYjL':
        {'has_friend':
            ['http://cos.alpha.sizl.org/people/ID#azAC7-RdCr3OiIaaWPfx7J',
             'http://cos.alpha.sizl.org/people/ID#azEe6yRdCr3OiIaaWPfx7J'],
         'rdf:type': 'http://cos.alpha.sizl.org/people#Person'}}

    """
    graph = {}
    for triple in triples:
        subject = wrap_if_not_none(str, triple.subject)
        predicate = wrap_if_not_none(str, triple.predicate)
        object_ = wrap_if_not_none(str, triple.object)

        if subject not in graph:
            graph[subject] = {}
        if predicate not in graph[subject]:
            graph[subject][predicate] = object_
        elif isinstance(graph[subject][predicate], list):
            graph[subject][predicate].append(object_)
        else:
            graph[subject][predicate] = [graph[subject][predicate], object_]
    return graph
