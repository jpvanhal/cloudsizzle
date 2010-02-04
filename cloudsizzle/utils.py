from cloudsizzle import pool
from cloudsizzle.kp import Triple, uri, literal

RDF_SCHEMA_URI = 'http://www.w3.org/2000/01/rdf-schema#'
RDF_SYNTAX_NS_URI = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'

def fetch_rdf_graph(subject):
    with pool.get_connection() as sc:
        triplets = sc.query(Triple(subject, None, None))

    graph = {}
    if not triplets:
        return graph

    for triplet in triplets:
        # Skip triplets that define RDF ontology
        if triplet.predicate.startswith(RDF_SYNTAX_NS_URI):
            continue

        s = str(triplet.subject)
        p = str(triplet.predicate)
        o = str(triplet.object)

        # Strip namespace uri from predicate
        if isinstance(triplet.predicate, uri):
            p = p.split('#')[-1]

        # The last condition is there to prevent wandering into RDF
        # ontology definitions
        if isinstance(triplet.object, uri) and not o.startswith(RDF_SCHEMA_URI):
            value = fetch_rdf_graph(o)
        else:
            value = o
        if s not in graph:
            graph[s] = {}
        if p not in graph[s]:
            graph[s][p] = value
        elif isinstance(graph[s][p], list):
            graph[s][p].append(value)
        else:
            graph[s][p] = [graph[s][p], value]

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
        s, p, o = str(triple.subject), str(triple.predicate), str(triple.object)
        if s not in graph:
            graph[s] = {}
        if p not in graph[s]:
            graph[s][p] = o
        elif isinstance(graph[s][p], list):
            graph[s][p].append(o)
        else:
            graph[s][p] = [graph[s][p], o]
    return graph
