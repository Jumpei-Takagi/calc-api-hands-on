import azure.functions as func

from function_app import divide_api, multiply_api


class DummyRequest:
    def __init__(self, url: str):
        self.url = url


def _body_text(resp: func.HttpResponse) -> str:
    return resp.get_body().decode("utf-8")


def test_divide_api_returns_200_and_error_on_division_by_zero():
    req = DummyRequest("https://example/api/divide?A=10&B=0")
    resp = divide_api(req)

    assert resp.status_code == 200
    assert _body_text(resp) == "Error: Division by zero"


def test_multiply_api_returns_200_and_error_on_duplicate_param():
    req = DummyRequest("https://example/api/multiply?A=1&A=2&B=3")
    resp = multiply_api(req)

    assert resp.status_code == 200
    assert _body_text(resp) == "Error: Multiple values for A"
