def my_sum(*args):
    return sum(args)

if __name__ == "__main__":
    print(my_sum(1, 2, 3, 4))
    print(my_sum(1, 2, 3, 400))
    print(my_sum(10, 2, 3, 4))