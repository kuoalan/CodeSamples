# Course: CS261 - Data Structures
# Assignment: 5
# Student: Alan Kuo
# Description: Implementation of Hash Map


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def get_hash_index(self, key) -> int:
        """Helper function for finding hash index for a given key.

        Args:
            key(str): The key to find the hash index for

        Returns:
            int: The hash index for a given key.
        """
        return self.hash_function(key) % self.capacity

    def clear(self) -> None:
        """
        Function that clears the content of the hash map without changing underlying capacity.

        Args:
            No arguments

        Returns:
            No returns
        """
        # Clears chains in buckets
        for i in range(self.capacity):
            cur_list = self.buckets.get_at_index(i)
            if cur_list.head is not None:
                cur_list.head = None
        # Resets size to 0
        self.size = 0
        pass

    def get(self, key: str) -> object:
        """
        Function that returns the value associated with a given key. If key is not in the hash map, returns None.

        Args:
            key(str): The key to get the value for

        Returns:
            object: The value associated with the key (if it exists). None otherwise.
        """
        # Finds chain matching hash index, iterates through node to find matching key
        hash_index = self.get_hash_index(key)
        chain = self.buckets.get_at_index(hash_index)
        for node in chain:
            if node.key == key:
                return node.value
        return None

    def put(self, key: str, value: object) -> None:
        """
        Function that updates a key/value pair in the hash map. If key already exists, associated value
        should be replaced. If key does not exist, key/value pair will be added to hash map.

        Args:
            key(str): The key of the key/value pair to update/add
            value(object): The value of the key/value pair to update/add

        Return:
            No returns
        """
        hash_index = self.get_hash_index(key)
        chain = self.buckets.get_at_index(hash_index)
        # Iterates through nodes in chain. If matching key is found, replaces value and exits loop
        for node in chain:
            if node.key == key:
                node.value = value
                return
        # Otherwise, inserts value into chain
        chain.insert(key, value)
        self.size += 1
        return

    def remove(self, key: str) -> None:
        """
        Function that removes the given key and associated value from the hash map. If key is not in the hash map,
        does nothing.

        Args:
            key(str): The key to remove from the hash map

        Returns:
            No returns
        """
        # Searches for chain matching hash index and removes node
        hash_index = self.get_hash_index(key)
        chain = self.buckets.get_at_index(hash_index)
        removed = chain.remove(key)
        if removed:
            self.size -= 1
        pass

    def contains_key(self, key: str) -> bool:
        """
        Function that returns True if a given key is in the hash map, otherwise False.

        Args:
            key(str): The key to search for in the hash map

        Returns:
            bool: True if key is in the hash map, otherwise False
        """
        # Empty hash map does not contain any keys
        if self.size == 0:
            return False
        # Checks each chain for node with matching key
        else:
            hash_index = self.get_hash_index(key)
            chain = self.buckets.get_at_index(hash_index)
            if chain.contains(key):
                return True
            return False

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.

        Args:
            No arguments

        Returns:
            int: the number of empty buckets in the hash table
        """
        num_empty_buckets = 0
        # Checks for empty chains
        for i in range(self.capacity):
            if self.buckets.get_at_index(i).head is None:
                num_empty_buckets += 1
        return num_empty_buckets

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.

        Args:
            no arguments

        Returns:
            float: the current hash table load factor
        """
        return self.size/self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing key/value pairs should remain in the new
        hash map and all links should be rehashed. If new_capacity is less than 1, function does nothing.
        """
        # Checks if new hash table capacity is greater than 1
        if new_capacity < 1:
            return
        # Create new set of buckets
        new_buckets = DynamicArray()
        new_size = 0
        # Appends chains to new set of buckets
        for _ in range(new_capacity):
            new_buckets.append(LinkedList())
        # Iterates through all chains in current buckets
        for i in range(self.capacity):
            cur_chain = self.buckets.get_at_index(i)
            # Iterates through nodes in each chain and rehashes with new capacity
            for node in cur_chain:
                hash_index = self.hash_function(node.key) % new_capacity
                insert_chain = new_buckets.get_at_index(hash_index)
                # Inserts key/value pair. Should be no duplicate keys because all keys in existing hash map
                # should be unique.
                insert_chain.insert(node.key, node.value)
                new_size += 1

        self.buckets = new_buckets
        self.capacity = new_capacity
        self.size = new_size
        pass

    def get_keys(self) -> DynamicArray:
        """
        Returns a DynamicArray containing all keys stored in hash map.

        Args:
            No arguments

        Returns:
            DynamicArray object: contains all keys stored in hash map
        """
        # Creates new DynamicArray
        keys_list = DynamicArray()
        # Iterates through each node in each chain and adds keys to array
        for i in range(self.capacity):
            cur_list = self.buckets.get_at_index(i)
            for node in cur_list:
                keys_list.append(node.key)
        return keys_list


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())


    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))


    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)


    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))


    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')


    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())


print(hash_function_1("dad"))
print(hash_function_1("add"))
print(hash_function_2("dad"))
print(hash_function_2("add"))