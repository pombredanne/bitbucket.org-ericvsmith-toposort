#######################################################################
# Tests for toposort module.
#
# Copyright 2014 True Blade Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Notes:
#
########################################################################

import unittest

from toposort import toposort, toposort_flatten

class TestCase(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(list(toposort({2: {11},
                                        9: {11, 8},
                                        10: {11, 3},
                                        11: {7, 5},
                                        8: {7, 3},
                                        })),
                         [{3, 5, 7},
                          {8, 11},
                          {2, 9, 10},
                          ])

        # make sure self dependencies are ignored
        self.assertEqual(list(toposort({2: {2, 11},
                                        9: {11, 8},
                                        10: {10, 11, 3},
                                        11: {7, 5},
                                        8: {7, 3},
                                        })),
                         [{3, 5, 7},
                          {8, 11},
                          {2, 9, 10},
                          ])

        self.assertEqual(list(toposort({1: set()})),
                         [{1}])
        self.assertEqual(list(toposort({1: {1}})),
                         [{1}])

    def test_no_dependencies(self):
        self.assertEqual(list(toposort({1: {2},
                                        3: {4},
                                        5: {6},
                                        })),
                         [{2, 4, 6}, {1, 3, 5}])

        self.assertEqual(list(toposort({1: set(),
                                        3: set(),
                                        5: set(),
                                        })),
                         [{1, 3, 5}])

    def test_empty(self):
        self.assertEqual(list(toposort({})),
                         [])

    def test_strings(self):
        self.assertEqual(list(toposort({'2': {'11'},
                                        '9': {'11', '8'},
                                        '10': {'11', '3'},
                                        '11': {'7', '5'},
                                        '8': {'7', '3'},
                                        })),
                         [{'3', '5', '7'},
                          {'8', '11'},
                          {'2', '9', '10'},
                          ])

    def test_objects(self):
        o2 = object()
        o3 = object()
        o5 = object()
        o7 = object()
        o8 = object()
        o9 = object()
        o10 = object()
        o11 = object()
        self.assertEqual(list(toposort({o2: {o11},
                                        o9: {o11, o8},
                                        o10: {o11, o3},
                                        o11: {o7, o5},
                                        o8: {o7, o3, o8},
                                        })),
                         [{o3, o5, o7},
                          {o8, o11},
                          {o2, o9, o10},
                          ])

    def test_cycle(self):
        # a simple, 2 element cycle
        self.assertRaises(ValueError, list, toposort({1: {2},
                                                      2: {1}
                                                      }))

        # an indirect cycle
        self.assertRaises(ValueError, list, toposort({1: {2},
                                                      2: {3},
                                                      3: {1},
                                                      }))

    def test_input_not_modified(self):
        data = {2: {11},
                9: {11, 8},
                10: {11, 3},
                11: {7, 5},
                8: {7, 3, 8},  # includes something self-referential
                }
        orig = data.copy()
        results = list(toposort(data))
        self.assertEqual(data, orig)

    def test_input_not_modified_when_cycle_error(self):
        data = {1: {2},
                2: {1},
                3: {4},
                }
        orig = data.copy()
        self.assertRaises(ValueError, list, toposort(data))
        self.assertEqual(data, orig)


class TestCaseAll(unittest.TestCase):
    def test_sort_flatten(self):
        data = {2: {11},
                9: {11, 8},
                10: {11, 3},
                11: {7, 5},
                8: {7, 3, 8},  # includes something self-referential
                }
        expected = [{3, 5, 7}, {8, 11}, {2, 9, 10}]
        self.assertEqual(list(toposort(data)), expected)

        # now check the sorted results
        results = []
        for item in expected:
            results.extend(sorted(item))
        self.assertEqual(toposort_flatten(data), results)

        # and the unsorted results. break the results up into groups to compare them
        actual = toposort_flatten(data, False)
        results = [{i for i in actual[0:3]}, {i for i in actual[3:5]}, {i for i in actual[5:8]}]
        self.assertEqual(results, expected)

class TestAll(unittest.TestCase):
    def test_all(self):
        import toposort

        # check that __all__ in the module contains everything that should be
        #  public, and only those symbols
        all = set(toposort.__all__)

        for sym in dir(toposort):
            if not sym.startswith('_'):
                self.assertIn(sym, all, 'symbol missing from __all__')
                all.remove(sym)
        self.assertEqual(all, set(), 'unexpected symbol in __all__')

unittest.main()
