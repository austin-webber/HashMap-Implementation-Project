# Name: Austin Webber
# OSU Email: webberau@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 (Portfolio Assignment)
# Due Date: 6/5/22 (2 free days used)
# Description: Implementation of a HashMap by using a dynamic array as the
#              underlying storage. Chaining is implemented for collision
#              resolution using a singly linked list, with chains of key/value
#              pairs being stored in linked list nodes.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If the given key already
        exists in the hash map, its associated value must be replaced with the
        new value. If the given key is not in the hash map, a key/value pair
        is added.
        """
        # running key through hash function
        hash_index = self._hash_function(key) % self._capacity
        # getting linked list at index
        linked_list = self._buckets.get_at_index(hash_index)

        # iterate through sll at index
        for node in linked_list:
            # if given key already exists, update its value
            if node.key == key:
                node.value = value
                return
        # we've iterated through the linked list, if we haven't returned,
        # the key is not in the hash map
        linked_list.insert(key, value)
        self._size += 1
        return

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        count = 0

        for index in range(self._capacity):
            current_bucket = self._buckets.get_at_index(index)
            if current_bucket.length() == 0:
                count += 1

        return count

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        load_factor = self._size/self._capacity
        return load_factor

    def clear(self) -> None:
        """
        Clears the contents of the hash map.
        """
        new_da = DynamicArray()
        for bucket in range(self._capacity):
            new_da.append(LinkedList())
        self._buckets = new_da
        self._size = 0
        return

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All hash table links
        must be rehashed.
        """
        if new_capacity < 1:
            return

        keys_to_append = self.get_keys()
        values_to_append = DynamicArray()
        # generating an array of value pairs to put() in the hashmap later
        for index in range(keys_to_append.length()):
            current_key = keys_to_append.get_at_index(index)
            values_to_append.append(self.get(current_key))

        new_da = DynamicArray()
        # populate new da with empty sll's
        for i in range(new_capacity):
            new_da.append(LinkedList())

        self._buckets = new_da
        self._capacity = new_capacity
        self._size = 0

        # we grab the value to each key from the old array and call
        # put() to rehash the key/value pair into the resized hash map
        for index in range(keys_to_append.length()):
            self.put(keys_to_append.get_at_index(index), values_to_append.get_at_index(index))

        return

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. If the key is not in
        the hash map, returns None.
        """
        # running key through hash function
        hash_index = self._hash_function(key) % self._capacity
        # getting linked list at index
        linked_list = self._buckets.get_at_index(hash_index)

        # iterate through sll at index
        for node in linked_list:
            # if given key exists, return value
            if node.key == key:
                return node.value
        # at this point, we know the key is not in the hash map
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns: True - if the given key is in the hash map
                 False - Otherwise
        """
        if self._size == 0:
            return False

        # running key through hash function
        hash_index = self._hash_function(key) % self._capacity
        # getting linked list at index
        linked_list = self._buckets.get_at_index(hash_index)

        # iterate through sll at index
        for node in linked_list:
            # if given key already exists, update its value
            if node.key == key:
                return True
        # at this point, we know the key is not in the hash map
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        """
        # running key through hash function
        hash_index = self._hash_function(key) % self._capacity
        # getting linked list at index
        linked_list = self._buckets.get_at_index(hash_index)

        # sll remove() method returns True if node was found and removed.
        # returns False otherwise
        node_was_removed = linked_list.remove(key)

        if node_was_removed:
            self._size -= 1

        return

    def get_keys(self) -> DynamicArray:
        """
        Returns a DynamicArray that contains all the keys stored in the hash
        map. Order does not matter.
        """
        result_da = DynamicArray()
        for index in range(self._capacity):
            current_sll = self._buckets.get_at_index(index)
            for node in current_sll:
                result_da.append(node.key)

        return result_da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Receives a DynamicArray, returns a tuple containing, first, a DynamicArray
    comprising the mode value/s of the array, and second, an integer that
    represents the highest frequency.
    If there is more than one value with the highest frequency, all values at
    that frequency are included in the returned array.

    Utilizes 3 separate O(N) loops, making the whole function O(N) complexity.
    """
    map = HashMap(da.length() // 3, hash_function_1)

    # iterating through the da, using put() to hash the da element into the map
    # for loop is O(N) complexity
    for index in range(da.length()):
        # .get_at_index() is O(1)
        current_key = da.get_at_index(index)
        # .contains_key is amortized O(1)
        # if the key is already in the map, increment its value(frequency)
        if map.contains_key(current_key):
            # .get() is amortized O(1)
            current_value = map.get(current_key)
            # .put() is amortized O(1)
            map.put(current_key, current_value + 1)
        # if the key is not in the map, add it with a frequency of 1
        else:
            map.put(current_key, 1)

    max_freq = 0
    result_da = DynamicArray()

    # iterating through hash map, updating max_freq with the highest frequency.
    # again, for loop is O(N), get_at_index() and get() are both amortized O(1)
    for index in range(da.length()):
        current_key = da.get_at_index(index)
        current_value = map.get(current_key)
        if current_value > max_freq:
            max_freq = current_value

    # iterating through hash map again, comparing values to max_freq
    # this loop also O(N), all functions used inside are amortized O(1)
    for index in range(da.length()):
        current_key = da.get_at_index(index)
        current_value = map.get(current_key)
        if current_value == max_freq:
            result_da.append(current_key)
            # if we don't remove the key after appending it to the result_da,
            # we will run into it again later and append it a second time.
            map.remove(current_key)

    result = (result_da, max_freq)
    return result


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

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
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

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
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

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
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
