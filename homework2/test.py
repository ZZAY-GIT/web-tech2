import pytest
from math import isclose, pi
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fact import fact_rec, fact_it
from process_list import process_list, process_list_comp, process_list_gen
from email_validation import fun
from fibonacci import fibonacci
from average_scores import compute_average_scores
from plane_angle import plane_angle, Point
from phone_number import sort_phone
from complex_numbers import Complex
from circle_square_mk import circle_square_mk
from my_sum import my_sum
from my_sum_argv import my_sum_argv
from sum_and_sub import sum_and_sub
from show_employee import show_employee
from files_sort import files_sort
from log_decorator import greeting_format
from people_sort import name_format

test_data = {
    'fact_rec': [
        (0, 1),
        (5, 120)
    ],
    'fact_it': [
        (5, 120),
        (7, 5040)
    ],
    'process_list': [
        ([1, 2, 3, 4], [1, 4, 27, 16]),
        ([], []),
        ([0], [0]),
        ([2], [4]),
        ([1, 3, 5], [1, 27, 125]),
        ([-1, -2, 3], [-1, 4, 27]),
        ([10, 11], [100, 1331]),
        ([7, 8, 9], [343, 64, 729]),
        ([0, 1, -1], [0, 1, -1])
    ],
    'email_validation': [
        ("user@domain.ru", True),
        ("a1_b-2@site123.co", True),
        ("x@y.z", True),
        ("test-123@abc.def", True),
        ("user@domain", False),
        ("@domain.ru", False),
        ("user@domain.123", False)
    ],
    'fibonacci': [
        (0, []),
        (1, [0]),
        (2, [0, 1]),
        (5, [0, 1, 1, 2, 3]),
        (10, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])
    ],
    'average_scores': [
        ([(90, 80, 70), (85, 95, 88)], (87.5, 87.5, 79.0)),
        ([(100, 100), (0, 0), (50, 50)], (50.0, 50.0))
    ],
    'plane_angle': [
        ((0,0,0, 1,0,0, 0,1,0, 0,0,1), 54.735610317245346),
        ((0,0,0, 1,0,0, 0,1,0, 1,1,0), 0.0)
    ],
    'sort_phone': [
        (["89123456789", "89098765432"], ["+7 (909) 876-54-32", "+7 (912) 345-67-89"]),
        (["81234567890", "+79123456789"], ["+7 (123) 456-78-90", "+7 (912) 345-67-89"]),
        (["8(912)345-67-89", "7-910-987-65-43"], ["+7 (910) 987-65-43", "+7 (912) 345-67-89"])
    ],
    'complex_add': [
        (2, 1, 5, 6, 7.0, 7.0)
    ],
    'complex_sub': [
        (1, 2, 3, 4, -2.0, -2.0)
    ],
    'complex_mul': [
        (1, 2, 3, 4, -5.0, 10.0)
    ],
    'complex_div': [
        (4, 2, 2, 0, 2.0, 1.0)
    ],
    'complex_mod': [
        (3, 4, 5.0)
    ],
    'monte_carlo': [
        (1.0, 50000, 0.10),
        (2.0, 100000, 0.06)
    ],
    'my_sum': [
        ((), 0),
        ((1,), 1),
        ((1, 2, 3), 6),
        ((10, 20, 30, 40), 100),
        ((-1, -2, -3), -6)
    ],
    'my_sum_argv': [
        (["1", "2", "3"], 6),
        (["10", "20"], 30),
        (["-1", "-2"], -3),
        (["100"], 100),
        (["0", "0", "0"], 0)
    ],
    'sum_and_sub': [
        (22, 12, (34, 10)),
        (1233, 21, (1254, 1212)),
        (0, 0, (0, 0))
    ],
    'show_employee': [
        ("Иван", 50000, "Иван: 50000 ₽"),
        ("Петр", None, "Петр: 100000 ₽"),
        ("Мария", 75000, "Мария: 75000 ₽")
    ],
    'greeting_format': [
        ("John", {}, "Hello, John!"),
        ("Anna", {"greeting": "Привет"}, "Привет, Anna!")
    ],
    'name_format': [
        (["John", "Doe", "25", "M"], "Mr. John Doe"),
        (["Jane", "Smith", "30", "F"], "Ms. Jane Smith")
    ]
}


@pytest.mark.parametrize("n, expected", test_data['fact_rec'])
def test_fact_rec(n, expected):
    assert fact_rec(n) == expected

@pytest.mark.parametrize("n, expected", test_data['fact_it'])
def test_fact_it(n, expected):
    assert fact_it(n) == expected

@pytest.mark.parametrize("input_list, expected", test_data['process_list'])
def test_process_list(input_list, expected):
    assert process_list(input_list) == expected
    assert process_list_comp(input_list) == expected
    assert list(process_list_gen(input_list)) == expected

@pytest.mark.parametrize("email, expected", test_data['email_validation'])
def test_email_validation(email, expected):
    assert fun(email) is expected

@pytest.mark.parametrize("n, expected", test_data['fibonacci'])
def test_fibonacci(n, expected):
    assert fibonacci(n) == expected

@pytest.mark.parametrize("scores, expected", test_data['average_scores'])
def test_average_scores(scores, expected):
    result = compute_average_scores(scores)
    for a, b in zip(result, expected):
        assert isclose(a, b, abs_tol=0.05)

@pytest.mark.parametrize("coords, expected", test_data['plane_angle'])
def test_plane_angle(coords, expected):
    ax, ay, az, bx, by, bz, cx, cy, cz, dx, dy, dz = coords
    A = Point(ax, ay, az)
    B = Point(bx, by, bz)
    C = Point(cx, cy, cz)
    D = Point(dx, dy, dz)
    angle = plane_angle(A, B, C, D)
    assert isclose(angle, expected, abs_tol=0.5)

@pytest.mark.parametrize("numbers, expected", test_data['sort_phone'])
def test_sort_phone(numbers, expected):
    result = sort_phone(numbers)
    assert result == expected

@pytest.mark.parametrize("r1,i1,r2,i2,exp_r,exp_i", test_data['complex_add'])
def test_complex_add(r1, i1, r2, i2, exp_r, exp_i):
    c1 = Complex(r1, i1)
    c2 = Complex(r2, i2)
    res = c1 + c2
    assert isclose(res.real, exp_r, abs_tol=1e-9)
    assert isclose(res.imaginary, exp_i, abs_tol=1e-9)

@pytest.mark.parametrize("r1,i1,r2,i2,exp_r,exp_i", test_data['complex_sub'])
def test_complex_sub(r1, i1, r2, i2, exp_r, exp_i):
    c1 = Complex(r1, i1)
    c2 = Complex(r2, i2)
    res = c1 - c2
    assert isclose(res.real, exp_r, abs_tol=1e-9)
    assert isclose(res.imaginary, exp_i, abs_tol=1e-9)

@pytest.mark.parametrize("r1,i1,r2,i2,exp_r,exp_i", test_data['complex_mul'])
def test_complex_mul(r1, i1, r2, i2, exp_r, exp_i):
    c1 = Complex(r1, i1)
    c2 = Complex(r2, i2)
    res = c1 * c2
    assert isclose(res.real, exp_r, abs_tol=1e-9)
    assert isclose(res.imaginary, exp_i, abs_tol=1e-9)

@pytest.mark.parametrize("r1,i1,r2,i2,exp_r,exp_i", test_data['complex_div'])
def test_complex_div(r1, i1, r2, i2, exp_r, exp_i):
    c1 = Complex(r1, i1)
    c2 = Complex(r2, i2)
    res = c1 / c2
    assert isclose(res.real, exp_r, abs_tol=1e-9)
    assert isclose(res.imaginary, exp_i, abs_tol=1e-9)

@pytest.mark.parametrize("r,i,expected", test_data['complex_mod'])
def test_complex_mod(r, i, expected):
    c = Complex(r, i)
    res = c.mod()
    assert isclose(res.real, expected, abs_tol=1e-9)

@pytest.mark.parametrize("r,n,tol", test_data['monte_carlo'])
def test_monte_carlo(r, n, tol):
    estimated = circle_square_mk(r, n)
    exact = pi * r * r
    assert isclose(estimated, exact, rel_tol=tol)

@pytest.mark.parametrize("args, expected", test_data['my_sum'])
def test_my_sum(args, expected):
    assert isclose(my_sum(*args), expected, abs_tol=1e-9)

@pytest.mark.parametrize("numbers, expected", test_data['my_sum_argv'])
def test_my_sum_argv(numbers, expected):
    assert my_sum_argv(numbers) == expected

@pytest.mark.parametrize("a,b,expected", test_data['sum_and_sub'])
def test_sum_and_sub(a, b, expected):
    assert sum_and_sub(a, b) == expected

@pytest.mark.parametrize("name,salary,expected", test_data['show_employee'])
def test_show_employee(name, salary, expected):
    if salary is None:
        assert show_employee(name) == expected
    else:
        assert show_employee(name, salary) == expected

@pytest.mark.parametrize("name,kwargs,expected", test_data['greeting_format'])
def test_greeting_format(name, kwargs, expected):
    if kwargs:
        assert greeting_format(name, **kwargs) == expected
    else:
        assert greeting_format(name) == expected

@pytest.mark.parametrize("person, expected", test_data['name_format'])
def test_name_format(person, expected):
    people = [person]
    result = name_format(people)
    assert result[0] == expected

def test_files_sort_1(tmp_path):
    (tmp_path / "a.txt").touch()
    (tmp_path / "b.doc").touch()
    (tmp_path / "c.txt").touch()
    result = files_sort(str(tmp_path))
    assert result == ["b.doc", "a.txt", "c.txt"]

def test_files_sort_2(tmp_path):
    (tmp_path / "1.py").touch()
    (tmp_path / "2.py").touch()
    assert files_sort(str(tmp_path)) == ["1.py", "2.py"]

def test_files_sort_3(tmp_path):
    (tmp_path / "file1").touch()
    (tmp_path / "file2.txt").touch()
    result = files_sort(str(tmp_path))
    assert result == ["file1", "file2.txt"]

def test_files_sort_4(tmp_path):
    (tmp_path / "dir").mkdir()
    assert files_sort(str(tmp_path)) == []
