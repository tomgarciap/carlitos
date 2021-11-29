from threading import Thread
import queue
import sounddevice as sd
import sys
import contador_de_chistes
import json
import spanish_numbers_understander
import calculadora
import tts
import sound_maker


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

    async def run(self):
        q = queue.Queue()

        def callback(indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            if status:
                print(status, file=sys.stderr)
            q.put(bytes(indata))

        try:
            device_info = sd.query_devices(self._device_index, 'input')
            print(device_info)
            # self._samplerate = int(device_info['default_samplerate'])

            with sd.RawInputStream(samplerate=self._samplerate, blocksize=8000, device=self._device_index,
                                   dtype='int16',
                                   channels=1, callback=callback):
                print("Enter wake mode")
                recognizer_status = "wake_mode"
                while True:
                    data = q.get()
                    if recognizer_status == "wake_mode":
                        if self.recognizers["wake_mode"].AcceptWaveform(data):
                            print(self.recognizers["wake_mode"].Result())
                            rec_result = self.recognizers["wake_mode"].Result()
                            if self._wake_word in rec_result:
                                run_wake_sound_thread()
                                recognizer_status = "calculator_mode"
                                print("Enter calculator mode")
                                self.recognizers["calculator_mode"].Reset()
                        else:
                            print(self.recognizers["wake_mode"].PartialResult())
                            rec_result = self.recognizers["wake_mode"].PartialResult()
                            if self._wake_word in rec_result:
                                run_wake_sound_thread()
                                recognizer_status = "calculator_mode"
                                print("Enter calculator mode")
                                self.recognizers["calculator_mode"].Reset()
                    elif recognizer_status == "calculator_mode":
                        # copy_for_yayo = bytes(bytearray(data))
                        # if self.recognizers["chiste_yayo_mode"].AcceptWaveform(copy_for_yayo):
                        #     phrase = json.loads(self.recognizers["calculator_mode"].Result())["text"]
                        #     if CHISTE_YAYO in phrase:
                        #         recognizer_status = "wake_mode"
                        #         contador_de_chistes.contar_chiste()
                        #         self.recognizers["wake_mode"].Reset()
                        #         print("Enter wake mode")
                        #         return
                        if self.recognizers["calculator_mode"].AcceptWaveform(data):
                            phrase = json.loads(self.recognizers["calculator_mode"].Result())["text"]
                            recognizer_status = "wake_mode"
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
                        else:
                            partial_result = self.recognizers["calculator_mode"].PartialResult()
                            print(partial_result)
        finally:
            for key, value in self.recognizers.items():
                value.Reset()
            print('Resetting wake word recognizer..')


async def enter_state(recognizers, wake_word, device_index, samplerate):
    print("Running wake word thread")
    await WakeWordAwaitingState(recognizers=recognizers,
                                wake_word=wake_word,
                                device_index=device_index,
                                samplerate=samplerate).run()
    print("Ending wake word thread")
