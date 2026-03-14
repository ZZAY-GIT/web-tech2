import subprocess
import pytest
from is_leap import is_leap

# Для Windows
INTERPRETER = 'python'
# Для MAC
# INTERPRETER = 'python3' 

def run_script(filename, input_data=None):
    proc = subprocess.run(
        [INTERPRETER, filename],
        input='\n'.join(input_data if input_data else []),
        capture_output=True,
        text=True,
        check=False
    )
    return proc.stdout.strip()

test_data = {
    'python_if_else': [
        ('1', 'Weird'),
        ('4', 'Not Weird'),
        ('3', 'Weird'),
        ('6','Weird'),
        ('22', 'Not Weird')
    ],
    'arithmetic_operators': [
        (['1', '2'], ['3', '-1', '2']),
        (['10', '5'], ['15', '5', '50'])
    ],
    'division': [(['3', '5'], ['0', '0.6']),
                 (['3', '0'], ['Division by zero'])
                ],
    'loops': [(['5'], ['0', '1', '4', '9', '16']),
              (['7'], ['0', '1', '4', '9', '16', '25', '36'])
    ],
    'print_function': [(['5'], ['12345']),
                       (['7'], ['1234567']),
                       (['2'], ['12'])
    ],
    'second_score': [(['12', '1 2 3 4 4 5 5 6 6 34 12 22'], ['22']),
                     (['5', '1 2 7 5 6'], ['6'])
    ],
    'nested_list': [
                     (['3', 'гарри', '37.21', 'Аня', '41', 'Лёха', '37.2'], ['гарри']),
                     (['5', 'Гарри', '37.21', 'Берри', '37.21', 'Тина', '37.2', 'Акрити', '41', 'Харш', '39'], ['Берри', 'Гарри']),
                     (['4', 'aaa', '10', 'bbb', '20', 'ccc', '10', 'ddd', '15'], ['ddd']),
                     (['6', 'x', '5.5', 'y', '5.5', 'z', '6.0', 'w', '6.0', 'v', '7.0', 'u', '5.5'], ['w', 'z']),
                     (['2', 'Alpha', '9.99', 'Beta', '10.00'], ['Beta']),
                     (['7', 'Петя', '4.5', 'Маша', '3.0', 'Коля', '5.0', 'Оля', '4.5', 'Вася', '4.5', 'Яна', '4.5', 'Зина', '4.5'], ['Вася', 'Зина', 'Оля', 'Петя', 'Яна']),
    ],
    'lists': [
                     (['12', 'insert 0 5', 'insert 1 10', 'insert 0 6', 'print', 'remove 6', 'append 9', 'append 1', 'sort', 'print', 'pop', 'reverse', 'print'], ['[6, 5, 10]', '[1, 5, 9, 10]', '[9, 5, 1]']),
                     (['6', 'append 100', 'append 200', 'insert 0 50', 'print', 'remove 100', 'print'], ['[50, 100, 200]', '[50, 200]']),
    ],
    'swap_case': [
        (['Www.MosPolytech.ru'], ['wWW.mOSpOLYTECH.RU']),
        (['Pythonist 2'], ['pYTHONIST 2'])
    ],
    'split_and_join': [
        (['this is a string'], ['this-is-a-string']),
        (['1'], ['1']),
        (['1 2'], ['1-2']),
                       ],
    'anagram': [
        (['abc', "bac"], ["YES"]),
        (['adc', "bac"], ["NO"]),
        (['rftr', "ftrr"], ["YES"]),
        (['сОн', "Нос"], ["YES"]),
        (['сон', "носс"], ["NO"]),
        (['tG', "gt"], ["YES"]),
    ],
    'metro': [
        (['3', '10 20', '15 25', '5 30', '18'], ['3']),
        (['2', '1 5', '6 10', '5'], ['1']),
    ],
    'minion_game': [
        (['BANANA'], ['Стюарт 12']),
        (['AEOUIA'], ['Кевин 21']),
        (['BRTSPK'], ['Стюарт 21']),
        (['AUDIO'], ['Кевин 11']),
        (['AB'], ['Кевин 2']),
    ],
    'is_leap': [
        (2000, True),
        (1900, False),
        (2024, True),
        (2023, False),
        (2400, True),
        (2100, False),
        (1600, True),
        (1700, False),
        (2004, True),
        (1999, False),
        (0, True),
        (4, True),
        (100, False),
    ],
    'happiness': [
        (['3 2', '1 5 3', '3 1', '5 7'], ['1']),
        (['8 3', '4 7 4 2 9 4 7 10', '4 2 9', '7 10 3'], ['2']),
        (['5 4', '10 20 10 30 20', '10 20 30 40', '99 88 77'], ['5'])
    ],
    'pirate_ship': [
        (['10 4', 'золото 5 300', 'серебро 8 160', 'жемчуг 3 210', 'вино 6 90'], ['золото 5.00 300.00', 'жемчуг 3.00 210.00', 'серебро 2.00 40.00']),
        (['30 5', 'алмазы 12 1200', 'рубины 8 960', 'изумруды 15 900', 'золото 10 500', 'серебро 20 300'], ['алмазы 12.00 1200.00', 'рубины 8.00 960.00', 'изумруды 10.00 600.00']),
        (['17 4', 'картина 10 800', 'статуя 9 720', 'монеты 6 360', 'часы 12 480'], ['картина 10.00 800.00', 'статуя 7.00 560.00']),
        (['25 3', 'бриллиант 20 5000', 'золото 15 1200', 'серебро 30 900'], ['бриллиант 20.00 5000.00', 'золото 5.00 400.00']),
        (['4 5', 'сапфир 10 1500', 'рубин 8 1400', 'изумруд 12 1800', 'жемчуг 5 600', 'монеты 3 300'], ['рубин 4.00 700.00'])
    ],
    'matrix_mult': [
        (['3', '1 2 3', '4 5 6', '7 8 9', '9 8 7', '6 5 4', '3 2 1'], ['30 24 18', '84 69 54', '138 114 90']),
        (['3', '1 0 0', '0 1 0', '0 0 1', '5 1 8', '2 4 9', '7 3 6'], ['5 1 8', '2 4 9', '7 3 6']),
        (['3', '1 -2 3', '-4 5 -6', '7 -8 9', '2 1 -1', '0 -3 4', '5 6 -2'], ['17 25 -15', '-38 -55 36', '59 85 -57'])
    ]
}

def test_hello_world():
    assert run_script('hello_world.py') == 'Hello, world!'

@pytest.mark.parametrize("input_data, expected", test_data['python_if_else'])
def test_python_if_else(input_data, expected):
    assert run_script('python_if_else.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['arithmetic_operators'])
def test_arithmetic_operators(input_data, expected):
    assert run_script('arithmetic_operators.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['division'])
def test_division(input_data, expected):
    assert run_script('division.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['loops'])
def test_loops(input_data, expected):
    assert run_script('loops.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['print_function'])
def test_print_function(input_data, expected):
    assert run_script('print_function.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['second_score'])
def test_second_score(input_data, expected):
    assert run_script('second_score.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['nested_list'])
def test_nested_list(input_data, expected):
    assert run_script('nested_list.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['lists'])
def test_lists(input_data, expected):
    assert run_script('lists.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['swap_case'])
def test_swap_case(input_data, expected):
    assert run_script('swap_case.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['split_and_join'])
def test_split_and_join(input_data, expected):
    assert run_script('split_and_join.py', input_data).split('\n') == expected

def test_max_word():
    assert run_script('max_word.py') == 'сосредоточенности'

def test_price_sum():
    assert run_script('price_sum.py') == '6842.84 5891.06 6810.90'
    
@pytest.mark.parametrize("input_data, expected", test_data['anagram'])
def test_anagram(input_data, expected):
    assert run_script('anagram.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['is_leap'])
def test_is_leap(input_data, expected):
    assert is_leap(input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['happiness'])
def test_happiness(input_data, expected):
    assert run_script('happiness.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['pirate_ship'])
def test_pirate_ship(input_data, expected):
    assert run_script('pirate_ship.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['matrix_mult'])
def test_matrix_mult(input_data, expected):
    assert run_script('matrix_mult.py', input_data).split('\n') == expected
    