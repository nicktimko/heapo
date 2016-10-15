'''
>>> heap = BikeHeap([4, 2, 1, 3])
>>> heap.pop()
1
>>> heap.pop()
2
'''

import heapq


class BikeHeap(object):
    def __init__(self, heap):
        self.heap = heap
        heapq.heapify(self.heap)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.heap)

    def __len__(self):
        return len(self.heap)

    def __iter__(self):
        return iter(self.heap)

    def __getitem__(self, index):
        return self.heap[index]

    def pop(self):
        return heapq.heappop(self.heap)

    def push(self, item):
        heapq.heappush(self.heap, item)

    def peek(self):
        return self.heap[0]

    def pushpop(self, item):
        return heapq.heappushpop(self.heap, item)

    def replace(self, item):
        return heapq.heapreplace(self.heap, item)


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
