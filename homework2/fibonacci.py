cube = lambda x: x ** 3


def fibonacci(n):
    if n <= 0:
        return []
    if n == 1:
        return [0]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[-1] + fib[-2])
    
    return fib[:n]


if __name__ == '__main__':
    n = int(input())
    print(list(map(cube, fibonacci(n))))