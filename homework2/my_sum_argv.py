import sys


def my_sum_argv(numbers):
    total = sum(int(x) for x in numbers)
    return total


if __name__ == "__main__":
    numbers = sys.argv[1:]
    print(my_sum_argv(numbers))