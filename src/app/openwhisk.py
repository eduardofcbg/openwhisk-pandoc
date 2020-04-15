from sanic.handlers import ErrorHandler
from sanic.exceptions import SanicException
from sanic.response import json


def _build_response(*, status=200, body=None, headers=None):
    return json({"statusCode": status, "body": body, "headers": headers or {},})


def document_response(
    *,
    status,
    document=None,
    errors=None,
    command=None,
    content_type=None,
    extention=None
):
    feedback = {
        "Pandoc-Extention": extention,
        "Pandoc-Command": command,
    }

    if errors:
        feedback["Pandoc-Errors"] = errors

    headers = {"Content-Type": content_type, **feedback}

    return _build_response(status=status, body=document, headers=headers)


def not_acceptable():
    return _build_response(status=406)


class OpenwhiskErrorHandler(ErrorHandler):
    def default(self, request, exception):
        defaultReponse = super().default(request, exception)

        if isinstance(exception, SanicException):
            return defaultReponse
        else:
            headers = {"Content-Type": "text/plain"}
            return _build_response(status=500, body="Server error", headers=headers)
