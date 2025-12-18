import azure.functions as func

from calc.core import divide, multiply
from calc.query import OperandError, parse_operands_from_request

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="multiply", methods=["GET"])
def multiply_api(req: func.HttpRequest) -> func.HttpResponse:
    try:
        a, b = parse_operands_from_request(req)
        result_text = multiply(a, b)
        return func.HttpResponse(result_text, status_code=200, mimetype="text/plain")
    except (OperandError, ValueError) as exc:
        return func.HttpResponse(f"Error: {exc}", status_code=200, mimetype="text/plain")


@app.route(route="divide", methods=["GET"])
def divide_api(req: func.HttpRequest) -> func.HttpResponse:
    try:
        a, b = parse_operands_from_request(req)
        result_text = divide(a, b)
        return func.HttpResponse(result_text, status_code=200, mimetype="text/plain")
    except (OperandError, ValueError) as exc:
        return func.HttpResponse(f"Error: {exc}", status_code=200, mimetype="text/plain")
