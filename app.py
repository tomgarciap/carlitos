# External modules
import os
import sounddevice as sd
import argparse
import asyncio
import json

# App modules
import wait_for_wake_word_state
import recognizer
import tts
import sound_maker
import spanish_numbers_understander
import calculadora

WAKE_WITH_SOUND = True


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])

parser.add_argument(
    '-am', '--assitant_mode', type=int,
    help='modo del asistente: 0 reconocedor general, 1 reconocer de wake word (default carlitos), '
         '2 modo asistente repetidor de frases',
    default=2)

parser.add_argument(
    '-ww', '--wake_word', type=str,
    help='la o las palabras para que el asistente de voz empiece a escuchar '
         'instrucciones',
    default='che carlitos')

parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-m', '--model_path', type=str, metavar='MODEL_PATH',
    help='Path to the model', default='model-es')
parser.add_argument(
    '-d', '--device_index', type=int_or_str,
    help='input device index (numeric ID or substring). Ejecutá este programa con el parametro --list-devices para '
         'ver la lista de dispositivos de audio de la maquina que estas usando', default=0)
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate', default=44100)

args = parser.parse_args(remaining)
if not os.path.exists(args.model_path):
    print("No se encontró el modelo, descargate el unico en español de aca https://alphacephei.com/vosk/models")
    print("Y unzipealo en esta misma carpeta y cambiale el nombre a model-es.")
    parser.exit(0)

exitParameter = 0
if args.assitant_mode == 0:
    print("corriendo el reconocedor general")
    model1 = recognizer.create_model(args.model_path)
    exitParameter = recognizer.recognize_mic_stream(recognizer.create_recognizer(model1, args.samplerate),
                                                    args.samplerate,
                                                    args.device_index)

if args.assitant_mode == 1:
    print("corriendo el reconocedor de wake word")
    model1 = recognizer.create_model(args.model_path)
    exitParameter = recognizer.recognize_mic_stream(
        recognizer.create_recognizer(model1, args.samplerate, args.wake_word),
        args.samplerate,
        args.device_index)
model = recognizer.create_model(args.model_path)
recognizers = {
    "wake_word": recognizer.create_recognizer(model, args.samplerate, [args.wake_word]),
    "general": recognizer.create_recognizer(model, args.samplerate, []),
    "calculator_mode": recognizer.create_recognizer(model, args.samplerate,
                                                    spanish_numbers_understander.get_domain_dictionary())
}


async def calculator_use_case():
    phrase = recognizer.recognize_mic_stream(recognizers["calculator_mode"],
                                             args.samplerate,
                                             args.device_index,
                                             return_phrase=True)
    integers_in_phrase = spanish_numbers_understander.extract_integers_from_phrase(phrase)
    print(f'Enteros de la frase {str(integers_in_phrase)}')
    if len(integers_in_phrase) == 0:
        return
    if len(integers_in_phrase) == 1:
        return integers_in_phrase[0]
    operators_in_phrase = spanish_numbers_understander.extract_mathematical_operators(phrase)
    operation_elements = [integers_in_phrase.pop(0)]
    for index in range(len(operators_in_phrase)):
        operation_elements.append(operators_in_phrase[index])
        operation_elements.append(integers_in_phrase[index])
    result = calculadora.calculate_operation_result(operation_elements)
    print(result)
    await tts.say(result)


def general_use_case():
    human_phrase = recognizer.recognize_mic_stream(recognizers["general"],
                                                   args.samplerate,
                                                   args.device_index,
                                                   True)
    print(f'la frase humana {str(human_phrase)}')
    print(f'numeros de la frase {str(spanish_numbers_understander.extract_integers_from_phrase(human_phrase))}')


def wake_word_use_case():
    wait_for_wake_word_state.enter_state(recognizers["wake_word"],
                                         args.wake_word,
                                         args.device_index,
                                         args.samplerate)


async def wake_and_calculate():
    wake_word_use_case()
    await calculator_use_case()


async def app():
    print("corriendo asistente")
    while True:
        try:
            await wake_and_calculate()
        except KeyboardInterrupt:
            print("\nExiting...")
            break
    exit()


if args.assitant_mode == 2:
    asyncio.run(app())

parser.exit(exitParameter)
