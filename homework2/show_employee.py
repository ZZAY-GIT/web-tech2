def show_employee(name, salary: int = 100000):
    return f"{name}: {salary} ₽"


if __name__ == "__main__":
    print(show_employee("Лёха кофиёк"))
    print(show_employee("Лёха брошка", 25000))