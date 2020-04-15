import base64
from shlex import quote

from sanic import Blueprint, response
from sanic.log import logger
from sanic.response import text

from .openwhisk import build_response, not_acceptable
from .process import execute
from .mime_types import mime_extention

pandoc = Blueprint("openwhisk")


@pandoc.post("/run")
async def run(request):
    payload = request.json
    headers = payload.get("__ow_headers", {})

    accept = headers.get("Accept")
    if accept in mime_extention:
        content_type = accept
        extention = mime_extention[accept]
    else:
        return not_acceptable()

    render_options = headers.get("Render-Options", "-v")
    command = "pandoc " + quote(render_options)

    logger.info("Will execute: %s", command)
    stdout_data, stderr_data = await execute(command)

    if stderr_data:
        errors = stderr_data.decode("utf-8")
        logger.error("Render errors: %s", errors)
    else:
        errors = None

    if not stdout_data:
        return build_response(
            status=400,
            document=None,
            errors=errors,
            command=command,
            content_type=content_type,
            extention=extention,
        )
    if stdout_data:
        document = base64.encodebytes(stdout_data)
        return build_response(
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
