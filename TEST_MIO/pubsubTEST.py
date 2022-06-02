from time import sleep
from MyMQTT import *
import paho.mqtt.client as PahoMQTT
import json
import time
import re

class pubsubTEST():

    def __init__(self):
        self.client = MyMQTT("TEST", "test.mosquitto.org", 1883, self)
        self.clientID = "TEST"
        print(f"{self.clientID} created")
        self.start()  
        

    def start (self):
        self.client.start()                

    def myPublish(self, topic, message):
        print(f"{self.clientID} publishing {message} to topic: {topic}")
        self.client.myPublish(topic, message)

    def notify(self, topic, message):
        pass
        

# cose da aggiungere: logica per cui se currTime - entryTime > threshold => riabilita il client

if __name__ == "__main__":
    
    test = pubsubTEST()

    sleep(2)

    topic = "PoliTo/C4ES/TEST/attack"
    message = {"hash_mismatch_in" : "test.txt", "untrust_topic" : "PoliTo/C4ES/TEST/attack"}
    test.myPublish(topic, message)