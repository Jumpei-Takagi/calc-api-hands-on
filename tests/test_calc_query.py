import pytest

from calc.query import OperandError, parse_operands_from_query, parse_operands_from_request


class DummyRequest:
    def __init__(self, url: str):
        self.url = url


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


def test_parse_operands_missing_b():
    with pytest.raises(OperandError, match=r"Missing parameter B"):
        parse_operands_from_query("a=1")


def test_parse_operands_duplicate_b_is_error():
    with pytest.raises(OperandError, match=r"Multiple values for B"):
        parse_operands_from_query("a=1&b=2&b=3")


def test_parse_operands_blank_b_is_missing():
    with pytest.raises(OperandError, match=r"Missing parameter B"):
        parse_operands_from_query("a=1&b=")


def test_parse_operands_duplicate_case_insensitive_is_error():
    with pytest.raises(OperandError, match=r"Multiple values for A"):
        parse_operands_from_query("A=1&a=2&b=3")


@pytest.mark.parametrize(
    ("raw_query", "expected_message"),
    [
        ("a=NaN&b=1", r"Invalid number for A"),
        ("a=Inf&b=1", r"Invalid number for A"),
        ("a=-Inf&b=1", r"Invalid number for A"),
        ("a=1&b=NaN", r"Invalid number for B"),
        ("a=1&b=Inf", r"Invalid number for B"),
        ("a=1&b=-Inf", r"Invalid number for B"),
    ],
)
def test_parse_operands_non_finite_is_invalid(raw_query: str, expected_message: str):
    with pytest.raises(OperandError, match=expected_message):
        parse_operands_from_query(raw_query)


def test_parse_operands_trims_whitespace():
    operands = parse_operands_from_query("a=%201%20&b=%202%20")
    assert operands.a == 1.0
    assert operands.b == 2.0


def test_parse_operands_extra_params_are_ignored():
    operands = parse_operands_from_query("a=1&b=2&x=3")
    assert operands.a == 1.0
    assert operands.b == 2.0


def test_parse_operands_from_request_parses_url_query():
    req = DummyRequest("https://example/api/multiply?A=10&B=20")
    a, b = parse_operands_from_request(req)
    assert a == 10.0
    assert b == 20.0


def test_parse_operands_from_request_detects_duplicates_from_url_query():
    req = DummyRequest("https://example/api/multiply?A=1&A=2&B=3")
    with pytest.raises(OperandError, match=r"Multiple values for A"):
        parse_operands_from_request(req)
