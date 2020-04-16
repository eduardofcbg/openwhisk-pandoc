import base64
from functools import wraps

from sanic import Blueprint, response
from sanic.log import logger
from sanic.response import text

from .mime_types import binary as binary_mime_types
from .openwhisk import document_response
from .process import execute

pandoc = Blueprint("pandoc")


@pandoc.post("/run")
async def run(request):
    action = request.json
    payload = action["value"]
    headers = payload["__ow_headers"]

    content_type = headers.get("accept", "text/plain")

    body = payload["__ow_body"]
    input_document = base64.b64decode(body)

    pandoc_options = headers.get("pandoc-options", "-v")
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
            document="Cannot convert",
            errors=errors,
            command=command,
            content_type="text/plain",
        )
    else:
        print("type " + content_type)
        if content_type in binary_mime_types:
            document = base64.b64encode(stdout_data)
        else:
            document = stdout_data.decode("utf-8")

        return document_response(
            status=207 if errors else 200,
            document=document,
            errors=errors,
            command=command,
            content_type=content_type,
        )


@pandoc.post("/init")
async def init(request):
    return text("OK")
