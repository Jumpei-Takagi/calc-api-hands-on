import pytest

from calc.core import divide, multiply


def test_multiply_integer_result_formats_without_decimal():
    assert multiply(2.0, 3.0) == "Result: 6"


def test_multiply_float_result():
    assert multiply(1.5, 2.0) == "Result: 3"


def test_divide_integer_result_formats_without_decimal():
    assert divide(6.0, 3.0) == "Result: 2"


def test_divide_by_zero_raises_value_error():
    with pytest.raises(ValueError):
        divide(1.0, 0.0)


def test_multiply_non_finite_result_raises_value_error():
    with pytest.raises(ValueError, match=r"Non-finite result"):
        multiply(1e308, 1e308)


def test_divide_non_integer_formats_with_significant_digits():
    assert divide(1.0, 3.0) == "Result: 0.333333333333333"


def test_multiply_non_integer_keeps_decimal():
    assert multiply(1.2, 3.0) == "Result: 3.6"
