import base64
from functools import wraps

from sanic import Blueprint, response
from sanic.log import logger
from sanic.response import text

from .mime_types import binary as binary_mime_types
from .openwhisk import response
from .process import execute

pandoc = Blueprint("pandoc")


@pandoc.post("/run")
async def run(request):
    action = request.json
    payload = action["value"]
    headers = payload["__ow_headers"]

    content_type = headers["content-type"]
    accept = headers.get("accept")

    logger.info("Content-Type: %s", content_type)
    logger.info("Accept: %s", accept)

    res_content_type = accept or "text/plain"

    body = payload.get("__ow_body")
    if body and content_type in binary_mime_types:
        input_document = base64.b64decode(body)
    elif body:
        input_document = body.encode()
    else:
        input_document = None

    pandoc_options = headers.get("pandoc-options", "-v")
    command = "pandoc " + pandoc_options

    logger.info("Will execute: %s", command)
    stdout_data, stderr_data = await execute(command, input_document)

    if stderr_data:
        errors = stderr_data.decode()
        logger.error("Pandoc errors: %s", errors)
    else:
        errors = None

    if not stdout_data and not errors:
        return response(
            status=400,
            document="No data returned",
            command=command,
            content_type="text/plain",
        )

    if not stdout_data and errors:
        return response(
            status=500, document="Error", command=command, content_type="text/plain",
        )

    if stdout_data:
        if res_content_type in binary_mime_types:
            document = base64.b64encode(stdout_data)
        else:
            document = stdout_data.decode()

        return response(
            status=207 if errors else 200,
            document=document,
            command=command,
            content_type=res_content_type,
        )


@pandoc.post("/init")
async def init(request):
    return text("OK")
