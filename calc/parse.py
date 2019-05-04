from .stack import Stack
from .array import Array


class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data


class InvalidCalcString(Exception):
    pass


class InvalidDivisor(Exception):
    pass


class CalcTree:

    def __init__(self):
        self.Operators = {'+': 1, '-': 1, '*': 2, '/': 2}
        self.Numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']
        self._head = None

    def _parse_string(self, s):
        """ parse given string to an array """
        s_size = len(s)

        arr_tmp = Array()
        num_tmp = Array()
        previous_char = None
        i = 0
        while i < s_size:
            c = s[i]
            if i > 0:
                previous_char = s[i-1]
            if c in self.Numbers or (c == '-' and previous_char not in self.Numbers):
                # numbers or negative sign ('-')
                num_tmp.add(c)
            elif c in self.Operators:
                if num_tmp.length() > 0:
                    arr_tmp.add(num_tmp.to_string())
                    num_tmp.clear()
                arr_tmp.add(c)
            elif c == '(':
                arr_tmp.add(c)
            elif c == ')':
                if num_tmp.length() > 0:
                    arr_tmp.add(num_tmp.to_string())
                    num_tmp.clear()
                arr_tmp.add(c)
            i += 1

        if num_tmp.length() > 0:
            arr_tmp.add(num_tmp.to_string())

        return arr_tmp.array()

    def _parse_array(self, arr):
        """ parse given array to a tree """
        cur_ope = None
        cur_ope_node = None
        cur_num_node = None
        head = None

        arr_size = len(arr)
        i = 0
        while i < arr_size:
            t = arr[i]
            if t in self.Operators:
                n = Node(t)
                if cur_ope is None:
                    n.left = cur_num_node
                    head = n
                else:
                    # compare the priorities of current operator and previous one
                    if self.Operators[t] >= self.Operators[cur_ope]:
                        # be the right child of current node
                        n.left = cur_num_node
                        cur_ope_node.right = n
                    else:
                        # be the top ancestor of current node
                        cur_ope_node.right = cur_num_node
                        n.left = head
                        head = n
                cur_ope = t
                cur_ope_node = n
                cur_num_node = None
            elif t == '(':
                parenthesis_counter = 1
                j = i + 1
                while True:
                    t2 = arr[j]
                    if t2 == '(':
                        parenthesis_counter += 1
                    elif t2 == ')':
                        parenthesis_counter -= 1
                        if parenthesis_counter == 0:
                            cur_num_node = self._parse_array(arr[(i+1):j])
                            break
                    j += 1
                i = j
            else:
                cur_num_node = Node(self._to_number(t))
            i += 1
        if cur_num_node is not None:
            cur_ope_node.right = cur_num_node
        return head

    def print(self):
        a = []
        self._print(a, self._head)
        print(','.join(a))

    def _print(self, arr, node):
        if node.left:
            self._print(arr, node.left)
        # arr.append(str(node.data))
        if node.right:
            self._print(arr, node.right)
        arr.append(str(node.data))

    def traverse_post_order(self):
        result = Array()
        stack = Stack()
        node = self._head
        last = None
        while node or not stack.empty():
            while node is not None:
                stack.push(node)
                node = node.left
            node = stack.peek()
            if not node.right or node.right == last:
                result.add(node.data)
                last = node
                stack.pop()
                node = None
            else:
                node = node.right
        return result.array()

    def calculate(self, input_str):
        if not input_str or len(input_str) == 0:
            raise InvalidCalcString

        a = self._parse_string(input_str)
        if len(a) < 3:
            raise InvalidCalcString

        self._head = self._parse_array(a)

        a = self.traverse_post_order()
        s = Stack()
        i = 0
        while i < len(a):
            t = a[i]
            if t in self.Operators:
                operand2 = s.pop()
                operand1 = s.pop()
                x = self._calculate(operand1, operand2, t)
                s.push(x)
            else:
                s.push(t)
            i += 1
        return s.pop()

    @staticmethod
    def _to_number(s):
        if '.' in s:
            return float(s)
        return int(s)

    @staticmethod
    def _calculate(operand1, operand2, operator):
        # a1 = float(operand1)
        # a2 = float(operand2)
        a1 = operand1
        a2 = operand2
        if operator == '+':
            return a1 + a2
        elif operator == '-':
            return a1 - a2
        elif operator == '*':
            return a1 * a2
        elif operator == '/':
            if a2 == 0:
                raise InvalidDivisor
            return a1 / a2
        return None
