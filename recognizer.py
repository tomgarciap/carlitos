#!/usr/bin/env python3
import queue
import sounddevice as sd
import vosk
import sys
import json
import sound_maker

def create_model(model_path):
    return vosk.Model(model_path)


def create_recognizer(model, samplerate, words) -> vosk.KaldiRecognizer:
    if len(words) != 0:
        return vosk.KaldiRecognizer(model, samplerate, str(words).replace("'", '"'))
    else:
        return vosk.KaldiRecognizer(model, samplerate)


def recognize_mic_stream(recognizerI: vosk.KaldiRecognizer,
                         samplerate,
                         device_index,
                         return_phrase=False):
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
            sound_maker.make_wake_sound()
            while True:
                mic_data = q.get()
                if recognizerI.AcceptWaveform(mic_data):
                    if return_phrase:
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
        print("Resetting general recognizer.. ")
        return phrase

