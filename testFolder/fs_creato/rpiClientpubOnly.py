from MyMQTT import *
from time import sleep
import paho.mqtt.client as PahoMQTT
import sys

#from pubsub import *
#from NEWNEWpubsub import *

class pubOnly():

    def __init__(self, clientID):
        self.client = MyMQTT(clientID, "test.mosquitto.org", 1883, self)
        self.clientID = clientID
        print(f"{self.clientID} created")
        self.client.start()
        self.client.mySubscribe("PoliTo/C4ES/#")

        topic = "PoliTo/C4ES/" + clientname + "/command"

        message = {"src" : clientname, "dest" : "pi0", "command" : "ls -la"}

        sleep(5)

        self.client.myPublish(topic, message)
        print(f"{self.clientID} publishing {message} to topic: {topic}")

        sleep(10)

    def notify(self, message, topic):
        if topic == f"PoliTo/C4ES/{self.clientID}/command":
            print("loopback")
            return



if __name__ == "__main__":

    clientname = str(sys.argv[1])

    publisher = pubOnly(clientname)
