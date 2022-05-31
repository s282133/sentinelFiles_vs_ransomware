#!/bin/bash

python3 -B ./initializeFS.py

python3 -B ./createProductionFiles.py

python3 -B ./createSentinels.py
