def fact_rec(n):
    if n <= 1:
        return 1
    return n * fact_rec(n - 1)


def fact_it(n):
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res


if __name__ == "__main__":
    n = 1000

    import time

    start = time.perf_counter()
    print(fact_rec(n))
    print(f"рекурсия:  {time.perf_counter() - start:.6f} с")

    start = time.perf_counter()
    print(fact_it(n))
    print(f"итерация:  {time.perf_counter() - start:.6f} с")