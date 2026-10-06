"""A small interactive calculator used to demonstrate CI/CD."""

import re


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


_EXPRESSION = re.compile(
    r"^\s*(-?(?:\d+(?:\.\d*)?|\.\d+))\s*([+\-*/])\s*"
    r"(-?(?:\d+(?:\.\d*)?|\.\d+))\s*$"
)


def calculate(expression: str) -> float:
    """Evaluate one supported two-number arithmetic expression."""
    match = _EXPRESSION.fullmatch(expression)
    if match is None:
        raise ValueError("Use: number operator number (for example, 10 + 5)")

    left, operator, right = match.groups()
    a, b = float(left), float(right)
    operations = {
        "+": add,
        "-": subtract,
        "*": multiply,
        "/": divide,
    }
    return operations[operator](a, b)


def main() -> None:
    print("CI/CD Demo Calculator")
    print("Enter an expression (for example, 10 + 5); type 'q' to quit.")
    while True:
        try:
            expression = input("> ")
        except EOFError:
            print()
            break
        if expression.strip().lower() in {"q", "quit"}:
            break
        try:
            print(f"Result: {calculate(expression)}")
        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
