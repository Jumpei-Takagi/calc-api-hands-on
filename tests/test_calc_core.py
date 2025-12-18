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
