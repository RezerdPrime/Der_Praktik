n = int(input())
List = []

for i in range(n):
    List.append(input().split())

for i in range(int(input())):
    Str = input()
    print( *(j[0] for j in List if Str in j) )