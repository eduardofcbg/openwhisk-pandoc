import base64
from functools import wraps

from sanic import Blueprint, response
from sanic.log import logger
from sanic.response import text

from .openwhisk import document_response, not_acceptable
from .process import execute
from .mime_types import mime_extention

pandoc = Blueprint("pandoc")


@pandoc.post("/run")
async def run(request):
    payload = request.json

    headers = payload["__ow_headers"]
    accept = headers.get("Accept")

    if accept not in mime_extention:
        return not_acceptable()

    content_type = accept
    extention = mime_extention[accept]

    body = payload["__ow_body"]
    input_document = base64.b64decode(body)

    pandoc_options = headers.get("Pandoc-Options", "-v")
    command = "pandoc " + pandoc_options

    logger.info("Will execute: %s", command)
    stdout_data, stderr_data = await execute(command, input_document)

    if stderr_data:
        errors = stderr_data.decode("utf-8")
        logger.error("Pandoc errors: %s", errors)
    else:
        errors = None

    if not stdout_data:
        return document_response(
            status=400,
            document=None,
            errors=errors,
            command=command,
            content_type=content_type,
            extention=extention,
        )
    if stdout_data:
        document = base64.encodebytes(stdout_data)
        return document_response(
            status=207 if errors else 200,
            document=document,
            errors=errors,
            command=command,
            content_type=content_type,
            extention=extention,
        )


@pandoc.post("/init")
async def init(request):
    return text("OK")
