import pytest

from calc.query import OperandError, parse_operands_from_query


def test_parse_operands_success_case_insensitive():
    operands = parse_operands_from_query("a=1&b=2")
    assert operands.a == 1.0
    assert operands.b == 2.0

    operands2 = parse_operands_from_query("A=3&B=4")
    assert operands2.a == 3.0
    assert operands2.b == 4.0


def test_parse_operands_missing_a():
    with pytest.raises(OperandError, match=r"Missing parameter A"):
        parse_operands_from_query("b=2")


def test_parse_operands_invalid_number():
    with pytest.raises(OperandError, match=r"Invalid number for A"):
        parse_operands_from_query("a=abc&b=2")


def test_parse_operands_duplicate_a_is_error():
    with pytest.raises(OperandError, match=r"Multiple values for A"):
        parse_operands_from_query("a=1&a=2&b=3")


def test_parse_operands_blank_is_missing():
    with pytest.raises(OperandError, match=r"Missing parameter A"):
        parse_operands_from_query("a=&b=2")
