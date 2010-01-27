def make_graph(triples):
    """Transforms a list of triples into a graph.

    >>> from cloudsizzle.kp import Triple
    >>> triples = [Triple('T-76.4115', 'rdf:type', 'Course'),
    ...     Triple('T-76.4115', 'name', 'Software Development Project'),
    ...     Triple('T-76.4115', 'extent', '5-8')]
    >>> make_graph(triples) #doctest: +NORMALIZE_WHITESPACE
    {uri('T-76.4115'): {uri('rdf:type'): literal('Course'),
                        uri('name'): literal('Software Development Project'),
                        uri('extent'): literal('5-8')}}

    """
    graph = {}
    for triple in triples:
        s, p, o = triple.subject, triple.predicate, triple.object
        if s not in graph:
            graph[s] = {}
        graph[s][p] = o
    return graph
