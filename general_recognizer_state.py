from threading import Thread
import queue
import sounddevice as sd
import json
import sys
import vosk 

class GeneralRecognizerState(Thread):
    def __init__(
            self,
            recognizer: vosk.KaldiRecognizer,
            device_index: int,
            samplerate: int):
        super(GeneralRecognizerState, self).__init__()
        self.recognizer = recognizer
        self.device_index = device_index
        self.samplerate = samplerate

    async def run(self):
        print("thread run")
        q = queue.Queue()
        def callback(indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            if status:
                print(status, file=sys.stderr)
            q.put(bytes(indata))

        try:
            if self.samplerate is None:
                device_info = sd.query_devices(self.device_index, 'input')
                self.samplerate = int(device_info['default_samplerate'])
            blocksizex = 8000
            print("Running microphone with: Sample rate -> " + str(self.samplerate)
                + " Block Size -> " + str(blocksizex) + " Device index -> " + str(self.device_index))
            with sd.RawInputStream(samplerate=self.samplerate, blocksize=blocksizex, device=self.device_index,
                                dtype='int16', channels=1, callback=callback):
                print('#' * 80)
                print('Grabando.. Apretar CTRL + C para salir de la app.')
                print('#' * 80)
                while True:
                    mic_data = q.get()
                    if self.recognizer.AcceptWaveform(mic_data):
                        phrase_object = json.loads(self.recognizer.FinalResult())
                        print("Final Result: " + phrase_object["text"])
                    else:
                        partial_result = json.loads(self.recognizer.PartialResult())["partial"]
                        print("Partial result: " + partial_result)
        finally:
            self.recognizer.Reset()

async def enter_state(recognizer, samplerate, device_index):
    print("Running general recognizer thread...")
    await GeneralRecognizerState(recognizer=recognizer,
                                device_index=device_index,
                                samplerate=samplerate).run()