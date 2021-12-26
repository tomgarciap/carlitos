#!/usr/bin/env python3
from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import json

def reconocedor(file_path):
    SetLogLevel(0)
    wf = wave.open(file_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)
    print(wf.getframerate())
    model = Model("model-es")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        rec.AcceptWaveform(data)
    result = rec.FinalResult()
    result_json = json.loads(result)
    result_text = result_json["text"]
    print(f"Resultado para audio: {file_path} es {result_text}")

if __name__ == "__main__":
    reconocedor("recorded_sounds/1.wav")
    reconocedor("recorded_sounds/2.wav")
    reconocedor("recorded_sounds/3.wav")
