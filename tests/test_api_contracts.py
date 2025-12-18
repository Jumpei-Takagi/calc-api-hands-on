import pytest

from calc.core import divide


def test_divide_zero_check_matches_requirements():
    with pytest.raises(ValueError, match=r"Division by zero"):
        divide(10.0, 0.0)
