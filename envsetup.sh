#!/bin/bash

if[-d "env"]
then
echo "Python virtual env exist"
else
    python3 -m venv env
fi

echo $PWD
source env/bin/activate

pip3 install -r requirements.txt

if[-d "logs"]
then
    echo "Log folder exists exist"
else
    mkdir logs
    touch logs/error.log logs/access.log
fi

