from math import log2

def is_prime(x):
    for i in range(2, int(x ** 0.5) + 1):
        if x % i == 0: return False
    return True

def check_pin(Str):
    flags = [False, False, False]
    lst = Str.split("-")

    if lst[1] == lst[1][::-1]: flags[1] = True

    log = log2(int(lst[2]))
    if log - int(log) == 0: flags[2] = True

    if is_prime(int(lst[0])): flags[0] = True

    if all(flags): return "Корректен"
    else: return "Некорректен"

s = input()
print(check_pin(s))
