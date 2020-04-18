'''Unit tests for linkedlist module.'''

import unittest as _ut
from linkedlist import LinkedList

class LinkedListTest(_ut.TestCase):
    '''Unit tests for LinkedList class.'''
    def setUp(self):
        self.list = LinkedList()

    def test_append(self):
        '''Append should increase size by one.'''
        size = len(self.list)
        self.list.append('a')
        self.assertEqual(size + 1, len(self.list))

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
        self.list.extend('ab')
        self.assertEqual('b', self.list[1])
        self.assertEqual('b', self.list[-1])

    def test_setitem_index_lower_boud(self):
        '''Lower bound should set first element.'''
        self.list.append('a')
        self.list[0] = 'b'
        self.assertEqual('b', self.list[0])

    def test_setitem_index_upper_boud(self):
        '''Upper bound should set last element.'''
        self.list.extend('ab')
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
        self.list.extend('abc')
        del self.list[2]
        self.assertEqual('b', self.list[1])
        del self.list[-1]
        self.assertEqual('a', self.list[-1])

    def test_insert(self):
        '''Insert should insert element at index, pushing other elements.'''
        self.list.insert(0, 'b')
        self.list.insert(0, 'a')
        self.list.insert(len(self.list), 'c')
        self.assertSequenceEqual(['a', 'b', 'c'], self.list)
