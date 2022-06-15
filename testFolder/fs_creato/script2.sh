#!/bin/bash

python3 -B ./initializeFS.py

python3 -B ./createProductionFiles.py

python3 -B ./createSentinels.py

clear

python3 -B ./rpiClient.py pi0
