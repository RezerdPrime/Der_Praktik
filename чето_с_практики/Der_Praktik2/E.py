class Queue:

    def __init__(self, *args):
        self.lst = [arg for arg in args]

    def __str__(self):
        return "{}".format(self.lst).replace(", ", " -> ")

    def is_empty(self):
        return len(self.lst) == 0

    def append(self, *args):
        self.lst += [arg for arg in args]

    def copy(self):
        nque = Queue(); nque.append(*self.lst)
        return nque

    def pop(self):

        if self.is_empty(): return None

        val = self.lst[0]
        self.lst.remove(val)
        return val

    def extend(self, que):
        self.lst += que.lst

    def next(self):
        if self.is_empty(): return Queue()
        return Queue(*self.lst[1:])

    def __next__(self):
        return self.next()

    def __add__(self, other):
        return Queue(*(self.lst + other.lst))

    def __iadd__(self, other):
        self.extend(other)
        return self

    def __eq__(self, other):
        return self.lst == other.lst

    def __ne__(self, other):
        return self.lst != other.lst

    def __rshift__(self, n):
        if len(self.lst) <= n: return Queue()
        return Queue(*self.lst[n:])

q1 = Queue(1, 2, 3)
print(q1)
q1.append(4, 5)
print(q1)
qx = q1.copy()
print(qx.pop())
print(qx)
q2 = q1.copy()
print(q2)
print(q1 == q2, id(q1) == id(q2))
q3 = q2.next()
print(q1, q2, q3, sep = "\n")
print(q1 + q3)
q3.extend(Queue(1, 2))
print(q3)
q4 = Queue(1, 2)
q4 += q3 >> 4
print(q4)
q5 = next(q4)
print(q4)
print(q5)