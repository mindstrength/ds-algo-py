"""Array-backed heap implementation with comparator support."""
from __future__ import annotations

from collections.abc import Callable, Collection, Iterable, Iterator
from typing import Generic, TypeVar

T = TypeVar('T')
Comparator = Callable[[T, T], bool]


def _default_comparator(left: T, right: T) -> bool:
    return left < right


class Heap(Collection[T], Generic[T]):
    """A simple array-backed heap that implements the Collection ABC."""

    def __init__(
        self,
        iterable: Iterable[T] | None = None,
        comparator: Comparator | None = None,
    ) -> None:
        self._comparator: Comparator = comparator or _default_comparator
        self._data: list[T] = list(iterable) if iterable is not None else []
        if self._data:
            self._heapify()

    def __contains__(self, value: object) -> bool:
        """Return True when value exists in the heap."""
        return value in self._data

    def __iter__(self) -> Iterator[T]:
        """Iterate over the heap's backing array."""
        return iter(self._data)

    def __len__(self) -> int:
        """Return the number of elements stored in the heap."""
        return len(self._data)

    def __repr__(self) -> str:
        """Return the heap representation."""
        return f'Heap({self._data!r})'

    def add(self, value: T) -> None:
        """Insert value and restore the heap invariant."""
        self._data.append(value)
        self._sift_up(len(self._data) - 1)

    push = add

    def peek(self) -> T:
        """Return the root element without removing it."""
        if not self._data:
            raise IndexError('peek from empty heap')
        return self._data[0]

    def pop(self) -> T:
        """Remove and return the root element from the heap."""
        if not self._data:
            raise IndexError('pop from empty heap')
        root = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sift_down(0)
        return root

    def replace(self, value: T) -> T:
        """Replace the root element and restore the heap invariant."""
        if not self._data:
            raise IndexError('replace from empty heap')
        root = self._data[0]
        self._data[0] = value
        self._sift_down(0)
        return root

    def pushpop(self, value: T) -> T:
        """Push value then pop and return the root element efficiently."""
        if not self._data or self._comparator(value, self._data[0]):
            return value
        root = self._data[0]
        self._data[0] = value
        self._sift_down(0)
        return root

    def clear(self) -> None:
        """Remove all elements from the heap."""
        self._data.clear()

    def _heapify(self) -> None:
        for index in range((len(self._data) // 2) - 1, -1, -1):
            self._sift_down(index)

    def _sift_up(self, index: int) -> None:
        while index > 0:
            parent = (index - 1) // 2
            if self._comparator(self._data[index], self._data[parent]):
                self._data[parent], self._data[index] = (
                    self._data[index],
                    self._data[parent],
                )
                index = parent
            else:
                break

    def _sift_down(self, index: int) -> None:
        size = len(self._data)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            preferred = index
            if left < size and self._comparator(self._data[left], self._data[preferred]):
                preferred = left
            if right < size and self._comparator(self._data[right], self._data[preferred]):
                preferred = right
            if preferred == index:
                break
            self._data[index], self._data[preferred] = self._data[preferred], self._data[index]
            index = preferred
