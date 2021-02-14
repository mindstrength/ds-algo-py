'''Basic list implementations.'''

from dataclasses import (
    dataclass as _data
)

from typing import (
    Any as _Any
)

from collections.abc import (
    MutableSequence as _MS,
    Iterable as _Itbl
)


@_data
class _Node:
    '''A node within a linked list.'''
    value: _Any = None
    left: _Any = None
    right: _Any = None

    def link_as_right(self, node):
        '''Set node as right link, and self as node's left link.
        Returns self's previous right node.'''
        old = self.right
        self.right = node
        node.left = self
        return old

    def link_as_left(self, node):
        '''Set node as left link, and self as node's right link.
        Return self's previous left node.'''
        old = self.left
        self.left = node
        node.right = self
        return old


class LinkedList(_MS):  # pylint: disable=too-many-ancestors
    '''A simplified, doubly-linked list.'''

    def __init__(self, iterable: _Itbl = None):
        self._head = _Node()
        self._tail = _Node()
        self._head.link_as_right(self._tail)
        self._count = 0
        if iterable:
            self.extend(iterable)

    def _verify_index(self, index, inclusive: bool = False):
        valid_index_types = (int,)
        index_type = type(index)
        self_type = type(self)
        self_len = len(self)
        offset = 1 if inclusive else 0
        if not issubclass(index_type, valid_index_types):
            raise TypeError(
                f'{self_type.__name__} indices '
                + f'must be of the following types: {valid_index_types}; '
                + f'not {index_type.__name__}'
            )
        if index < 0:
            index = self_len + index
        if index < 0 - offset or index >= self_len + offset:
            raise IndexError(f'{self_type.__name__} index out of range')
        return index

    def _getnode(self, index):
        '''Get node by index for insertion.
        Return the node whose right link should be at the given index.'''
        cur = self._head
        idx = 0
        while cur.right is not self._tail and idx < index:
            cur = cur.right
            idx += 1
        return cur

    def __len__(self):
        return self._count

    def __getitem__(self, index):
        index = self._verify_index(index)
        return self._getnode(index + 1).value

    def __setitem__(self, index, value):
        index = self._verify_index(index)
        self._getnode(index + 1).value = value

    def __delitem__(self, index):
        index = self._verify_index(index)
        cur = self._getnode(index + 1)
        cur.left.link_as_right(cur.right)
        self._count -= 1

    def __iter__(self):
        cur = self._head
        while cur.right is not self._tail:
            cur = cur.right
            yield cur.value

    def __reversed__(self):
        cur = self._tail
        while cur.left is not self._head:
            cur = cur.left
            yield cur.value

    def reverse(self):
        old_head, old_tail = self._head, self._tail
        cur = self._head
        while cur is not None:
            old_left, old_right = cur.left, cur.right
            cur.left = cur.right
            cur.right = old_left
            cur = old_right
        self._head, self._tail = old_tail, old_head

    def clear(self):
        self._head.link_as_right(self._tail)
        self._count = 0

    def insert(self, index, value):
        index = self._verify_index(index, inclusive=True)
        left = self._getnode(index)
        right = left.right
        node = _Node(value, left, right)
        left.link_as_right(node)
        right.link_as_left(node)
        self._count += 1

    def append(self, value):
        prev = self._tail.left
        node = _Node(value, prev, self._tail)
        prev.link_as_right(node)
        self._tail.link_as_left(node)
        self._count += 1
