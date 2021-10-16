#!/bin/bash
rm ./static/logs/*.log

if [ "$1" == "" ]
then
  echo "Usage: ./run.sh <n_processes>"
  exit
fi

echo "Executing $1 processes in background..."
processes_arr=()
for (( i=0; i<=$1-1; i++ ))
do
   echo "Staring process $i."
   gnome-terminal --title="Instance $i" --window --hide-menubar -- python3 main.py $1 $i
   echo $!
done
