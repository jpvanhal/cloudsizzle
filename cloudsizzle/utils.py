def make_graph(triples):
    """Transforms a list of triples into a graph.

    >>> from cloudsizzle.kp import Triple, uri, literal
    >>> triples = [Triple('T-76.4115', 'rdf:type', 'Course'),
    ...     Triple('T-76.4115', 'name', 'Software Development Project'),
    ...     Triple('T-76.4115', 'extent', '5-8')]
    >>> expected = {
    ...     uri('T-76.4115'): {
    ...         uri('rdf:type'): literal('Course'),
    ...         uri('name'): literal('Software Development Project'),
    ...         uri('extent'): literal('5-8')
    ...     }
    ... }
    >>> make_graph(triples) == expected
    True

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
    >>> expected = {
    ...     uri('http://cos.alpha.sizl.org/people/ID#dRq9He3yWr3QUKaaWPEYjL'): {
    ...         uri('rdf:type'): literal('http://cos.alpha.sizl.org/people#Person'),
    ...         uri('has_friend'): [
    ...             literal('http://cos.alpha.sizl.org/people/ID#azAC7-RdCr3OiIaaWPfx7J'),
    ...             literal('http://cos.alpha.sizl.org/people/ID#azEe6yRdCr3OiIaaWPfx7J')
    ...         ]
    ...     }
    ... }
    >>> make_graph(triples) == expected
    True

    """
    graph = {}
    for triple in triples:
        s, p, o = triple.subject, triple.predicate, triple.object
        if s not in graph:
            graph[s] = {}
        if p not in graph[s]:
            graph[s][p] = o
        elif isinstance(graph[s][p], list):
            graph[s][p].append(o)
        else:
            graph[s][p] = [graph[s][p], o]
    return graph
