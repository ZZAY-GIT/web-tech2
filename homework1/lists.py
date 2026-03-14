arr = []

n = int(input())

for _ in range(n):
    line = input().split()
    cmd = line[0]

    if cmd == "insert":
        i = int(line[1])
        e = int(line[2])
        arr.insert(i, e)

    elif cmd == "print":
        print(arr)

    elif cmd == "remove":
        e = int(line[1])
        arr.remove(e)

    elif cmd == "append":
        e = int(line[1])
        arr.append(e)

    elif cmd == "sort":
        arr.sort()

    elif cmd == "pop":
        if arr:
            arr.pop()

    elif cmd == "reverse":
        arr.reverse()