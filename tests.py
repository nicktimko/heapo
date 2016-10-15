"""
Unittests for heapq (<cpython>/Lib/test/test_heapq.py) ported for use with
a heap object
"""

import random
import unittest

from test import support
from unittest import TestCase, skipUnless
from operator import itemgetter

from bikeheap import BikeHeap


class TestHeap(TestCase):

    def setUp(self):
        self.heap_type = BikeHeap

    def test_push_pop(self):
        # 1) Push 256 random numbers and pop them off, verifying all's OK.
        heap = self.heap_type([])
        data = []
        self.check_invariant(heap)
        for i in range(256):
            item = random.random()
            data.append(item)
            heap.push(item)
            self.check_invariant(heap)
        results = []
        while heap:
            item = heap.pop()
            self.check_invariant(heap)
            results.append(item)
        data_sorted = data[:]
        data_sorted.sort()
        self.assertEqual(data_sorted, results)
        # 2) Check that the invariant holds for a sorted array
        self.check_invariant(results)

        heap = self.heap_type([])
        self.assertRaises(TypeError, heap.push)
        try:
            self.assertRaises(TypeError, heap.push, None, None)
            self.assertRaises(TypeError, heap.pop, None)
        except AttributeError:
            pass

    def check_invariant(self, heap):
        if type(heap) == self.heap_type:
            heap = heap.heap # extract the actual heap out of the implementation
        elif isinstance(heap, list):
            pass
        else:
            heap = list(heap)
        # Check the heap invariant.
        for pos, item in enumerate(heap):
            if pos: # pos 0 has no parent
                parentpos = (pos-1) >> 1
                self.assertTrue(heap[parentpos] <= item)

    def test_heapinit(self):
        for size in list(range(30)) + [20000]:
            heap = [random.random() for dummy in range(size)]
            heap = self.heap_type(heap)
            self.check_invariant(heap)

        self.assertRaises(TypeError, self.heap_type, None)

    def test_peek(self):
        for _ in range(10):
            init_data = [random.random() for _ in range(100)]
            min_ = min(init_data)
            heap = self.heap_type(init_data)
            self.assertEqual(heap.peek(), min_)

            for _ in range(10):
                x = random.random() / 20
                min_ = min(min_, x)
                heap.push(x)
                self.assertEqual(heap.peek(), min_)

    def test_naive_nbest(self):
        data = [random.randrange(2000) for i in range(1000)]
        heap = self.heap_type([])
        for item in data:
            heap.push(item)
            if len(heap) > 10:
                heap.pop()
        self.assertEqual(sorted(heap), sorted(data)[-10:])

    def heapiter(self, heap):
        # An iterator returning a heap's elements, smallest-first.
        try:
            while 1:
                yield heap.pop()
        except IndexError:
            pass

    def test_nbest(self):
        # Less-naive "N-best" algorithm, much faster (if len(data) is big
        # enough <wink>) than sorting all of data.  However, if we had a max
        # heap instead of a min heap, it could go faster still via
        # heapify'ing all of data (linear time), then doing 10 heappops
        # (10 log-time steps).
        data = [random.randrange(2000) for i in range(1000)]
        heap = data[:10]
        heap = self.heap_type(heap)
        for item in data[10:]:
            if item > heap.peek():  # this gets rarer the longer we run
                heap.replace(item)
        self.assertEqual(list(self.heapiter(heap)), sorted(data)[-10:])

        self.assertRaises(TypeError, heap.replace)
        self.assertRaises(IndexError, heap.replace, None)

    def test_nbest_with_pushpop(self):
        data = [random.randrange(2000) for i in range(1000)]
        heap = data[:10]
        heap = self.heap_type(heap)
        for item in data[10:]:
            heap.pushpop(item)
        self.assertEqual(list(self.heapiter(heap)), sorted(data)[-10:])
        self.assertEqual(self.heap_type([]).pushpop('x'), 'x')

    def test_heappushpop(self):
        h = self.heap_type([])
        x = h.pushpop(10)
        self.assertEqual((list(h), x), ([], 10))

        h = self.heap_type([10])
        x = h.pushpop(10.0)
        self.assertEqual((list(h), x), ([10], 10.0))
        self.assertEqual(type(h.peek()), int)
        self.assertEqual(type(x), float)

        h = self.heap_type([10])
        x = h.pushpop(9)
        self.assertEqual((list(h), x), ([10], 9))

        h = self.heap_type([10])
        x = h.pushpop(11)
        self.assertEqual((list(h), x), ([11], 10))

    def test_heapsort(self):
        # Exercise everything with repeated heapsort checks
        for trial in range(100):
            size = random.randrange(50)
            data = [random.randrange(25) for i in range(size)]
            if trial & 1:     # Half of the time, use heapify
                heap = self.heap_type(data[:])
            else:             # The rest of the time, use heappush
                heap = self.heap_type([])
                for item in data:
                    heap.push(item)
            heap_sorted = [heap.pop() for i in range(size)]
            self.assertEqual(heap_sorted, sorted(data))

    def test_comparison_operator(self):
        # Issue 3051: Make sure heapq works with both __lt__
        # For python 3.0, __le__ alone is not enough
        def hsort(data, comp):
            data = [comp(x) for x in data]
            heap = self.heap_type(data)
            return [heap.pop().x for i in range(len(data))]
        class LT:
            def __init__(self, x):
                self.x = x
            def __lt__(self, other):
                return self.x > other.x
        class LE:
            def __init__(self, x):
                self.x = x
            def __le__(self, other):
                return self.x >= other.x
        data = [random.random() for i in range(100)]
        target = sorted(data, reverse=True)
        self.assertEqual(hsort(data, LT), target)
        self.assertRaises(TypeError, data, LE)

    def test_roundtrip_repr(self):
        data = [5, 1, 4, 2, 3]
        heap = self.heap_type(data)
        representation = repr(heap)
        reconstructed = eval(representation)
        self.assertEqual(set(heap), set(reconstructed))
#==============================================================================

class LenOnly:
    "Dummy sequence class defining __len__ but not __getitem__."
    def __len__(self):
        return 10

class GetOnly:
    "Dummy sequence class defining __getitem__ but not __len__."
    def __getitem__(self, ndx):
        return 10

class CmpErr:
    "Dummy element that always raises an error during comparison"
    def __eq__(self, other):
        raise ZeroDivisionError
    __ne__ = __lt__ = __le__ = __gt__ = __ge__ = __eq__

def R(seqn):
    'Regular generator'
    for i in seqn:
        yield i

class G:
    'Sequence using __getitem__'
    def __init__(self, seqn):
        self.seqn = seqn
    def __getitem__(self, i):
        return self.seqn[i]

class I:
    'Sequence using iterator protocol'
    def __init__(self, seqn):
        self.seqn = seqn
        self.i = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self.i >= len(self.seqn): raise StopIteration
        v = self.seqn[self.i]
        self.i += 1
        return v

class Ig:
    'Sequence using iterator protocol defined with a generator'
    def __init__(self, seqn):
        self.seqn = seqn
        self.i = 0
    def __iter__(self):
        for val in self.seqn:
            yield val

class X:
    'Missing __getitem__ and __iter__'
    def __init__(self, seqn):
        self.seqn = seqn
        self.i = 0
    def __next__(self):
        if self.i >= len(self.seqn): raise StopIteration
        v = self.seqn[self.i]
        self.i += 1
        return v

class N:
    'Iterator missing __next__()'
    def __init__(self, seqn):
        self.seqn = seqn
        self.i = 0
    def __iter__(self):
        return self

class E:
    'Test propagation of exceptions'
    def __init__(self, seqn):
        self.seqn = seqn
        self.i = 0
    def __iter__(self):
        return self
    def __next__(self):
        3 // 0

class S:
    'Test immediate stop'
    def __init__(self, seqn):
        pass
    def __iter__(self):
        return self
    def __next__(self):
        raise StopIteration

from itertools import chain
def L(seqn):
    'Test multiple tiers of iterators'
    return chain(map(lambda x:x, R(Ig(G(seqn)))))


class SideEffectLT:
    def __init__(self, value, heap):
        self.value = value
        self.heap = heap

    def __lt__(self, other):
        self.heap[:] = []
        return self.value < other.value


class TestErrorHandling(TestCase):

    def setUp(self):
        self.heap_type = BikeHeap

    def test_non_sequence(self):
        self.assertRaises((TypeError, AttributeError), self.heap_type, 10)

    def test_len_only(self):
        self.assertRaises((TypeError, AttributeError), self.heap_type, LenOnly())

    def test_get_only(self):
        self.assertRaises(TypeError, self.heap_type, GetOnly())

    def test_cmp_error(self):
        seq = [CmpErr(), CmpErr(), CmpErr()]
        self.assertRaises(ZeroDivisionError, self.heap_type, seq)

    def test_arg_parsing(self):
        self.assertRaises((TypeError, AttributeError), self.heap_type, 10)

    # Issue #17278: the heap may change size while it's being walked.

    def test_heapinit_mutating_heap(self):
        heap_list = []
        heap_list.extend(SideEffectLT(i, heap_list) for i in range(200))
        # Python version raises IndexError, C version RuntimeError
        with self.assertRaises((IndexError, RuntimeError)):
            heap = self.heap_type(heap_list)

    def test_heappush_mutating_heap(self):
        heap_list = []
        heap = self.heap_type(heap_list)
        with self.assertRaises((IndexError, RuntimeError)):
            for problem in range(99):
                heap.push(SideEffectLT(problem, heap_list))


if __name__ == "__main__":
    unittest.main()
