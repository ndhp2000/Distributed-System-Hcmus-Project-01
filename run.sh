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
   python3 main.py $1 $i &
   processes_arr+=($!)
done

echo "Press control+C to stops."
for (( i=0; i<=$1-1; i++ ))
do
  wait ${processes_arr[i]}
done


#python3 main.py $1 0 &
#pid1=$!
#python3 main.py $1 1 &
#pid2=$!
#echo "Executed all process in background..."
#
