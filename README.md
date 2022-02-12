# Carlitos 
Carlitos is a experimental voice recognizing app created using [Vosk API](https://github.com/alphacep/vosk-api). It has two modes: calculator mode and general recognizer mode. 

On calculator mode, Carlitos listens to it's wake word and when it's awake it can translate some math calculation operations text into real mathematical operations, execute them and outputs the result on the terminal. If run in Mac it also uses the in built TTS to output the result in audio format. 

On general recognizer mode it just outputs recognized text in human speech in the terminal.

# If you want to try it out, here are the steps to do it:
Requirements:
```sh
conda 4.10.3
python 3.9
```

1 - Create a conda env out of the env.yml file.

2 - If you want to use the calculator mode download the only spanish language model available from [vosk docs](https://alphacephei.com/vosk/models). The calculator mode is only available in spanish. You can use any other model you'd like for the general recognizer.

3 - Activate the environement and run the help command for further instructions about audio input devices.

    python ui.py --help 

4 - Try out the two modes running these commands:

General recognizer: 

    python ui.py -am=reconocedor_general

Calculator mode: 

    python ui.py -am=wake_calculadora

5 - Add custom wake word with this command:

    python ui.py -am=wake_calculadora -ww="che sandra"

6 - Specify other models to use with this command

    python ui.py -am=reconocedor_general -m=model-en

# NOTE
Special thanks to [Nickolay V. Shmyrev](https://github.com/nshmyrev) for building Vosk and sharing it to the world. 

This is one of my pet projects and it emerges out of my passion for language models. If you have any questions about it or would like to contribute to this project feel free to send me an email: tomas.garcia.pineiro@gmail.com
