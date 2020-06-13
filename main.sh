#!/bin/sh

source ./env/bin/activate ||
(
    python3 -m venv env
    source ./env/bin/activate
    pip3 install -r requirements.txt
)


while read line; do
    (
    echo "doing ${line%%:*}"
    python main.py "${line#*:}" > output/"${line%%:*}".csv && 
    echo "done ${line%%:*}"
    ) &
done < unis.yml
wait


deactivate