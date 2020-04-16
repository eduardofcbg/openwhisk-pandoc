from sanic.response import json


def _build_response(*, status=200, body=None, headers=None):
    return json({"statusCode": status, "body": body, "headers": headers or {},})


def document_response(
    *, status, document=None, command=None, content_type=None,
):
    headers = {
        "Content-Type": content_type,
        "Pandoc-Command": command,
    }

    return _build_response(status=status, body=document, headers=headers)
