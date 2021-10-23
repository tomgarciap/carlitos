import os
import sounddevice as sd
import argparse
import recognizer


def int_or_str(text):
    """Helper function 1 for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


def string_to_array_like_string(argument_value):
    """Helper function 2 for argument parsing."""
    return f'["{argument_value}"]'


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
    '-ww', '--wake_word', type=string_to_array_like_string,
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
         'ver la lista de dispositivos de audio de la maquina que estas usando')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')

args = parser.parse_args(remaining)
if not os.path.exists(args.model_path):
    print("No se encontró el modelo, descargate el unico en español de aca https://alphacephei.com/vosk/models")
    print("Y unzipealo en esta misma carpeta y cambiale el nombre a model-es.")
    parser.exit(0)

exitParameter = recognizer.recognize_mic_stream(args.model_path,
                                                args.samplerate,
                                                args.device_index,
                                                args.filename,
                                                args.wake_word)
parser.exit(exitParameter)
