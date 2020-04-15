from sanic.handlers import ErrorHandler
from sanic.exceptions import SanicException
from sanic.response import json


def build_response(
    *,
    status,
    document=None,
    errors=None,
    command=None,
    content_type=None,
    extention=None
):
    feedback = {
        "File-Extention": extention,
        "Render-Command": command,
    }

    if errors:
        feedback["Render-Errors"] = errors

    return json(
        {
            "statusCode": status,
            "body": document,
            "headers": {"Content-Type": content_type, **feedback},
        }
    )


def not_acceptable():
    return build_response(status=406)


class OpenwhiskErrorHandler(ErrorHandler):
    def default(self, request, exception):
        defaultReponse = super().default(request, exception)

        if isinstance(exception, SanicException):
            return defaultReponse
        else:
            return build_response(
                status=500, document="Server error", content_type="text/plain"
            )
