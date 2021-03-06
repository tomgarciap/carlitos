#!usr/bin/env python
import pyaudio
import wave
import copy

chunk = 1024


def make_wake_sound():
    f = wave.open(r"downloaded_sounds/hard-tone-modif-1.wav", "rb")
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    data = f.readframes(chunk)
    count = 0
    while data:
        stream.write(data)
        data = f.readframes(chunk)
    print(count)
    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == '__main__':
    make_wake_sound()
