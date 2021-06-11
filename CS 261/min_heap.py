# Course: CS261 - Data Structures
# Assignment: 5
# Student: Alan Kuo
# Description: Implementation of MinHeap


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initializes a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.heap = DynamicArray()

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
        return 'HEAP ' + str(self.heap)

    def is_empty(self) -> bool:
        """
        Return True if no elements in the heap, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.heap.length() == 0

    def get_parent_index(self, node_index) -> int:
        """
        Helper function for finding the index for the parent node of a node.

        Args:
            node_index(int): The index of the given node

        Returns:
            int: The index for the parent node of the given node.
        """
        node_parent_index = (node_index - 1) // 2
        if node_parent_index < 0:
            node_parent_index = 0
        return node_parent_index

    def get_left_index(self, node_index) ->int:
        """
        Helper function for finding the index of the left child of a node.

        Args:
            node_index(int): The index of the given node

        Returns:
            int: The index for the left child of a given node
        """
        left_child_index = (2*node_index)+1
        return left_child_index

    def get_right_index(self, node_index):
        """Helper function for finding the index of the right child of a node

        Args:
            node_index(int): the index of the given node

        Returns:
            int: The index for the right child of a given node
        """
        right_child_index = (2*node_index) + 2
        return right_child_index

    def add(self, node: object) -> None:
        """
        Function that adds a new object to the MinHeap and maintains heap property.
        Runtime complexity is O(logN)

        Args:
            node(object): The new object to add to the MinHeap

        Returns:
            no returns
        """
        # If heap is empty, append to end
        if self.heap.length() == 0:
            self.heap.append(node)
            return
        # If heap is not empty, put element at end of array, compare node to parent. While node < parent, swap positions
        else:
            self.heap.append(node)
            node_index = self.heap.length()-1
            node_parent_index = self.get_parent_index(node_index)
            node_parent = self.heap.get_at_index(node_parent_index)
            while node_parent > node:
                # Swap nodes in underlying DA
                self.heap.swap(node_index, node_parent_index)
                # Updates index for node that is being inserted
                node_index = node_parent_index
                # Updating parent node and parent index
                node_parent_index = self.get_parent_index(node_index)
                node_parent = self.heap.get_at_index(node_parent_index)
        pass

    def get_min(self) -> object:
        """
        Function that returns an object with the minimum key and removes from the heap.

        Args:
            No arguments

        Returns:
            object: The object with the minimum key

        Raises:
            MinHeapException: Exception raised if heap is empty
        """
        if self.is_empty():
            raise MinHeapException
        else:
            return self.heap.get_at_index(0)

    def remove_min(self) -> object:
        """
        Function that returns an object with a minimum key and removes from the heap.

        Args:
            No arguments

        Returns:
            object: The object with a minimum key

        Raises:
            MinHeapException: Exception raised if heap is empty
        """
        # Checking if heap is empty
        if self.is_empty():
            raise MinHeapException
        else:
            # If heap only has one object, can simply pop off the object
            if self.heap.length() == 1:
                return self.heap.pop()
            else:
                # Swap value of first element with value of last element
                self.heap.swap(0, self.heap.length()-1)
                # Pop off value to be removed and save value to return later
                deleted_value = self.heap.pop()
                # Calls helper function to recreate heap structure
                self.trickle_down(0, self.heap.length())
                return deleted_value

    def trickle_down(self, start_index, length):
        """
        Helper function for recreating heap structure. Starts from top of heap and works downward by comparing start
        value to its children and swapping if necessary.

        Args:
            start_index(int): Index of the element to start with.
            length(int): The length of the heap DA, used to check whether an index is within current bounds

        Returns:
            no returns
        """
        # Getting values for node and its children
        start_node = self.heap.get_at_index(start_index)
        left_index = self.get_left_index(start_index)
        right_index = self.get_right_index(start_index)

        # Start by assuming that current node is the smallest
        curr_smallest = start_node
        # If left child is in bounds, check if it is smaller than the start node and replace as smallest if necessary
        if left_index < length and self.heap.get_at_index(left_index) < start_node:
            curr_smallest = self.heap.get_at_index(left_index)
            smallest_index = left_index

        # If right child is in bounds, check if it is smaller than the current smallest and replace if necessary
        if right_index < length and self.heap.get_at_index(right_index) < curr_smallest:
            curr_smallest = self.heap.get_at_index(right_index)
            smallest_index = right_index

        # If start node is not the current smallest, swap with the current smallest and repeat process.
        if curr_smallest != start_node:
            self.heap.swap(start_index, smallest_index)
            self.trickle_down(smallest_index, length)

    def build_heap(self, da: DynamicArray) -> None:
        """
        Receives a dynamic array with objects in any order and builds a proper MinHeap. Contents of current MinHeap
        are lost.

        Runtime complexity is O(N) by using trickle down vs using the add method. Implementation based on course
        materials and course reading (https://opendatastructures.org/ods-python/11_1_Comparison_Based_Sorti.html#sec:heapsort)

        Args:
            da(DynamicArray object): Dynamic array containing objects to build a proper MinHeap

        Returns:
            no returns
        """
        # Clearing current contents
        self.heap = DynamicArray()
        # Copying in new elements from given DA
        for i in range(da.length()):
            self.heap.append(da.get_at_index(i))
        # Getting index of last non-leaf element
        last_index = self.heap.length() - 1
        last_non_leaf = self.get_parent_index(last_index)
        # Calling trickle down on each element starting with first non-leaf
        for i in range(last_non_leaf, -1, -1):
            self.trickle_down(i, self.heap.length())
        pass


# BASIC TESTING
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


    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())


    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty():
        print(h, end=' ')
        print(h.remove_min())


    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)
    da.set_at_index(0, 500)
    print(da)
    print(h)
