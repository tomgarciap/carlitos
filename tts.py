from os import system
import asyncio


async def say(text):
    return system(f'say {text}')


if __name__ == "__main__":
    asyncio.run(say('lo vamos a hacer por la oreja. ¿Por la oreja?'))
