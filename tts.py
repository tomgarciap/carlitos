from os import system


async def say(text):
    return system(f'say {text}')


if __name__ == "__main__":
    say('Texto de prueba, hola como estas la concha de dios, oh my god. soy una maquina')
