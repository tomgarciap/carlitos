#!/usr/bin/env python3
import queue
import sounddevice as sd
import vosk
import sys
import os


def recognize_mic_stream(model_path,
                         samplerate,
                         device_index,
                         wake_word=None):
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

        model = vosk.Model(model_path)
        with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device_index, dtype='int16',
                               channels=1, callback=callback):
            print('#' * 80)
            print('Ejecutá el comando Ctrl+C para frenar la grabación')
            print('#' * 80)
            if wake_word:
                rec = vosk.KaldiRecognizer(model, samplerate, wake_word)
            else:
                rec = vosk.KaldiRecognizer(model, samplerate)

            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    return rec.Result()
                else:
                    print(rec.PartialResult())

    except KeyboardInterrupt:
        print('\nDone')
        return 0
    except Exception as e:
        return type(e).__name__ + ': ' + str(e)
