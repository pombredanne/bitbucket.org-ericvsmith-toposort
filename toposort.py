# originally from http://code.activestate.com/recipes/578272-topological-sort/
# with modifications by Eric V. Smith (eric@trueblade.com)
#  2013-11-05: Added unittests.
#              Deleted doctests (maybe not the best idea in the
#                world, but it cleans up the docstring.
#              Moved functools import to the top of the file
#              Changed assert to a ValueError
#              Changed iter[items|keys] to [items|keys], for
#                python 3 compatibility. I don't think it matters
#                for python 2 these are now lists instead of
#                iterables.
#              Copy the input so as to leave it unmodified.
#              Renamed function from toposort2 to toposort.
#              Handle empty input.
#              Switch tests to use set literals.

from functools import reduce

def toposort(data):
    """Dependencies are expressed as a dictionary whose keys are items
and whose values are a set of dependent items. Output is a list of
sets in topological order. The first set consists of items with no
dependences, each subsequent set consists of items that depend upon
items in the preceeding sets.
"""

    # Special case an empty input.
    if not data:
        return

    # Copy the input so as to leave it unmodified.
    data = data.copy()

    # Ignore self dependencies.
    for k, v in data.items():
        v.discard(k)
    # Find all items that don't depend on anything.
    extra_items_in_deps = reduce(set.union, data.values()) - set(data.keys())
    # Add empty dependences where needed.
    data.update({item:set() for item in extra_items_in_deps})
    while True:
        ordered = set(item for item, dep in data.items() if not dep)
        if not ordered:
            break
        yield ordered
        data = {item: (dep - ordered)
                for item, dep in data.items()
                    if item not in ordered}
    if data:
        raise ValueError('Cyclic dependencies exist among these items: {}'.format(' ,'.join(repr(x) for x in data.items())))


def toposort_all(data, sort=True):
    """Returns a single list of dependencies. For any set returned by
toposort(), those items are sorted and appended to the result (just to
make the results deterministic."""

    result = []
    for d in toposort(data):
        result.extend((sorted if sort else list)(d))
    return result


