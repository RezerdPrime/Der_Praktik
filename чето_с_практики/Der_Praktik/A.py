n = int(input())

Dict = [{} for i in range(n)]

for i in range(n):
    k = int(input())

    for j in range(k):
        s = input().split()
        Dict[i][s[0]] = int(s[1])

print("ДА" if all(
    any(i > 1 for i in Dict[j].values()) for j in range(n)
) else "НЕТ")