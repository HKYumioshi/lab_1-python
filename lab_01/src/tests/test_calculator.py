import pytest

from toolkit.calculator import calculate
from toolkit.calculator import rpn_conversion
from toolkit.calculator import tokenize
from toolkit.calculator import validate
from toolkit.errors import CalculatorError


def run(expression: str) -> float:
    tokens = tokenize(expression)
    tokens = validate(tokens)
    rpn = rpn_conversion(tokens)
    return calculate(rpn)


#позитивные тесты 

def test_tokenize_basic():
    assert tokenize("2+3") == [2.0, "+", 3.0]


def test_tokenize_ignores_spaces():
    assert tokenize("  2  +   3 ") == [2.0, "+", 3.0]


def test_tokenize_floats_and_parentheses():
    assert tokenize("(1.5*2)") == ["(", 1.5, "*", 2.0, ")"]


def test_validate_folds_unary_minus_into_number():
    tokens = validate(tokenize("-5+3"))
    assert tokens == [-5.0, "+", 3.0]


def test_validate_folds_unary_plus_into_number():
    tokens = validate(tokenize("+5+3"))
    assert tokens == [5.0, "+", 3.0]


def test_precedence_multiplication_over_addition():
    assert run("2 + 3 * 4") == 14.0


def test_parentheses_change_precedence():
    assert run("(2 + 3) * 4") == 20.0


def test_full_pipeline_with_unary_and_parentheses():
    assert run("-5 + (2 + 3)") == 0.0


def test_rpn_conversion_simple():
    tokens = validate(tokenize("2+3*4"))
    assert rpn_conversion(tokens) == [2.0, 3.0, 4.0, "*", "+"]


#негативные тесты 

def test_tokenize_empty_expression_raises():
    with pytest.raises(CalculatorError):
        tokenize("")


def test_tokenize_invalid_number_raises():
    with pytest.raises(CalculatorError):
        tokenize("1.2.3")


def test_validate_consecutive_operators_raises():
    with pytest.raises(CalculatorError):
        validate(tokenize("2 * * 3"))


def test_validate_missing_operand_at_end_raises():
    with pytest.raises(CalculatorError):
        validate(tokenize("2+"))


def test_validate_unmatched_parenthesis_raises():
    with pytest.raises(CalculatorError):
        validate(tokenize("(2+3"))


def test_calculate_division_by_zero_raises():
    tokens = validate(tokenize("1/0"))
    rpn = rpn_conversion(tokens)
    with pytest.raises(ZeroDivisionError):
        calculate(rpn)
