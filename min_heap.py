# Name: Robert Smith
# OSU Email: Smithro8@oregonstate.edu
# Course:       CS261 - Data Structures
# Assignment: 5
# Due Date: 03/05/2023
# Description: Creates a min heap class using a dynamic array. Has various methods to add,
#              remove, sort the heap etc.

from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._heap = DynamicArray()
        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return 'HEAP ' + str(heap_data)
# ---------------------------------------------------------------------------

    def add(self, node: object) -> None:
        """
        Adds a node object to the heap
        """
        # sets index and parent index
        child = self._heap.length()
        parent = (child-1)//2
        if self._heap.is_empty():
            self._heap.append(node)
        else:
            # uses append to add at the end of DA
            self._heap.append(node)
            # percolates up to root node
            while parent > - 1:
                if self._heap[child] >= self._heap[parent]:
                    return
                if self._heap[child] < self._heap[parent]:
                    # saves values
                    parent_value = self._heap[parent]
                    child_value = self._heap[child]
                    # swaps values
                    self._heap[parent] = child_value
                    self._heap[child] = parent_value
                    # moves nodes up the heap
                    child = parent
                    parent = (parent - 1) // 2
        return

    def is_empty(self) -> bool:
        """
        Returns true if empty
        Else false
        """
        if self._heap.is_empty():
            return True
        else:
            return False

    def get_min(self) -> object:
        """
        Gets the min mode (top node)
        Exception if empty
        """
        # if empty
        if self._heap.is_empty():
            raise MinHeapException
        else:
            return self._heap[0]

    def remove_min(self) -> object:
        """
        Removes the min node (top)
        Exception if empty
        """
        # if empty
        if self._heap.is_empty():
            raise MinHeapException
        last_node = self._heap[self._heap.length() - 1]
        removed_node = self._heap[0]
        self._heap[0] = last_node
        self._heap.remove_at_index(self._heap.length() - 1)
        _percolate_down(self._heap, 0)
        return removed_node

    def build_heap(self, da: DynamicArray) -> None:
        """
        Builds a heap out of a passed array
        """
        self._heap = DynamicArray(da)
        last_index = self._heap.length() - 1
        # gets last parent index
        index = (last_index-1) // 2

        while index > -1:
            _percolate_down(self._heap, index)
            index -= 1

    def size(self) -> int:
        """
        Returns the size od the heap
        """
        return self._heap.length()

    def clear(self) -> None:
        """
        Clears the heap
        """
        self._heap = DynamicArray()


def heapsort(da: DynamicArray) -> None:
    """
    Receives an array, builds a heap in place
    Sorts the heap
    """

    last_index = da.length() - 1
    # gets last parent index
    index = (last_index - 1) // 2
    # builds valid heap
    while index > -1:
        _percolate_down(da, index)
        index -= 1
    # trades min with last val
    while last_index != 0:
        min = da[0]
        temp = da[last_index]
        # makes valid swap for last two nodes
        if last_index == 1:
            if min > temp:
                da[0] = min
            else:
                da[0] = temp
                da[last_index] = min
        # swaps nodes
        else:
            da[0] = temp
            da[last_index] = min

        parent = 0
        left = 1
        right = 2
        index_bounds = left + right
        # percolate down to last index
        while index_bounds < last_index * 2 - 1:
            # sets lowest val to child
            if da[left] <= da[right]:
                child = left
            else:
                child = right
            # stop if child >= parent
            if da[child] >= da[parent]:
                index_bounds = last_index * 2
            # swaps child and parent
            else:
                # saves values
                parent_value = da[parent]
                child_value = da[child]
                # swaps values
                da[parent] = child_value
                da[child] = parent_value
                # moves nodes down the heap
                parent = child
                left = parent * 2 + 1
                right = parent * 2 + 2
                # keeps saved vals safe
                index_bounds = left + right
        last_index -= 1


def _percolate_down(da: DynamicArray, parent: int) -> None:
    """
    percolates down the heap
    """
    left = parent * 2 + 1
    right = parent * 2 + 2
    # has no children
    if da.length() <= 1:
        return
    # if only has left child
    if da.length() == 2:
        child_index = left
    elif right >= da.length():
        child_index = left
        # picks smallest child
    elif da[left] <= da[right]:
        child_index = left
    else:
        child_index = right

    while da[parent] > da[child_index]:
        # saves values
        parent_value = da[parent]
        child_value = da[child_index]
        # swaps values
        da[parent] = child_value
        da[child_index] = parent_value
        # moves nodes down the heap
        parent = child_index
        left = parent * 2 + 1
        right = parent * 2 + 2
        # if no children
        if left >= da.length():
            return
        # if one child(left)
        if right >= da.length():
            child_index = left
        # if two children
        elif da[left] <= da[right]:
            child_index = left
        else:
            child_index = right


# ------------------- BASIC TESTING -----------------------------------------
if __name__ == '__main__':
    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)
    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)
    print("\nPDF - is_empty example 1")
    print("-------------------")
    h = MinHeap([2, 4, 12, 56, 8, 34, 67])
    print(h.is_empty())
    print("\nPDF - is_empty example 2")
    print("-------------------")
    h = MinHeap()
    print(h.is_empty())
    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())
    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([8, 9, 10])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())
    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([28671, -6005, 96598, -69130])
    h = MinHeap([28671])
    print(h)
    h.build_heap(da)
    print(h)
    print("--------------------------")
    print("Inserting 500 into input DA:")
    da[0] = 500
    print(da)
    print("Your MinHeap:")
    print(h)
    if h.get_min() == 500:
        print("Error: input array and heap's underlying DA reference same object in memory")
    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([-31843, 71540, -90778, 15048, -24440, -41354, 81415, -12257, 61379])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")
    print("right answer-> [57859, -15449, -20793, -51444, -51444, -59389, -69800, -70567, -82759]")
    print("\nPDF - heapsort example 2")
    # print("------------------------")
    # da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    # print(f"Before: {da}")
    # heapsort(da)
    # print(f"After:  {da}")
    # print("\nPDF - size example 1")
    # print("--------------------")
    # h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    # print(h.size())
    # print("\nPDF - size example 2")
    # print("--------------------")
    # h = MinHeap([])
    # print(h.size())
    # print("\nPDF - clear example 1")
    # print("---------------------")
    # h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    # print(h)
    # print(h.clear())
    # print(h)
