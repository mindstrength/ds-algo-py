'''Basic trie implementations.'''

from collections import (
    deque as _Deq
)
from collections.abc import (
    MutableSet as _MS,
    Iterable as _Itbl,
    MutableMapping as _MM
)

class _MapTrieNode:  # pylint: disable=too-few-public-methods
    '''A node within a MapTrie.'''

    def __init__(self, value = None, children: _MM = None,
                 word: bool = False):
        self.value = value
        self.children = children or dict()
        self.word = word

class MapTrie(_MS):
    '''A simplified, mapping-backed trie.'''

    def __init__(self, values: _Itbl = None):
        self._root = _MapTrieNode()
        self._count = 0
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
        return bool(cur and cur.word)

    def __iter__(self):
        def dfs_find_word(node: _MapTrieNode):
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
                    entries.append(cur_word)
                # push node's children.
                for cur_child in cur_node.children.values():
                    node_queue.append((cur_depth + 1, cur_child))
        entries = []
        for root_child in self._root.children.values():
            dfs_find_word(root_child)
        return iter(entries)


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
