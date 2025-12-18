from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple
from urllib.parse import parse_qs, urlsplit


class OperandError(ValueError):
    pass


@dataclass(frozen=True)
class Operands:
    a: float
    b: float


def _parse_query_string(raw_query: str) -> Dict[str, List[str]]:
    parsed = parse_qs(raw_query, keep_blank_values=True)
    lowered: Dict[str, List[str]] = {}
    for key, values in parsed.items():
        lowered.setdefault(key.lower(), []).extend(values)
    return lowered


def _extract_single_value(params: Dict[str, List[str]], key: str, display_key: str) -> str:
    values = params.get(key)
    if values is None:
        raise OperandError(f"Missing parameter {display_key}")
    if len(values) != 1:
        raise OperandError(f"Multiple values for {display_key}")

    value = values[0].strip()
    if value == "":
        raise OperandError(f"Missing parameter {display_key}")
    return value


def _parse_float(value: str, display_key: str) -> float:
    try:
        number = float(value)
    except ValueError as exc:
        raise OperandError(f"Invalid number for {display_key}") from exc

    if not math.isfinite(number):
        raise OperandError(f"Invalid number for {display_key}")

    return number


def parse_operands_from_query(raw_query: str) -> Operands:
    params = _parse_query_string(raw_query)

    a_raw = _extract_single_value(params, "a", "A")
    b_raw = _extract_single_value(params, "b", "B")

    a = _parse_float(a_raw, "A")
    b = _parse_float(b_raw, "B")

    return Operands(a=a, b=b)


def parse_operands_from_request(req) -> Tuple[float, float]:
    # azure.functions.HttpRequest has .url; parsing raw query is needed to detect duplicates.
    query = urlsplit(req.url).query
    operands = parse_operands_from_query(query)
    return operands.a, operands.b
