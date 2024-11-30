import sys
from collections import defaultdict as dd

data = sys.stdin.readline()
Dict = dd(lambda: dd(int))

while data != "\n":
    chel, item, count = data.split()
    Dict[chel][item] += int(count)
    data = sys.stdin.readline()

for chel in Dict: Dict[chel] = dict(sorted(Dict[chel].items()))

Dict = dict(sorted(Dict.items()))

for chel in Dict:
    print(chel + ":")

    for item in Dict[chel]:
        print(item, Dict[chel][item])