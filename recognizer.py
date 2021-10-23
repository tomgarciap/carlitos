#!/usr/bin/env python3
import queue
import sounddevice as sd
import vosk
import sys


def recognize_mic_stream(model_path,
                         samplerate,
                         device_index,
                         file_name,
                         wake_word):
    q = queue.Queue()

    def callback(indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        q.put(bytes(indata))

    try:
        if samplerate is None:
            device_info = sd.query_devices(device_index, 'input')
            # soundfile expects an int, sounddevice provides a float:
            # TODO: Acá se debería validar que el input del micrófono sea de 16k HZ de frame rate
            #   O básicamente el mismo que el del modelo. Si el modelo no cambia, esto podría ser una
            #   contante de la apliacion
            samplerate = int(device_info['default_samplerate'])

        model = vosk.Model(model_path)

        if file_name:
            dump_fn = open(file_name, "wb")
        else:
            dump_fn = None

        with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device_index, dtype='int16',
                               channels=1, callback=callback):
            print('#' * 80)
            print('Ejecutá el comando Ctrl+C para frenar la grabación')
            print('#' * 80)

            rec = vosk.KaldiRecognizer(model, samplerate, wake_word)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    print(rec.Result())
                else:
                    print(rec.PartialResult())
                if dump_fn is not None:
                    dump_fn.write(data)

    except KeyboardInterrupt:
        print('\nDone')
        return 0
    except Exception as e:
        return type(e).__name__ + ': ' + str(e)
