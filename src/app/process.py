from asyncio import create_subprocess_shell, create_task, CancelledError
from subprocess import PIPE


async def execute(command):
    process = await create_subprocess_shell(command, stdout=PIPE, stderr=PIPE)
    communitation = create_task(process.communicate())

    try:
        return await communitation
    except CancelledError as e:
        process.terminate()
        raise e
