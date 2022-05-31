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
        self.unsubTopics = []
        self.unsubTopics.append(self.pubTopic) 
        self.client.mySubscribe(self.subTopic)
        

    def start (self):
        self.client.start()                

    def myPublish(self, topic, message):
        print(f"{self.clientID} publishing {message} to topic: {topic}")
        self.client.myPublish(topic, message)

    def notify(self, topic, message):
        if(topic in self.unsubTopics):
            pass        # i.e., ignore the message
        elif(topic == "PoliTo/C4ES/+/attack" and not topic in self.unsubTopics):
            fields = topic.split("/")
            fieldClientID = fields[2]
            newUnsubTopic = self.baseTopic + "/" + fieldClientID + "#"
            self.unsubTopics.append(newUnsubTopic)
            print(f"from now on {self.clientID} will not manage messages from {fieldClientID}") 
        else:
            print(f"{self.clientID} received {message} from {topic}")

    # def myUnsubscribe(self, topic):
    #     print(f"{self.clientID} unsubscribing from topic: {topic}")
    #     PahoMQTT..unsubscribe(topic)