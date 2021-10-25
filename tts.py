from os import system
import asyncio


async def say(text):
    return system(f'say {text}')


if __name__ == "__main__":
    asyncio.run(say('Dale wacho, requetebien piola. Cajetiala toda gato, oh my god. '
                    'Y andate a la concha de tu madre all boys'))
