from pubsub import *
from MyMQTT import *
from time import sleep
import sys

if __name__ == "__main__":

    clientname = str(sys.argv[1])

    rpi = pubsub(clientname)

    for i in range(0,10):
        message = f"hi_from_{clientname}"
        rpi.myPublish(rpi.pubTopic, message)
        sleep(10)