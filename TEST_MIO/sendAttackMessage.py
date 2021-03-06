from time import sleep
from MyMQTT import *

TESTclientID = "TEST"

class testpub():
    def __init__(self, clientID):
        self.client = MyMQTT(clientID, "test.mosquitto.org", 1883, self)
        self.clientID = clientID
        print(f"{self.clientID} created")
        self.start()
        self.subTopic = "PoliTo/C4ES/#"
        self.client.mySubscribe(self.subTopic)

    def start (self):
        self.client.start()  

    def myPublish(self, topic, message):
        print(f"{self.clientID} publishing {message} to topic: {topic}")
        self.client.myPublish(topic, message)

    def notify(self, topic, message):
        print("sono nella notify")

if __name__ == "__main__":

    test = testpub("TEST")
    sleep(2)
    topic = "PoliTo/C4ES/pippo"
    message = {"hash_mismatch_in" : "test.txt", "untrust_topic" : "PoliTo/C4ES/TEST/attack"}
    test.myPublish(topic, message)