from time import sleep
from MyMQTT import *

TESTclientID = "TEST"

class testpub():
    def __init__(self):
        self.client = MyMQTT(TESTclientID, "test.mosquitto.org", 1883, self)
        self.clientID = TESTclientID
        print(f"{self.clientID} created")
        self.start()

    def start (self):
        self.client.start()  

    def myPublish(self, topic, message):
        print(f"{self.clientID} publishing {message} to topic: {topic}")
        self.client.myPublish(topic, message)


if __name__ == "__main__":

    test = testpub()
    sleep(10)
    message = {"hash_mismatch_in" : "test.txt", "untrust_topic" : "PoliTo/C4ES/TEST/attack"}
    test.myPublish("PoliTo/C4ES/TEST/attack", message)