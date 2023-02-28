# Name: Robert Smith
# OSU Email: Smithro8@oregonstate.edu
# Course:       CS261 - Data Structures
# Assignment: 3
# Due Date: 02/13/2023
# Description: A dynamic array data structure that has a lot of methods to act similar to
#              python list and features associated with python lists.

from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.data = None
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)
        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration
        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Changes the capacity of the dynamic array
        It doesn't change value or order of objects
        It only accepts positive numbers bigger than the size of array
        """

        if new_capacity <= 0 or new_capacity < self.length():
            return
        else:
            # sets capacity and keeps old list
            self._capacity = new_capacity
            temp_arr = self._data
            self._data = StaticArray(self._capacity)
            for item in range(self.length()):
                self._data[item] = temp_arr.get(item)

    def append(self, value: object) -> None:
        """
        Adds value to the end of the array
        Doubles capacity when full
        """
        # if there is no room in da
        if self._data.get(self._data.length() - 1) is not None:
            new_capacity = self._capacity * 2
            self.resize(new_capacity)

        # if there is room in da
        if self._data.get(self._data.length() - 1) is None:
            self._data[self._size] = value
            self._size = self._size + 1

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Adds new value at specific index
        Doubles capacity when full
        """

        if index < 0 or index > self.length():
            raise DynamicArrayException
        if self._data[0] is None:
            self.append(value)
            return

        # appends val then shifts to index
        self.append(value)
        da_index = self._data.length() - 1
        while da_index != index:
            if self._data[da_index] is not None:
                self._data[da_index], self._data[da_index - 1] = self._data[da_index - 1], self._data[da_index]
                da_index -= 1
            if self._data[da_index] is None:
                da_index -= 1

    def remove_at_index(self, index: int) -> None:
        """
        Removes value at specific index
        Reduces capacity if less than 1/4 space being used
        Will not reduce below 10
        """
        # invalid index
        if index < 0 or index > self.length():
            raise DynamicArrayException

        # empty array
        if self._size == 0:
            raise DynamicArrayException

        # resize to 10
        if self.length() * 2 < 10 and self.get_capacity() > 10:
            if self.length() / self.get_capacity() < 0.25:
                self.resize(10)

        # resize to twice the size of length
        if self.length() * 2 > 10:
            if self.length() / self.get_capacity() < 0.25:
                new_capacity = self.length() * 2
                self.resize(new_capacity)

        da_index = index
        # if last index
        if self._size - 1 == index:
            self._size -= 1
            return

        # shifts vals to the right takes off end
        while da_index != self._size - 1:
            self.set_at_index(da_index, self.get_at_index(da_index + 1))
            da_index += 1
            if da_index == self._data.length() - 1:
                self.set_at_index(da_index, None)
        self._size -= 1

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Returns a new array that contains a 'slice' of the original array
        """

        new_arr = DynamicArray()
        # invalid index
        if start_index < 0 or start_index >= self.length():
            raise DynamicArrayException

        # negative size
        if size < 0:
            raise DynamicArrayException

        # not enough indices
        if start_index + size > self.length():
            raise DynamicArrayException

        if size == 0:
            return new_arr

        index = start_index
        stop_index = start_index + size
        # appends values to new arr
        while index != stop_index:
            value = self.get_at_index(index)
            new_arr.append(value)
            index += 1
        return new_arr

    def merge(self, second_da: "DynamicArray") -> None:
        """
        Merges two arrays into one array
        """

        index = 0
        while index != second_da.length():
            self.append(second_da.get_at_index(index))
            index += 1

    def map(self, map_func) -> "DynamicArray":
        """
        Returns new array with values of the function passed
        """
        new_arr = DynamicArray()
        index = 0
        # gets val, applies func, appends
        while index != self.length():
            value = self.get_at_index(index)
            mapped_val = map_func(value)
            new_arr.append(mapped_val)
            index += 1
        return new_arr

    def filter(self, filter_func) -> "DynamicArray":
        """
        Returns a filtered new array
        Values are filtered by a passed function
        """

        new_arr = DynamicArray()
        index = 0
        # gets value, changes val to T or F, appends if true
        while index != self.length():
            value = self.get_at_index(index)
            filtered_val = filter_func(value)
            if filtered_val is True:
                new_arr.append(self.get_at_index(index))
            index += 1
        return new_arr

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Returns a reduced object
        The object value is derived from a passed function
        """
        # if no items
        if self.length() == 0:
            return initializer

        # sets initializer if not passed
        if initializer is None:
            initializer = self.get_at_index(0)
            index = 1
        else:
            index = 0

        # gets value, reduces and adjusts initializer
        while index != self.length():
            value = self.get_at_index(index)
            reduced_val = reduce_func(initializer, value)
            initializer = reduced_val
            index += 1
        return initializer


def find_mode(arr: DynamicArray) -> (DynamicArray, int):
    """
    Returns a new array with the most occurring objects
    Also returns frequency of objects
    Array must be ordered
    """

    new_arr = DynamicArray()
    # if arr is one item
    if arr.length() == 1:
        new_arr.append(arr[0])
        return new_arr, 1

    # loop counts the highest frequency
    max_index = arr.length() - 1
    index = 0
    counter = 1
    frequency = 0
    while index != max_index:
        if arr[index] == arr[index + 1]:
            counter += 1
        # if occurrence ends, reset counter
        if arr[index] != arr[index + 1]:
            counter = 1
        # sets the highest frequency
        if counter >= frequency:
            frequency = counter
        index += 1

    # if one occurrence of items
    if frequency == 1:
        for item in arr:
            new_arr.append(item)
        return new_arr, frequency

    # appends highest frequency numbers
    counter = 1
    max_index = arr.length() - 1
    index = 0
    while index != max_index:
        if arr[index] == arr[index + 1]:
            counter += 1
        # if occurrence end reset values
        if arr[index] != arr[index + 1]:
            counter = 1
        if counter == frequency:
            new_arr.append(arr[index])
        index += 1
    return new_arr, frequency