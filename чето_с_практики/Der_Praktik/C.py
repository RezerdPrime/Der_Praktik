condition = lambda x: x % 9 == 0
pow2 = lambda x: x**2
print(sum(map(pow2, filter(condition, [i for i in range(10, 100)]))))