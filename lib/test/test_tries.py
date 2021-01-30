'''Unit tests for 'tries' module.'''

import unittest as _ut
from tries import MapTrie

class MapTrieTest(_ut.TestCase):
    '''Unit tests for MapTrie class.'''
    def setUp(self):
        self.trie = MapTrie()

    def test_add_unique(self):
        '''Add unique value should increase size by one and return True.'''
        size = len(self.trie)
        res = self.trie.add('abc')
        self.assertEqual(size + 1, len(self.trie))
        self.assertTrue(res)

    def test_add_duplicate(self):
        '''Add duplicate value should keep size and return False.'''
        self.trie = MapTrie(['abc'])
        size = len(self.trie)
        res = self.trie.add('abc')
        self.assertEqual(size, len(self.trie))
        self.assertFalse(res)

    def test_contains_absent(self):
        '''Contains when absent should return False.'''
        res = 'abc' in self.trie
        self.assertFalse(res)

    def test_contains_present(self):
        '''Contains when present should return True.'''
        self.trie = MapTrie(['abc'])
        res = 'abc' in self.trie
        self.assertTrue(res)

    def test_clear(self):
        '''Clear should make empty.'''
        self.trie = MapTrie(['abc'])
        self.trie.clear()
        self.assertEqual(0, len(self.trie))

    def test_discard_absent(self):
        '''Discard when value is absent should not alter len.'''
        self.trie = MapTrie(['abc'])
        self.trie.discard('xyz')
        self.assertEqual(1, len(self.trie))

    def test_discard_value_empty(self):
        '''Discard when value is empty should not alter len.'''
        self.trie = MapTrie(['abc'])
        self.trie.discard('')
        self.assertEqual(1, len(self.trie))

    def test_discard_partial_match(self):
        '''Discard when value is only a partial match should not alter len.'''
        self.trie = MapTrie(['abc'])
        self.trie.discard('ab')
        self.assertEqual(1, len(self.trie))

    def test_discard_present_no_shared_prefix(self):
        '''Discard when value is present should decrement len.'''
        self.trie = MapTrie(['abc', 'def'])
        self.trie.discard('abc')
        self.assertEqual(1, len(self.trie))

    def test_discard_present_shared_prefix_short(self):
        '''Discard when shorter value is present should decrement len.'''
        self.trie = MapTrie(['ab', 'abc', 'abd', 'efg'])
        self.trie.discard('ab')
        self.assertEqual(3, len(self.trie))

    def test_discard_present_shared_prefix_long(self):
        '''Discard when longer value is present should decrement len.'''
        self.trie = MapTrie(['ab', 'abc', 'abd', 'efg'])
        self.trie.discard('abd')
        self.assertEqual(3, len(self.trie))
