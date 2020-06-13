#!/bin/sh

source ./env/bin/activate ||
(
    python -m venv env
    source ./env/bin/activate
    pip install -r requirements.txt
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