# Name: Austin Webber
# OSU Email: webberau@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 (Portfolio Assignment)
# Due Date: 6/5/22 (2 free days used)
# Description: Implementation of a HashMap by using a dynamic array as the
#              underlying storage. Open Addressing with Quadratic Probing is
#              implemented for collision resolution with key/value pairs being
#              stored in the array as hash entries.


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

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
        exists in the hash map, its associated value must be replaced with
        the new value. If the given key is not in the hash map, a key/value
        pair must be added.
        If this method is called and the current load factor of the table is
        greater than or equal to 0.5, the table must be resized to double its
        current capacity.
        """
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # running key through hash function
        i_initial = self._hash_function(key) % self._capacity
        # getting hash_entry at index
        hash_entry = self._buckets.get_at_index(i_initial)

        # if empty at i_initial, insert element and stop
        if hash_entry is None:
            new_hash_entry = HashEntry(key, value)
            self._buckets.set_at_index(i_initial, new_hash_entry)
            self._size += 1
            return

        # otherwise, start search for empty position by computing next index
        # in the probing sequence
        j = 1
        while hash_entry is not None:
            # first check if current hash entry has the same key
            if hash_entry.key == key:
                # if hash_entry is a tombstone, set it to False before updating
                if hash_entry.is_tombstone:
                    hash_entry.is_tombstone = False
                    self._size += 1
                # update its value and stop
                hash_entry.value = value
                return
            # otherwise, proceed with quadratic probing scheme
            new_index = (i_initial + (j * j)) % self._capacity
            j += 1
            hash_entry = self._buckets.get_at_index(new_index)

        # at this point, we've arrived at an empty position
        new_hash_entry = HashEntry(key, value)
        self._buckets.set_at_index(new_index, new_hash_entry)
        self._size += 1
        return

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        load_factor = self._size/self._capacity
        return load_factor

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        count = 0

        for index in range(self._capacity):
            current_hash_entry = self._buckets.get_at_index(index)
            if current_hash_entry is None:
                count += 1

        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing key/value
        remain in the new hash map, and all hash table links are rehashed.
        """
        # remember to rehash non-deleted entries into new table
        # method does nothing in these cases
        if new_capacity < 1 or new_capacity < self._size:
            return

        # get_keys() only returns non-tombstone hash entries
        keys_to_append = self.get_keys()
        values_to_append = DynamicArray()
        # generating an array of value pairs to put() in the hashmap later
        for index in range(keys_to_append.length()):
            current_key = keys_to_append.get_at_index(index)
            values_to_append.append(self.get(current_key))

        new_da = DynamicArray()
        # initialize new da with None objects
        for i in range(new_capacity):
            new_da.append(None)

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
        i_initial = self._hash_function(key) % self._capacity
        # getting hash_entry at index
        hash_entry = self._buckets.get_at_index(i_initial)

        # if empty at i_initial, key is not in hash map, return None
        if hash_entry is None:
            return None

        # otherwise, start search for given key by computing next index
        # in the probing sequence
        j = 1
        while hash_entry is not None:
            # first check if current hash entry has the same key
            if hash_entry.key == key:
                # if hash_entry is not a tombstone, return value
                if not hash_entry.is_tombstone:
                    return hash_entry.value

            # otherwise, proceed with quadratic probing scheme
            new_index = (i_initial + (j * j)) % self._capacity
            j += 1
            hash_entry = self._buckets.get_at_index(new_index)

        # at this point, key is not in the hash map
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns: True - if the given key is in the hash map
                 False - Otherwise
        """
        if self._size == 0:
            return False

        # running key through hash function
        i_initial = self._hash_function(key) % self._capacity
        # getting hash_entry at index
        hash_entry = self._buckets.get_at_index(i_initial)

        # if empty at i_initial, key is not in hash map, return False
        if hash_entry is None:
            return False

        # otherwise, start search for given key by computing next index
        # in the probing sequence
        j = 1
        while hash_entry is not None:
            # first check if current hash entry has the same key
            if hash_entry.key == key:
                # if hash_entry is not a tombstone, return True
                if not hash_entry.is_tombstone:
                    return True

            # otherwise, proceed with quadratic probing scheme
            new_index = (i_initial + (j * j)) % self._capacity
            j += 1
            hash_entry = self._buckets.get_at_index(new_index)

        # at this point, key is not in the hash map
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        If the key is not in the hash map, nothing happens.
        """
        # running key through hash function
        i_initial = self._hash_function(key) % self._capacity
        # getting hash_entry at index
        hash_entry = self._buckets.get_at_index(i_initial)

        # if empty at i_initial, key is not in hash map, nothing happens
        if hash_entry is None:
            return

        # otherwise, start search for given key by computing next index
        # in the probing sequence
        j = 1
        while hash_entry is not None:
            # first check if current hash entry has the same key
            if hash_entry.key == key:
                # check to see if tombstone, if so, nothing happens
                if hash_entry.is_tombstone:
                    return
                else:
                    # remove the entry by updating the tombstone to True
                    hash_entry.is_tombstone = True
                    # decrement size
                    self._size -= 1
                    return
            # otherwise, proceed with quadratic probing scheme
            new_index = (i_initial + (j * j)) % self._capacity
            j += 1
            hash_entry = self._buckets.get_at_index(new_index)

        # at this point, we've arrived at an empty position. We know the key
        # is not in the hash map
        return

    def clear(self) -> None:
        """
        Clears the contents of the hash map.
        """
        new_da = DynamicArray()
        for bucket in range(self._capacity):
            new_da.append(None)
        self._buckets = new_da
        self._size = 0
        return

    def get_keys(self) -> DynamicArray:
        """
        Returns a DynamicArray that contains all the keys stored in the hash
        map. Order does not matter.
        """
        result_da = DynamicArray()
        for index in range(self._capacity):
            current_hash_entry = self._buckets.get_at_index(index)
            if current_hash_entry is not None:
                # only add key to result_da if not a tombstone
                if not current_hash_entry.is_tombstone:
                    current_key = current_hash_entry.key
                    result_da.append(current_key)

        return result_da


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

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

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
