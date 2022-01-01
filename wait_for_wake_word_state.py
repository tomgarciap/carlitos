from threading import Thread
import queue
import sounddevice as sd
import sys
import contador_de_chistes
import time
import json
import spanish_numbers_understander
import calculadora
import tts
import sound_maker
from datetime import datetime


def run_wake_sound_thread():
    thread = Thread(target=sound_maker.make_wake_sound)
    thread.start()


CHISTE_YAYO = "chiste yayo"


class WakeWordAwaitingState(Thread):

    def __init__(
            self,
            recognizers: dict,
            device_index: int,
            samplerate: int,
            wake_word: str):
        super(WakeWordAwaitingState, self).__init__()
        self._wake_word = wake_word
        self.recognizers = recognizers
        self._device_index = device_index
        self._samplerate = samplerate

    async def execute_command(self, phrase):
        print(f'Frase: {phrase}')
        integers_in_phrase = spanish_numbers_understander.extract_integers_from_phrase(phrase)
        print(f'Enteros de la frase {str(integers_in_phrase)}')
        if len(integers_in_phrase) == 0:
            return
        if len(integers_in_phrase) == 1:
            return integers_in_phrase[0]
        operators_in_phrase = spanish_numbers_understander.extract_mathematical_operators(phrase)
        operation_elements = [integers_in_phrase.pop(0)]
        for index in range(len(operators_in_phrase)):
            operation_elements.append(operators_in_phrase[index])
            operation_elements.append(integers_in_phrase[index])
        result = calculadora.calculate_operation_result(operation_elements)
        print(result)
        await tts.say(result)
        self.recognizers["wake_mode"].Reset()
        print("Enter wake mode")

    async def run(self):
        q = queue.Queue()

        def callback(indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            if status:
                print(status)
            q.put(bytes(indata))

        try:
            device_info = sd.query_devices(self._device_index, 'input')
            print(device_info)
            # self._samplerate = int(device_info['default_samplerate'])
            milliseconds_without_words = 0
            start_epoch = int(time.time() * 100)
            collected_calculator_phrases = list()
            print("Booting system...")
            time.sleep(5)
            blocksizex = 8000
            print("Running microphone with: Sample rate -> " + self._samplerate
                  + " Block Size -> " + blocksizex + " Device index -> " + self._device_index)
            with sd.RawInputStream(samplerate=self._samplerate, blocksize=blocksizex, device=self._device_index,
                                   dtype='int16', channels=1, callback=callback):
                recognizer_status = "wake_mode"
                print("Entering wake mode..")
                while True:
                    data = q.get()
                    if recognizer_status == "wake_mode":
                        if self.recognizers["wake_mode"].AcceptWaveform(data):
                            rec_result = self.recognizers["wake_mode"].Result()
                            if self._wake_word in rec_result:
                                run_wake_sound_thread()
                                recognizer_status = "calculator_mode"
                                self.recognizers["wake_mode"].Reset()
                                print("Enter calculator mode..")
                        else:
                            rec_result = self.recognizers["wake_mode"].PartialResult()
                            if self._wake_word in rec_result:
                                run_wake_sound_thread()
                                recognizer_status = "calculator_mode"
                                self.recognizers["wake_mode"].Reset()
                                print("Enter calculator mode..")
                    elif recognizer_status == "calculator_mode":
                        no_words = True
                        if self.recognizers["calculator_mode"].AcceptWaveform(data):
                            phrase = json.loads(self.recognizers["calculator_mode"].Result())["text"]
                            collected_calculator_phrases.append(phrase)
                            print("Result: " + phrase)
                            if phrase == "":
                                no_words = True
                            if milliseconds_without_words > 3000:
                                final_phrase = json.loads(self.recognizers["calculator_mode"].FinalResult())["text"]
                                if final_phrase != "":
                                    await self.execute_command(final_phrase)
                                else:
                                    milliseconds_without_words = 0
                                    recognizer_status = "wake_mode"
                                    self.recognizers["calculator_mode"].Reset()
                        else:
                            partial_result = json.loads(self.recognizers["calculator_mode"].PartialResult())["partial"]
                            if partial_result == "":
                                no_words = True
                            print("Partial result: " + partial_result)
                        if no_words:
                            milliseconds_without_words += (int(time.time()) * 100) - start_epoch
                        #print(milliseconds_without_words)

        finally:
            for key, value in self.recognizers.items():
                value.Reset()
            print('Resetting all recoginzers.')


async def enter_state(recognizers, wake_word, device_index, samplerate):
    print("Running wake word thread")
    await WakeWordAwaitingState(recognizers=recognizers,
                                wake_word=wake_word,
                                device_index=device_index,
                                samplerate=samplerate).run()
    print("Ending wake word thread")
