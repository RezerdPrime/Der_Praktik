def my_map(func, vals):
    return [func(i) for i in vals]

def functeon(x):
    return x ** x

print(my_map(functeon, [i for i in range(10)]))