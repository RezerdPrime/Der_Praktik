class Summator:

    def __init__(self, N):
        self.N = N

    def transform(self, n):
        return n

    def sum(self, n):
        return sum([self.transform(i) for i in range(1, n + 1)])

class CQ_Summator(Summator):

    def __init__(self, N):
        super().__init__(N)

    def transform(self, n):
        return n ** 2

class CB_Summator(Summator):

    def __init__(self, N):
        super().__init__(N)

    def transform(self, n):
        return n ** 3

val = 5
s1 = Summator(val)
s2 = CQ_Summator(val)
s3 = CB_Summator(val)

print(s1.sum(s1.N),
      s2.sum(s2.N),
      s3.sum(s3.N))