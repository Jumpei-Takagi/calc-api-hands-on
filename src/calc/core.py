from __future__ import annotations

import math


def _format_number(value: float) -> str:
    if not math.isfinite(value):
        raise ValueError("Non-finite result")

    if float(value).is_integer():
        return str(int(value))

    return format(value, ".15g")


def multiply(a: float, b: float) -> str:
    result = a * b
    return f"Result: {_format_number(result)}"


def divide(a: float, b: float) -> str:
    if b == 0:
        raise ValueError("Division by zero")

    result = a / b
    return f"Result: {_format_number(result)}"
