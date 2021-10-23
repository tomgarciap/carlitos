import os
import sounddevice as sd
import argparse
import wait_for_wake_word_state
import recognizer


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
         '2 modo sleep con deteccion de wake word',
    default=0)

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
    exitParameter = recognizer.recognize_mic_stream(args.model_path,
                                                    args.samplerate,
                                                    args.device_index)

if args.assitant_mode == 1:
    print("corriendo el reconocedor de wake word")
    exitParameter = recognizer.recognize_mic_stream(args.model_path,
                                                    args.samplerate,
                                                    args.device_index,
                                                    args.wake_word)
if args.assitant_mode == 2:
    print("corriendo asistente")
    exitParameter = wait_for_wake_word_state.enter_state(args.model_path,
                                                         args.wake_word,
                                                         args.device_index,
                                                         args.samplerate)
    humanPhrase = recognizer.recognize_mic_stream(args.model_path,
                                                  args.samplerate,
                                                  args.device_index)
    print(f'la frase humana {humanPhrase}')
parser.exit(exitParameter)
