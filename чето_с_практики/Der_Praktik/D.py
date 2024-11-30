def ASCII(Str):
    Sum = 0
    for i in range(len(Str)):
        Sum += ord(Str[i]) - 64

    return Sum

s = " "
Dict = {}

while s:
    s = input()
    Dict[s] = ASCII(s.upper())

print(
    *dict(sorted(Dict.items(), key = lambda x: (x[1], x[0]))),
    sep = "\n"
)