# App modules
import wait_for_wake_word_state
import general_recognizer_state
import vosk_builders
import spanish_numbers_understander

WAKE_WITH_SOUND = True


class App:
    def __init__(self):
        pass

    async def run(self, wake_word, device_index, samplerate, app_mode, model_path):
        model = vosk_builders.create_model(model_path)
        while True:
            try:
                if app_mode == "reconocedor_general":
                    await general_recognizer_state.enter_state(vosk_builders.create_recognizer(model, samplerate, []), 
                    samplerate, 
                    device_index)
                elif app_mode == "wake_calculadora":
                    print("Listening for wake word: " + wake_word)
                    recognizers = {
                        "wake_mode": vosk_builders.create_recognizer(model, samplerate, [wake_word]),
                        "calculator_mode": vosk_builders.create_recognizer(model, samplerate, spanish_numbers_understander.get_domain_dictionary())
                    }
                    await wait_for_wake_word_state.enter_state(recognizers,
                                                               wake_word,
                                                               device_index,
                                                               samplerate)
                else:
                    raise Exception("Modo de asistente no reconocido..")
            except KeyboardInterrupt:
                break
        print("Ending carlitos..")
        exit()
