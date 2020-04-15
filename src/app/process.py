from asyncio import create_subprocess_shell, create_task, CancelledError
from subprocess import PIPE


async def execute(command, stdin):
    process = await create_subprocess_shell(
        command, stdin=PIPE, stdout=PIPE, stderr=PIPE
    )
    communitation = create_task(process.communicate(stdin))

    try:
        return await communitation
    except CancelledError as e:
        process.terminate()
        raise e
