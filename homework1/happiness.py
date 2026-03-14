n, m = map(int, input().split())
arr = list(map(int, input().split()))

A = set(map(int, input().split()))
B = set(map(int, input().split()))

mood = 0

for x in arr:
    if x in A:
        mood += 1
    elif x in B:
        mood -= 1

print(mood)