'''Unit tests for 'heaps' module.''' 

import unittest as _ut
from heaps import Heap


class HeapTest(_ut.TestCase):
    '''Unit tests for Heap class.'''

    def test_empty_heap_len(self):
        heap = Heap[int]()
        self.assertEqual(0, len(heap))

    def test_peek_empty_raises(self):
        heap = Heap[int]()
        with self.assertRaises(IndexError):
            heap.peek()

    def test_pop_empty_raises(self):
        heap = Heap[int]()
        with self.assertRaises(IndexError):
            heap.pop()

    def test_replace_empty_raises(self):
        heap = Heap[int]()
        with self.assertRaises(IndexError):
            heap.replace(1)

    def test_add_and_peek(self):
        heap = Heap([3, 1, 2])
        self.assertEqual(1, heap.peek())
        heap.add(0)
        self.assertEqual(0, heap.peek())

    def test_pop_returns_sorted_elements(self):
        heap = Heap([5, 1, 3, 2, 4])
        result = [heap.pop() for _ in range(len(heap))]
        self.assertEqual([1, 2, 3, 4, 5], result)
        self.assertEqual(0, len(heap))

    def test_clear_empties_heap(self):
        heap = Heap([2, 1, 3])
        heap.clear()
        self.assertEqual(0, len(heap))
        with self.assertRaises(IndexError):
            heap.peek()

    def test_contains(self):
        heap = Heap(['c', 'a', 'b'])
        self.assertIn('a', heap)
        self.assertNotIn('z', heap)

    def test_iter_returns_internal_order(self):
        heap = Heap([4, 1, 3, 2])
        self.assertListEqual(list(heap), heap._data)

    def test_pushpop_returns_smaller_value(self):
        heap = Heap([2, 5, 3])
        result = heap.pushpop(1)
        self.assertEqual(1, result)
        self.assertEqual(2, heap.peek())

    def test_pushpop_empty_returns_value(self):
        heap = Heap[int]()
        result = heap.pushpop(1)
        self.assertEqual(1, result)
        self.assertEqual(0, len(heap))

    def test_pushpop_replaces_root(self):
        heap = Heap([2, 5, 3])
        result = heap.pushpop(4)
        self.assertEqual(2, result)
        self.assertEqual(3, heap.peek())

    def test_replace_swaps_root(self):
        heap = Heap([2, 5, 3])
        root = heap.replace(4)
        self.assertEqual(2, root)
        self.assertEqual(3, heap.peek())

    def test_custom_comparator_max_heap(self):
        comparator = lambda left, right: left > right
        heap = Heap([1, 4, 2, 5, 3], comparator=comparator)
        self.assertEqual(5, heap.peek())
        self.assertEqual([5, 4, 3, 2, 1], [heap.pop() for _ in range(len(heap))])

    def test_heapify_from_iterable(self):
        data = [10, 2, 8, 6, 4]
        heap = Heap(data)
        self.assertEqual(2, heap.peek())
        self.assertEqual(5, len(heap))

    def test_push_and_pop_sequence(self):
        heap = Heap[int]()
        for value in [6, 1, 8, 3, 7, 2, 5, 4]:
            heap.add(value)
        self.assertEqual(1, heap.peek())
        popped = [heap.pop() for _ in range(len(heap))]
        self.assertEqual(list(range(1, 9)), popped)
