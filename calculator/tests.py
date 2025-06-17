# tests.py

import unittest
from pkg.calculator import Calculator
from main import is_valid_expression
from pkg.render import render  # Import the render function

print("Running tests...")  # Add print statement

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        result = self.calculator.evaluate("3 + 5")
        self.assertEqual(result, 8)

    def test_subtraction(self):
        result = self.calculator.evaluate("10 - 4")
        self.assertEqual(result, 6)

    def test_multiplication(self):
        result = self.calculator.evaluate("3 * 4")
        self.assertEqual(result, 12)

    def test_division(self):
        result = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5)

    def test_nested_expression(self):
        result = self.calculator.evaluate("3 * 4 + 5")
        self.assertEqual(result, 17)

    def test_complex_expression(self):
        result = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7)

    def test_empty_expression(self):
        result = self.calculator.evaluate("")
        self.assertIsNone(result)

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("$ 3 5")

    def test_not_enough_operands(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("+ 3")

    def test_valid_expression(self):
        self.assertTrue(is_valid_expression("3 + 5"))
        self.assertTrue(is_valid_expression("10 - 4"))
        self.assertTrue(is_valid_expression("3 * 4"))
        self.assertTrue(is_valid_expression("10 / 2"))
        self.assertTrue(is_valid_expression("2.5 + 3.5"))
        self.assertTrue(is_valid_expression("(2 + 3) * 4"))
        self.assertTrue(is_valid_expression("3 + -5"))  # Allow negative numbers
        self.assertTrue(is_valid_expression("-3 + 5"))  # Allow negative numbers at the beginning

    def test_invalid_expression(self):
        self.assertFalse(is_valid_expression("3 $ 5"))
        self.assertFalse(is_valid_expression("10 & 4"))
        self.assertFalse(is_valid_expression("3 # 4"))
        self.assertFalse(is_valid_expression("10 % 2"))
        self.assertFalse(is_valid_expression("3 ^ 5"))

    def test_render_function(self):
        expression = "3 + 5"
        result = 8
        expected_output = render(expression, result)
        self.assertIsInstance(expected_output, str)
        self.assertIn("3 + 5", expected_output)
        self.assertIn("8", expected_output)

    def test_render_function_float_result(self):
        expression = "10 / 4"
        result = 2.5
        expected_output = render(expression, result)
        self.assertIsInstance(expected_output, str)
        self.assertIn("10 / 4", expected_output)
        self.assertIn("2.5", expected_output)

    def test_render_function_integer_float_result(self):
        expression = "10 / 2"
        result = 5.0
        expected_output = render(expression, result)
        self.assertIsInstance(expected_output, str)
        self.assertIn("10 / 2", expected_output)
        self.assertIn("5", expected_output)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calculator.evaluate("10 / 0")

    def test_large_numbers(self):
        result = self.calculator.evaluate("1000000 * 1000000")
        self.assertEqual(result, 1000000000000)

    def test_exponentiation(self):
        result = self.calculator.evaluate("2 ** 3")
        self.assertEqual(result, 8)

    def test_modulo(self):
        result = self.calculator.evaluate("10 % 3")
        self.assertEqual(result, 1)

    def test_invalid_expression_consecutive_operators(self):
        self.assertFalse(is_valid_expression("3 + * 5"))
        self.assertFalse(is_valid_expression("10 - / 4"))
        self.assertFalse(is_valid_expression("3++5"))
        self.assertFalse(is_valid_expression("3--5"))

    def test_invalid_expression_unbalanced_parentheses(self):
        self.assertFalse(is_valid_expression("(3 + 5"))
        self.assertFalse(is_valid_expression("3 + 5)"))
        self.assertFalse(is_valid_expression("((3 + 5)"))
        self.assertFalse(is_valid_expression("(3 + 5))"))
        self.assertTrue(is_valid_expression("(3 + 5)"))
        self.assertTrue(is_valid_expression("((3 + 5) * 2)"))
        self.assertTrue(is_valid_expression("(-1)"))
        self.assertFalse(is_valid_expression("2+(-1"))

    def test_parentheses(self):
        self.assertEqual(self.calculator.evaluate("(3 + 5) * 2"), 16)
        self.assertEqual(self.calculator.evaluate("2 * (3 + 5)"), 16)
        self.assertEqual(self.calculator.evaluate("((3 + 5) * 2) / 4"), 4)
        self.assertEqual(self.calculator.evaluate("10 - (2 * 3)"), 4)
        self.assertEqual(self.calculator.evaluate("(10 - 2) * 3"), 24)

    def test_unmatched_parentheses(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("(3 + 5")
        with self.assertRaises(ValueError):
            self.calculator.evaluate("3 + 5)")
        with self.assertRaises(ValueError):
            self.calculator.evaluate("((3 + 5)")
        with self.assertRaises(ValueError):
            self.calculator.evaluate("(3 + 5))")


if __name__ == "__main__":
    unittest.main()
