#!/usr/bin/env python3
import queue
import sounddevice as sd
import vosk
import sys
import json


def string_to_array_like_string(argument_value):
    return f'["{argument_value}"]'


def create_model(model_path):
    return vosk.Model(model_path)


def create_recognizer(model, samplerate, word=None) -> vosk.KaldiRecognizer:
    if word is not None:
        return vosk.KaldiRecognizer(model, samplerate, string_to_array_like_string(word))
    else:
        return vosk.KaldiRecognizer(model, samplerate)


def recognize_mic_stream(recognizerI: vosk.KaldiRecognizer,
                         samplerate,
                         device_index,
                         only_one=False):
    q = queue.Queue()

    def callback(indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        q.put(bytes(indata))

    try:
        if samplerate is None:
            device_info = sd.query_devices(device_index, 'input')
            samplerate = int(device_info['default_samplerate'])
        phrase = ""
        with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device_index, dtype='int16',
                               channels=1, callback=callback):
            print('#' * 80)
            print('Grabando.. Tirar CTRL + C para salir de la app.')
            print('#' * 80)

            while True:
                data = q.get()
                if recognizerI.AcceptWaveform(data):
                    if only_one:
                        phrase_object = json.loads(recognizerI.Result())
                        if phrase_object["text"] == '':
                            continue
                        else:
                            phrase = phrase_object["text"]
                            return
                    print(recognizerI.Result())
                else:
                    print(recognizerI.PartialResult())
                
    except Exception as e:
        return type(e).__name__ + ': ' + str(e)
    finally:
        recognizerI.Reset()
        return phrase

