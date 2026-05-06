"""Basic list implementations."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterable, Iterator, Optional, TypeVar
from collections.abc import MutableSequence

T = TypeVar('T')


@dataclass
class _Node(Generic[T]):
    """A node within a linked list."""
    value: T | None = None
    left: Optional[_Node[T]] = None
    right: Optional[_Node[T]] = None

    def link_as_right(self, node: _Node[T]) -> Optional[_Node[T]]:
        """Set node as right link, and self as node's left link.
        Returns self's previous right node."""
        old = self.right
        self.right = node
        node.left = self
        return old

    def link_as_left(self, node: _Node[T]) -> Optional[_Node[T]]:
        """Set node as left link, and self as node's right link.
        Return self's previous left node."""
        old = self.left
        self.left = node
        node.right = self
        return old


class LinkedList(MutableSequence[T]):
    """A simplified, doubly-linked list."""

    def __init__(self, iterable: Iterable[T] | None = None) -> None:
        self._head: _Node[T] = _Node()
        self._tail: _Node[T] = _Node()
        self._head.link_as_right(self._tail)
        self._count = 0
        if iterable is not None:
            self.extend(iterable)

    def _verify_index(self, index: int, inclusive: bool = False) -> int:
        valid_index_types = (int,)
        index_type = type(index)
        self_type = type(self)
        self_len = len(self)
        offset = 1 if inclusive else 0
        if not issubclass(index_type, valid_index_types):
            raise TypeError(
                f'{self_type.__name__} indices '
                f'must be of the following types: {valid_index_types}; '
                f'not {index_type.__name__}'
            )
        if index < 0:
            index = self_len + index
        if index < 0 - offset or index >= self_len + offset:
            raise IndexError(f'{self_type.__name__} index out of range')
        return index

    def _getnode(self, index: int) -> _Node[T]:
        """Get node by index for insertion.
        Return the node whose right link should be at the given index."""
        cur = self._head
        idx = 0
        while cur.right is not self._tail and idx < index:
            cur = cur.right
            idx += 1
        return cur

    def __len__(self) -> int:
        return self._count

    def __getitem__(self, index: int) -> T:
        index = self._verify_index(index)
        node = self._getnode(index + 1)
        assert node.value is not None
        return node.value

    def __setitem__(self, index: int, value: T) -> None:
        index = self._verify_index(index)
        self._getnode(index + 1).value = value

    def __delitem__(self, index: int) -> None:
        index = self._verify_index(index)
        cur = self._getnode(index + 1)
        assert cur.left is not None and cur.right is not None
        cur.left.link_as_right(cur.right)
        self._count -= 1

    def __iter__(self) -> Iterator[T]:
        cur = self._head
        while cur.right is not self._tail:
            cur = cur.right
            assert cur.value is not None
            yield cur.value

    def __reversed__(self) -> Iterator[T]:
        cur = self._tail
        while cur.left is not self._head:
            cur = cur.left
            assert cur.value is not None
            yield cur.value

    def reverse(self) -> None:
        old_head, old_tail = self._head, self._tail
        cur = self._head
        while cur is not None:
            old_left, old_right = cur.left, cur.right
            cur.left = cur.right
            cur.right = old_left
            cur = old_right
        self._head, self._tail = old_tail, old_head

    def clear(self) -> None:
        self._head.link_as_right(self._tail)
        self._count = 0

    def insert(self, index: int, value: T) -> None:
        index = self._verify_index(index, inclusive=True)
        left = self._getnode(index)
        right = left.right
        assert right is not None
        node = _Node(value, left, right)
        left.link_as_right(node)
        right.link_as_left(node)
        self._count += 1

    def append(self, value: T) -> None:
        prev = self._tail.left
        assert prev is not None
        node = _Node(value, prev, self._tail)
        prev.link_as_right(node)
        self._tail.link_as_left(node)
        self._count += 1
