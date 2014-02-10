========
toposort
========

Overview
========

Implements a topological sort algorith.

From `Wikipedia <http://en.wikipedia.org/wiki/Topological_sorting>`_:
In computer science, a topological sort (sometimes abbreviated topsort
or toposort) or topological ordering of a directed graph is a linear
ordering of its vertices such that for every directed edge uv from
vertex u to vertex v, u comes before v in the ordering.

Typical usage
=============

The interpretation here is: If 2 depends on 11, 9 depends on 11 and 8,
10 depends on 11 and 3 (and so on), then in what order should we
process the items such that all items are processed before any of
their dependencies?::

    >>> from __future__ import print_function
    >>> from toposort import toposort
    >>> list(toposort({2: {2, 11},
    ...                9: {11, 8},
    ...                10: {11, 3},
    ...                11: {7, 5},
    ...                8: {7, 3},
    ...               }))
    [{3, 5, 7}, {8, 11}, {9, 2, 10}]

And the answer is: process 3, 5, and 7 (in any order), then process 8
and 11, then process 2, 9, and 10.

Circular dependencies
=====================

A circular dependency will raise a ValueError. Here 1 depends on 2,
and 2 depends on 1::

    >>> list(toposort({1: {2},
    ...                2: {1},
    ...               }))
    Traceback (most recent call last):
        ...
    ValueError: Cyclic dependencies exist among these items: (1, {2}) ,(2, {1})


Module contents
===============

toposort(data)

toposort_all(data, sort=True)
