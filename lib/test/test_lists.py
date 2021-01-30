'''Unit tests for 'lists' module.'''

import unittest as _ut
from lists import LinkedList


class LinkedListTest(_ut.TestCase):
    '''Unit tests for LinkedList class.'''

    def setUp(self):
        self.list = LinkedList()

    def test_append(self):
        '''Append should increase size by one.'''
        size = len(self.list)
        self.list.append('a')
        self.assertEqual(size + 1, len(self.list))

    def test_iter_empty(self):
        '''Empty iterator should immediately stop iteration.'''
        i = iter(self.list)
        with self.assertRaises(StopIteration):
            next(i)

    def test_iter_populated(self):
        '''Populated iterator should iteratore over elements.'''
        self.list = LinkedList([1, 2, 3])
        i = iter(self.list)
        self.assertSequenceEqual([1, 2, 3], list(i))

    def test_reversed_empty(self):
        '''Reversed empty list should immediately stop iteration.'''
        r_list = reversed(self.list)
        with self.assertRaises(StopIteration):
            next(r_list)

    def test_reversed_populated(self):
        '''Reversed empty list should lazily iterate in reverse order.'''
        self.list = LinkedList([1, 2, 3])
        r_list = reversed(self.list)
        self.assertSequenceEqual([3, 2, 1], list(r_list))

    def test_reverse_empty(self):
        '''In-place reverse on empty list should be empty.'''
        self.list.reverse()
        self.assertSequenceEqual([], self.list)

    def test_reverse_populated(self):
        '''In-place reverse on populated list should reverse order of list.'''
        self.list = LinkedList([1, 2, 3])
        self.list.reverse()
        self.assertSequenceEqual([3, 2, 1], self.list)

    def test_clear(self):
        '''Clear should empty the list.'''
        self.list = LinkedList([1, 2, 3])
        self.list.clear()
        self.assertSequenceEqual([], self.list)

    def test_getitem_invalid_index_type(self):
        '''Invalid index type should raise TypeError.'''
        with self.assertRaises(TypeError):
            self.list['a']

    def test_getitem_invalid_index_range(self):
        '''Invalid index range should raise IndexError.'''
        with self.assertRaises(IndexError):
            self.list[-100]

    def test_getitem_index_lower_bound(self):
        '''Lower bound should return first element.'''
        self.list.append('a')
        self.assertEqual('a', self.list[0])

    def test_getitem_index_upper_bound(self):
        '''Upper bound should return last element.'''
        self.list = LinkedList('ab')
        self.assertEqual('b', self.list[1])
        self.assertEqual('b', self.list[-1])

    def test_setitem_index_lower_boud(self):
        '''Lower bound should set first element.'''
        self.list.append('a')
        self.list[0] = 'b'
        self.assertEqual('b', self.list[0])

    def test_setitem_index_upper_boud(self):
        '''Upper bound should set last element.'''
        self.list = LinkedList('ab')
        self.list[1] = 'c'
        self.assertEqual('c', self.list[1])
        self.list[-1] = 'd'
        self.assertEqual('d', self.list[-1])

    def test_delitem_index_lower_boud(self):
        '''Lower bound should delete first element.'''
        self.list.append('a')
        del self.list[0]
        self.assertEqual(0, len(self.list))

    def test_delitem_index_upper_boud(self):
        '''Upper bound should delete last element.'''
        self.list = LinkedList('abc')
        del self.list[2]
        self.assertEqual('b', self.list[1])
        del self.list[-1]
        self.assertEqual('a', self.list[-1])

    def test_insert(self):
        '''Insert should insert element at index, pushing other elements.'''
        self.list.insert(0, 'b')
        self.list.insert(0, 'a')
        self.list.insert(len(self.list), 'c')
        self.assertSequenceEqual('abc', self.list)

    def test_extend_collection(self):
        '''Extend should append the elements of other collection.'''
        self.list.extend('abc')
        self.assertSequenceEqual('abc', self.list)
