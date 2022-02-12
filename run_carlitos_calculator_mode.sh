eval "$(conda shell.bash hook)"
conda activate vosk
if [ -z "$1" ]
then
   echo "Ingresar wake word. Ejemplo: bash run_carlitos_calculator_mode.sh 'che carlitos'";
   exit
fi
python ui.py -am=wake_calculadora --wake_word="$1"