n = int(input())

intervals = []
for _ in range(n):
    a, b = map(int, input().split())
    intervals.append((a, b))

t = int(input())

count = 0
for start, end in intervals:
    if start <= t <= end:
        count += 1

print(count)