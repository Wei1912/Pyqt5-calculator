class Stack:
    _stack_default_size = 16
    _stack_size = 0
    _cursor = 0
    _arr = None

    def __init__(self):
        self._arr = [None] * self._stack_default_size
        self._stack_size = self._stack_default_size

    def push(self, element):
        if self._cursor == self._stack_size:
            # stack is full, need to extend
            _arr2 = [None] * (self._stack_size * 2)
            i = 0
            while i < self._stack_size:
                _arr2[i] = self._arr[i]
                i += 1
            self._arr = _arr2
            self._stack_size *= 2

        self._arr[self._cursor] = element
        self._cursor += 1

    def pop(self):
        if self.empty():
            raise Exception('stack is empty.')
        self._cursor -= 1
        return self._arr[self._cursor]

    def peek(self):
        if self.empty():
            raise Exception('stack is empty.')
        return self._arr[self._cursor - 1]

    def empty(self):
        return self._cursor == 0

    def clear(self):
        self._cursor = 0
