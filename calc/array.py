class Array:
    _init_size = 32
    _size = 0
    _len = 0
    _arr = None

    def __init__(self):
        self._arr = [None] * self._init_size
        self._size = self._init_size

    def add(self, element):
        if self._len == self._size:
            # extend
            _arr2 = [None] * (self._size * 2)
            i = 0
            while i < self._size:
                _arr2[i] = self._arr[i]
                i += 1
            self._arr = _arr2
            self._size *= 2

        self._arr[self._len] = element
        self._len += 1

    def get(self, index):
        if index < 0 or index >= self._len:
            raise Exception('Out of range: ' + str(index))
        return self._arr(index)

    def set(self, index, value):
        if index < 0 or index >= self._len:
            raise Exception('Out of range: ' + str(index))
        self._arr[index] = value

    def clear(self):
        for i in range(self._len):
            self._arr[i] = None
        self._len = 0

    def length(self):
        return self._len

    def array(self):
        return self._arr[:self._len]

    def to_string(self):
        return ''.join(self.array())
