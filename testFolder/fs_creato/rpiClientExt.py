from email import message
from MyMQTT import *
from time import sleep
import sys
import os
import hashlib
import subprocess
import time
import json

from pub import *

if __name__ == "__main__":

    clientname = str(sys.argv[1])

    rpi = pubsub(clientname)

    sleep(5)

    message = {"src" : clientname, "dest" : "TEST1", "command" : "ls"}

    rpi.myPublish("PoliTo/C4ES/" + clientname, message)