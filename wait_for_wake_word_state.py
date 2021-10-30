from threading import Thread
import queue
import sounddevice as sd
import sys
import vosk 


class WakeWordAwaitingState(Thread):

    def __init__(
            self,
            recognizerI: vosk.KaldiRecognizer,
            device_index,
            samplerate,
            wake_word):
        super(WakeWordAwaitingState, self).__init__()
        self._wake_word = wake_word
        self._recognizerI: vosk.KaldiRecognizer = recognizerI
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

            with sd.RawInputStream(samplerate=self._samplerate, blocksize=8000, device=self._device_index,
                                   dtype='int16',
                                   channels=1, callback=callback):
                while True:
                    data = q.get()
                    if self._recognizerI.AcceptWaveform(data):
                        print(self._recognizerI.Result())
                        rec_result = self._recognizerI.Result()
                        if self._wake_word in rec_result:
                            return
                    else:
                        print(self._recognizerI.PartialResult())
                        rec_result = self._recognizerI.PartialResult()
                        if self._wake_word in rec_result:
                            return
        finally:
            # call delete() method on all instances?
            self._recognizerI.Reset()
            print('Fiuff finally..')


def enter_state(recognizerI, wake_word, device_index, samplerate):
    print("Running wake word thread")
    WakeWordAwaitingState(recognizerI=recognizerI,
                          wake_word=wake_word,
                          device_index=device_index,
                          samplerate=samplerate).run()
    print("Ending wake word thread")
    return 0
