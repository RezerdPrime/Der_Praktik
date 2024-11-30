import sys

Str = " "
text = {}
while Str != "\n":
    Str = sys.stdin.readline()

    for s in Str.split():
        if s not in text.keys():
            text[s] = 1
        else: text[s] += 1

print(
    *dict(sorted(text.items(), key = lambda x: (-x[1], x[0]))),
    sep = "\n"
)