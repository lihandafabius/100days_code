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

num1 = int(input("What's your first number?"))

for symbol in operations:
    print(symbol)

to_continue = True

while to_continue:
    operation_symbol = input("Pick an operation from the lines above: ")
    num2 = int(input("What's your second number?"))

    calculation_function = operations[operation_symbol]
    first_answer = calculation_function(num1, num2)

    print(f"{num1} {operation_symbol} {num2} = {first_answer}")

    to_continue = input("Type 'Y' to continue calculating with the result, or 'N' to exit: ")

    if to_continue.lower() == 'y':
        num1 = first_answer  # Update num1 with the result of the first calculation
        num3 = int(input("What's the next number: "))
        operation_symbol = input(
            "Pick a new operation from the lines above: ")  # Allow the user to choose a new operation
        calculation_function = operations[operation_symbol]
        second_answer = calculation_function(num1, num3)

        print(f"{num1} {operation_symbol} {num3} = {second_answer}")

        to_continue = input("Type 'Y' to continue calculating with the result, or 'N' to exit: ")
    else:
        to_continue = False
