#!/usr/bin/env python3
import sounddevice as sd
import vosk


def create_model(model_path) -> vosk.Model:
    return vosk.Model(model_path)


def create_recognizer(model, samplerate, words) -> vosk.KaldiRecognizer:
    if len(words) != 0:
        return vosk.KaldiRecognizer(model, samplerate, str(words).replace("'", '"'))
    else:
        return vosk.KaldiRecognizer(model, samplerate)
