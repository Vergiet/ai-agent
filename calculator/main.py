# main.py

import sys
from pkg.calculator import Calculator
from pkg.render import render

def is_valid_expression(expression):
    valid_characters = "0123456789+-*/. () "
    if not expression:
        return True

    # Check for consecutive operators
    for i in range(len(expression) - 1):
        if expression[i] in "+-*/" and expression[i+1] in "*/":
            return False
        # Allow '+' or '-' after '(' or at the beginning of the expression
        if expression[i] in '()' and expression[i+1] in '+-':
            continue
        if expression[i] in '+-' and expression[i+1] in '+-' and i != 0 and expression[i-1] not in '(':
          return False
        if expression[i] in '*/' and expression[i+1] in '+-':
          return False

    # Check for unbalanced parentheses
    open_parentheses = 0
    for char in expression:
        if char == '(':
            open_parentheses += 1
        elif char == ')':
            open_parentheses -= 1
        if open_parentheses < 0:
            return False
    if open_parentheses != 0:
        return False

    for char in expression:
        if char not in valid_characters:
            return False

    return True

def main():
    calculator = Calculator()
    if len(sys.argv) <= 1:
        print("Calculator App")
        print('Usage: python main.py "<expression>"')
        print('Example: python main.py "3 + 5"')
        return

    expression = " ".join(sys.argv[1:])

    if not is_valid_expression(expression):
        print("Error: Invalid characters in expression.")
        return

    try:
        result = calculator.evaluate(expression)
        to_print = render(expression, result)
        print(to_print)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
