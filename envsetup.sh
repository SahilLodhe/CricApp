#!/bin/bash

if [ -d "env" ] 
then
    echo "Python virtual environment exists." 
else
    python3 -m venv env
fi
# source .env/bin/activate
# source env/bin/bash/activate
source env/bin/Activate


pip3 install -r requirements1.txt
pip3 install -r requrements.txt

if [ -d "logs" ] 
then
    echo "Log folder exists." 
else
    mkdir logs
    touch logs/error.log logs/access.log
fi

sudo chmod -R 777 logs
