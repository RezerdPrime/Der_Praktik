class Balance:

    def __init__(self, left = 0, right = 0):
        self.left = left
        self.right = right

    def add_left(self, val): self.left += val

    def add_right(self, val): self.right += val

    def result(self):
        if self.left == self.right: return "="
        if self.left < self.right: return "R"
        return "L"

balance = Balance()
balance.add_right(10)
balance.add_left(5)
balance.add_left(5)
print(balance.result())
balance.add_left(1)
print(balance.result())