import argparse
import sounddevice as sd
import os
import asyncio
from app import App


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list_devices', action='store_true',
    help='Mostrar lista de dispositivos de audio del sistema') 
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])

parser.add_argument(
    '-am', '--assitant_mode', type=str,
    help='Ingresar: wake_calculadora o reconocedor_general',
    default="wake_calculadora")

parser.add_argument(
    '-ww', '--wake_word', type=str,
    help='La o las palabras para que el asistente de voz empiece a escuchar '
         'instrucciones en el modo wake calculadora. El default es: che carlitos',
    default='che carlitos')

parser.add_argument(
    '-m', '--model_path', type=str, metavar='MODEL_PATH',
    help='Path al modelo sin backslash, ejemplo: model-es', default='model-es')

parser.add_argument(
    '-d', '--device_index', type=int_or_str,
    help='Ejecutá este programa con el parametro --list-devices para '
         'ver la lista de dispositivos de audio de la maquina que estas usando.' 
         'Ingresar el index del microfono a utilizar. El default es cero', default=0)

parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate', default=44100)

args = parser.parse_args(remaining)
if not os.path.exists(args.model_path):
    print("No se encontró el modelo, descargate el único en español de acá https://alphacephei.com/vosk/models")
    print("Y unzipealo en el root de este proyecto en una carpeta.")
    parser.exit(0)

if args.assitant_mode not in ["wake_calculadora", "reconocedor_general"]:
    print("El modo debe ser wake_calculadora o reconocedor_general")
    parser.exit(0)
app = App()
asyncio.run(app.run(args.wake_word, args.device_index, args.samplerate, args.assitant_mode, args.model_path))
