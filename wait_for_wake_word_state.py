from threading import Thread
import queue
import sounddevice as sd
import vosk
import sys


def string_to_array_like_string(argument_value):
    """Helper function 2 for argument parsing."""
    return f'["{argument_value}"]'


class WakeWordAwaitingState(Thread):

    def __init__(
            self,
            model_path,
            wake_word,
            device_index,
            samplerate):
        super(WakeWordAwaitingState, self).__init__()

        self._model_path = model_path
        self._wake_word = wake_word
        self._device_index = device_index
        self._samplerate = samplerate

    def run(self):
        q = queue.Queue()

        def callback(indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            if status:
                print(status, file=sys.stderr)
            q.put(bytes(indata))

        try:
            if self._samplerate is None:
                device_info = sd.query_devices(self._device_index, 'input')
                self._samplerate = int(device_info['default_samplerate'])

            model = vosk.Model(self._model_path)
            with sd.RawInputStream(samplerate=self._samplerate, blocksize=8000, device=self._device_index, dtype='int16',
                                   channels=1, callback=callback):
                print('#' * 80)
                print('Ejecutá el comando Ctrl+C para frenar la grabación')
                print('#' * 80)

                rec = vosk.KaldiRecognizer(model, self._samplerate, string_to_array_like_string(self._wake_word))
                while True:
                    data = q.get()
                    if rec.AcceptWaveform(data):
                        rec_result = rec.Result()
                        if self._wake_word in rec_result:
                            return
                    else:
                        rec_result = rec.PartialResult()
                        if self._wake_word in rec_result:
                            return
        except KeyboardInterrupt:
            print('Stopping ...')
        finally:
            # call delete() method on all instances?
            print('Fiuff finally..')


def enter_state(model_path, wake_word, device_index, samplerate):
    WakeWordAwaitingState(model_path=model_path,
                                              wake_word=wake_word,
                                              device_index=device_index,
                                              samplerate=samplerate).run()
    print("Wake mode ON")
    return 0
