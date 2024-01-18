from art3 import logo


def add(n1, n2):
    return n1 + n2


def subtract(n1, n2):
    return n1 - n2


def multiply(n1, n2):
    return n1 * n2


def divide(n1, n2):
    return n1 / n2


operations = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide
}


def calculator():
    print(logo)
    num1 = float(input("What's your first number?"))

    for symbol in operations:
        print(symbol)

    to_continue = True

    while to_continue:
        operation_symbol = input("Pick an operation from the lines above: ")
        num2 = float(input("What's the next number: "))

        calculation_function = operations[operation_symbol]
        answer = calculation_function(num1, num2)

        print(f"{num1} {operation_symbol} {num2} = {answer}")

        if input(f"Type 'Y' to continue calculating with {answer}, or 'N' to continue from start: ").lower() == 'y':
            num1 = answer
        else:
            to_continue = False
            calculator()


calculator()