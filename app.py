# App modules
import wait_for_wake_word_state
import recognizer
import tts
import sound_maker
import spanish_numbers_understander
import calculadora

WAKE_WITH_SOUND = True


class App:
    def __init__(self):
        pass

    async def calculator_use_case(self, calculator_recognizer, samplerate, device_index):
        phrase = recognizer.recognize_mic_stream(calculator_recognizer,
                                                 samplerate,
                                                 device_index,
                                                 return_phrase=True)
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

    def general_use_case(self, samplerate, device_index, general_recognizer):
        human_phrase = recognizer.recognize_mic_stream(general_recognizer,
                                                       samplerate,
                                                       device_index,
                                                       True)
        print(f'la frase humana {str(human_phrase)}')
        print(f'numeros de la frase {str(spanish_numbers_understander.extract_integers_from_phrase(human_phrase))}')

    def wake_word_use_case(self, wake_word, device_index, samplerate, wake_word_recognizer):
        wait_for_wake_word_state.enter_state(wake_word_recognizer,
                                             wake_word,
                                             device_index,
                                             samplerate)

    async def wake_and_calculate_use_case(self, wake_word, device_index, samplerate, wake_word_recognizer,
                                          calculator_recognizer):
        self.wake_word_use_case(wake_word, device_index, samplerate, wake_word_recognizer)
        await self.calculator_use_case(calculator_recognizer, samplerate, device_index)

    async def run(self, wake_word, device_index, samplerate, app_mode, model_path):
        print("corriendo asistente")
        model = recognizer.create_model(model_path)
        recognizers = {
            "wake_mode": recognizer.create_recognizer(model, samplerate, [wake_word]),
            "general": recognizer.create_recognizer(model, samplerate, []),
            "calculator_mode": recognizer.create_recognizer(model, samplerate, spanish_numbers_understander.get_domain_dictionary())
        }
        while True:
            try:
                if app_mode == "carlitos":
                    await self.wake_and_calculate_use_case(wake_word, device_index, samplerate,
                                                           recognizers["wake_word"],
                                                           recognizers["calculator"])
                elif app_mode == "reconocedor_general":
                    await self.general_use_case(samplerate, device_index, recognizers["general"])
                elif app_mode == "carlitos_premium":
                    await wait_for_wake_word_state.enter_state(recognizers,
                                                               wake_word,
                                                               device_index,
                                                               samplerate)
                else:
                    raise Exception("Modo de asistente no reconocido")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
        exit()
