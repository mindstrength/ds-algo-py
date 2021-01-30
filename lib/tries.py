'''Basic trie implementations.'''

from collections.abc import (
    MutableSet as _MS,
    Iterable as _Itbl,
    MutableMapping as _MM
)

from typing import (
    Any as _Any
)

class _MapNode:  # pylint: disable=too-few-public-methods
    '''A node within a MapTrie.'''

    def __init__(self, value: _Any = None, children: _MM = None,
                 word: bool = False):
        self.value = value
        self.children = children or dict()
        self.word = word

class MapTrie(_MS):
    '''A simplified, mapping-backed trie.'''

    def __init__(self, iterable: _Itbl = None):
        self._root = _MapNode()
        self._count = 0
        if iterable:
            for val in iterable:
                self.add(val)

    def __contains__(self, value: _Itbl):
        cur = self._root
        for elem in value:
            child = cur.children.get(elem)
            if not child:
                return False
            cur = child
        return bool(cur and cur.word)

    def __iter__(self):
        pass # TODO: implement '__iter__'.

    def __len__(self):
        return self._count

    def add(self, value: _Itbl):
        cur = self._root
        for elem in value:
            child = cur.children.get(elem)
            if not child:
                child = _MapNode(elem)
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
