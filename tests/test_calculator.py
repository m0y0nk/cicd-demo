import pytest

from app.calculator import add, calculate, divide, multiply, subtract


def test_add():
    assert add(10, 5) == 15


def test_subtract():
    assert subtract(10, 5) == 5


def test_multiply():
    assert multiply(10, 5) == 50


def test_divide():
    assert divide(10, 5) == 2


def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("10 + 5", 15),
        ("-2 * 3", -6),
        (".5 + 1.5", 2),
        ("10 / 4", 2.5),
    ],
)
def test_calculate(expression, expected):
    assert calculate(expression) == expected


@pytest.mark.parametrize("expression", ["", "10 +", "1 ** 2", "one + 2"])
def test_calculate_rejects_invalid_expressions(expression):
    with pytest.raises(ValueError, match="Use:"):
        calculate(expression)


def test_calculate_rejects_division_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculate("10 / 0")
