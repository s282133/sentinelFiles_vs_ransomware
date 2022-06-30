#!/bin/bash

python3 -B ./initializeFS.py

python3 -B ./createProductionFiles.py

python3 -B ./createSentinels.py

clear

chmod 500 ./createProductionFiles.py
chmod 500 ./createSentinels.py
chmod 500 ./initializeFS.py
chmod 500 ./MyMQTT.py
chmod 500 ./NEWNEWpubsub.py
chmod 500 ./pubsub.py
chmod 500 ./rpiClient.py
chmod 500 ./rpiClientpubOnly.py
chmod 500 ./script.sh
chmod 500 ./script2.sh

python3 -B ./rpiClient.py $USER
