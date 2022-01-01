eval "$(conda shell.bash hook)"
conda activate vosk
if [ -z "$1" ]
then
   echo "Ingresar wake word";
   exit
fi
python ui.py -am=carlitos_premium --wake_word="$1"