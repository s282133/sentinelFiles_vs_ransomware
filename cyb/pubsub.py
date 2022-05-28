from time import sleep
from MyMQTT import *
import paho.mqtt.client as PahoMQTT

class pubsub():

    def __init__(self, clientID):
        self.client = MyMQTT(clientID, "test.mosquitto.org", 1883, self)
        self.clientID = clientID
        print(f"{self.clientID} created")
        self.start()  
        self.baseTopic = "PoliTo/C4ES/"
        self.pubTopic = self.baseTopic + self.clientID
        self.subTopic = self.baseTopic + "#"
        self.unsubTopic = self.pubTopic 
        print(f"pubtopic: {self.pubTopic}       subtopic: {self.subTopic}       unsubtopic: {self.unsubTopic}")
        self.client.mySubscribe(self.subTopic)
        

    def start (self):
        self.client.start()                

    def myPublish(self, topic, message):
        print(f"{self.clientID} publishing {message} to topic: {topic}")
        self.client.myPublish(topic, message)

    def notify(self, topic, message):
        if(topic == self.unsubTopic):
            pass        # i.e., ignore the message
        else:
            print(f"{self.clientID} received {message} from topic: {topic}")

    # def myUnsubscribe(self, topic):
    #     print(f"{self.clientID} unsubscribing from topic: {topic}")
    #     PahoMQTT..unsubscribe(topic)