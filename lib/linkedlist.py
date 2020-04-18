'''A simplified, doubly-linked list.'''

from dataclasses import dataclass as _data
from typing import Any as _Any
from collections.abc import MutableSequence as _MS, Collection as _Col


@_data
class _Node:
    '''A node within a linked list.'''
    value: _Any
    left: _Any
    right: _Any


class LinkedList(_MS):
    '''A simplified, doubly-linked list.'''

    def __init__(self, collection: _Col = None):
        self.head = _Node(None, None, None)
        self.tail = _Node(None, self.head, None)
        self.head.right = self.tail
        self.count = 0
        if collection:
            self.extend(collection)

    def _verify_index(self, index, inclusive=False):
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

    def __len__(self):
        return self.count

    def __getitem__(self, index):
        index = self._verify_index(index)
        return self._getnode(index + 1).value

    def _getnode(self, index):
        '''Get node by index.'''
        cur = self.head
        idx = 0
        while cur.right is not self.tail and idx < index:
            cur = cur.right
            idx += 1
        return cur

    def __setitem__(self, index, value):
        index = self._verify_index(index)
        self._getnode(index + 1).value = value

    def __delitem__(self, index):
        index = self._verify_index(index)
        cur = self._getnode(index + 1)
        left, right = cur.left, cur.right
        left.right, right.left = cur.right, cur.left
        self.count -= 1

    def insert(self, index, value):
        index = self._verify_index(index, inclusive=True)
        left = self._getnode(index)
        right = left.right
        node = _Node(value, left, right)
        left.right, right.left = node, node
        self.count += 1
