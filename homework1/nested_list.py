n = int(input())
students = [[input().strip(), float(input())] for _ in range(n)]

second_score = sorted({s[1] for s in students})[1]

for name in sorted(name for name, score in students if score == second_score):
    print(name)