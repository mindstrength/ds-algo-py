'''Basic trie implementations.'''

from abc import (
    ABC as _ABC,
    abstractmethod as _abstract
)

from collections import (
    deque as _Deq
)
from collections.abc import (
    Collection as _Col,
    MutableSequence as _MSeq,
    MutableSet as _MSet,
    Iterable as _Itbl,
    MutableMapping as _MMap
)

class Trie(_ABC, _Col): # pylint: disable=too-few-public-methods
    '''A Trie or prefix tree abstract base class.'''
    @_abstract
    def values_with_prefix(self, prefix):
        '''Get values matching the prefix.'''
        return []


class _MapTrieNode:  # pylint: disable=too-few-public-methods
    '''A node within a MapTrie.'''

    def __init__(self, value = None, children: _MMap = None,
                 word: bool = False):
        self.value = value
        self.children = children or dict()
        self.word = word

class MapTrie(_MSet, Trie): # pylint: disable=too-many-ancestors
    '''A simplified, mapping-backed trie.'''

    def __init__(self, values: _Itbl = None, mapper = list):
        self._root = _MapTrieNode()
        self._count = 0
        self._mapper = mapper
        if values:
            for val in values:
                self.add(val)

    def __contains__(self, value: _Itbl):
        cur = self._root
        for elem in value:
            child = cur.children.get(elem)
            if not child:
                return False
            cur = child
        return cur.word

    def _dfs_find_words(self, node: _MapTrieNode, accumulator: _MSeq,
                         transformer = lambda x: x):
        '''Accumulates the words rooted at the given node.'''
        node_queue = _Deq()
        node_queue.append((1, node)) # (depth, node)
        cur_word = []
        while node_queue:
            # pop node.
            cur_depth, cur_node = node_queue.pop()
            # visit node.
            cur_word = cur_word[:cur_depth - 1]
            cur_word.append(cur_node.value)
            if cur_node.word:
                accumulator.append(transformer(self._mapper(cur_word)))
            # push node's children.
            for cur_child in cur_node.children.values():
                node_queue.append((cur_depth + 1, cur_child))

    def __iter__(self):
        values = []
        for root_child in self._root.children.values():
            self._dfs_find_words(root_child, values)
        return iter(values)

    def __len__(self):
        return self._count

    def add(self, value: _Itbl):
        cur = self._root
        for elem in value:
            child = cur.children.get(elem)
            if not child:
                child = _MapTrieNode(elem)
                cur.children[elem] = child
            cur = child
        if cur is self._root or cur.word:
            return False
        cur.word = True
        self._count += 1
        return True

    def discard(self, value: _Itbl):
        cur = self._root
        temp = []
        for elem in value:
            child = cur.children.get(elem)
            if not child:
                return
            temp.append(child)
            cur = child
        if not temp:
            return
        temp.reverse()
        if not temp[0].word:
            return
        to_del = None
        for cur in temp:
            if not to_del:
                cur.word = False
                if cur.children:
                    self._count -= 1
                    return
                to_del = cur
            else:
                cur.children.pop(to_del.value)
                if cur.children or cur.word:
                    self._count -= 1
                    return
                to_del = cur
        self._root.children.pop(to_del.value)
        self._count -= 1

    def clear(self):
        self._root.children = dict()
        self._count = 0

    def values_with_prefix(self, prefix):
        def append_word_ending(ending):
            return prefix[:len(prefix) - 1] + ending
        cur = self._root
        values = []
        for elem in prefix:
            child = cur.children.get(elem)
            if not child:
                return values
            cur = child
        self._dfs_find_words(cur, values, append_word_ending)
        return values
