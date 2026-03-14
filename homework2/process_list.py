def process_list(arr):
    """Исходная функция"""
    result = []
    for i in arr:
        if i % 2 == 0:
            result.append(i**2)
        else:
            result.append(i**3)
    return result


def process_list_comp(arr):
    """Версия с list comprehension"""
    return [x**2 if x % 2 == 0 else x**3 for x in arr]


def process_list_gen(arr):
    """Генератор (yield)"""
    for x in arr:
        if x % 2 == 0:
            yield x**2
        else:
            yield x**3

if __name__ == "__main__":
    arr = list(range(1, 1000001))

    import time

    start = time.perf_counter()
    process_list(arr)
    print(f"for + append     : {time.perf_counter() - start:.6f} с")

    start = time.perf_counter()
    process_list_comp(arr)
    print(f"list comp        : {time.perf_counter() - start:.6f} с")

    start = time.perf_counter()
    list(process_list_gen(arr))
    print(f"generator → list : {time.perf_counter() - start:.6f} с")