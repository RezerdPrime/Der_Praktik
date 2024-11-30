class Polynomial:

    def __init__(self, lst : list):
        self.lst = lst

    def __call__(self, x):
        res = self.lst[0]

        for i in range(1, len(self.lst)):
            res += self.lst[i] * x ** i

        return res

    def __add__(self, other):
        nlist = [0 for _ in range(max(len(self.lst), len(other.lst)))]

        for i in range(len(self.lst)):
            nlist[i] += self.lst[i]

        for i in range(len(other.lst)):
            nlist[i] += other.lst[i]

        return Polynomial(nlist)

poly1 = Polynomial([0, 1])
poly2 = Polynomial([10])
poly3 = poly1 + poly2
poly4 = poly2 + poly1
print(poly3(-2), poly4(-2))
print(poly3(-1), poly4(-1))
print(poly3(0), poly4(0))
print(poly3(1), poly4(1))
print(poly3(2), poly4(2))