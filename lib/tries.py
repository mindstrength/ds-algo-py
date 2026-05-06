"""Basic trie implementations."""
from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from collections.abc import (
    Callable,
    Collection,
    Iterable,
    Iterator,
    MutableMapping,
    MutableSequence,
    MutableSet,
    Sequence,
)
from typing import Generic, Hashable, TypeVar

E = TypeVar('E', bound=Hashable)
Transformer = Callable[[list[E]], Iterable[E]]


class Trie(Collection[Iterable[E]], ABC, Generic[E]): # pylint: disable=too-few-public-methods
    """A Trie or prefix tree abstract base class."""

    @abstractmethod
    def values_with_prefix(self, prefix: Sequence[E]) -> list[Iterable[E]]:
        """Get values matching the prefix."""
        return []


class _MapTrieNode(Generic[E]): # pylint: disable=too-few-public-methods
    """A node within a MapTrie."""

    def __init__(
        self,
        value: E | None = None,
        children: MutableMapping[E, _MapTrieNode[E]] | None = None,
        word: bool = False,
    ) -> None:
        self.value: E | None = value
        self.children: MutableMapping[E, _MapTrieNode[E]] = children or {}
        self.word = word


class MapTrie(MutableSet[Iterable[E]], Trie[E]):
    """A simplified, mapping-backed trie."""

    def __init__(
        self,
        values: Iterable[Iterable[E]] | None = None,
        mapper: Transformer = list,
    ) -> None:
        self._root: _MapTrieNode[E] = _MapTrieNode()
        self._count = 0
        self._mapper = mapper
        if values is not None:
            for val in values:
                self.add(val)

    def __contains__(self, value: object) -> bool:
        if not isinstance(value, Iterable):
            return False
        cur = self._root
        for elem in value:  # type: ignore[union-attr]
            child = cur.children.get(elem)
            if child is None:
                return False
            cur = child
        return cur.word

    def _dfs_find_words(
        self,
        node: _MapTrieNode[E],
        accumulator: MutableSequence[Iterable[E]],
        transformer: Transformer | None = None,
    ) -> None:
        """Accumulates the words rooted at the given node."""
        def default_transformer(word: list[E]) -> Iterable[E]:
            """Use the trie's mapper to transform the word."""
            return self._mapper(word)
        if transformer is None:
            transformer = default_transformer

        node_queue: deque[tuple[int, _MapTrieNode[E]]] = deque()
        node_queue.append((1, node))
        cur_word: list[E] = []
        while node_queue:
            cur_depth, cur_node = node_queue.pop()
            cur_word = cur_word[:cur_depth - 1]
            assert cur_node.value is not None
            cur_word.append(cur_node.value)
            if cur_node.word:
                accumulator.append(transformer(cur_word))
            for cur_child in cur_node.children.values():
                node_queue.append((cur_depth + 1, cur_child))

    def __iter__(self) -> Iterator[Iterable[E]]:
        values: list[Iterable[E]] = []
        for root_child in self._root.children.values():
            self._dfs_find_words(root_child, values)
        return iter(values)

    def __len__(self) -> int:
        return self._count

    def add(self, value: Iterable[E]) -> None:
        cur = self._root
        for elem in value:
            child = cur.children.get(elem)
            if child is None:
                child = _MapTrieNode(elem)
                cur.children[elem] = child
            cur = child
        if cur is self._root or cur.word:
            return
        cur.word = True
        self._count += 1

    def discard(self, value: Iterable[E]) -> None:
        cur = self._root
        temp: list[_MapTrieNode[E]] = []
        for elem in value:
            child = cur.children.get(elem)
            if child is None:
                return
            temp.append(child)
            cur = child
        if not temp:
            return
        temp.reverse()
        if not temp[0].word:
            return
        to_del: _MapTrieNode[E] | None = None
        for cur_node in temp:
            if to_del is None:
                cur_node.word = False
                if cur_node.children:
                    self._count -= 1
                    return
                to_del = cur_node
            else:
                assert to_del.value is not None
                cur_node.children.pop(to_del.value)
                if cur_node.children or cur_node.word:
                    self._count -= 1
                    return
                to_del = cur_node
        assert to_del is not None and to_del.value is not None
        self._root.children.pop(to_del.value)
        self._count -= 1

    def clear(self) -> None:
        self._root.children = {}
        self._count = 0

    def values_with_prefix(self, prefix: Sequence[E]) -> list[Iterable[E]]:
        def append_word_ending(ending: list[E]) -> Iterable[E]:
            return self._mapper(prefix_sequence + ending)

        prefix_sequence: list[E] = list(prefix[:-1])
        cur = self._root
        values: list[Iterable[E]] = []
        for elem in prefix:
            child = cur.children.get(elem)
            if child is None:
                return values
            cur = child
        self._dfs_find_words(cur, values, append_word_ending)
        return values
