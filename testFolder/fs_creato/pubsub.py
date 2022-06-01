from time import sleep
from MyMQTT import *
import paho.mqtt.client as PahoMQTT
import json
import time
import re

pattern = re.compile(r'PoliTo/C4ES/.+/attack')

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
        self.blacklist = open("blacklist.json", "w")
        self.blacklist.close()
        self.banTime = 10 * 60
        

    def start (self):
        self.client.start()                

    def myPublish(self, topic, message):
        print(f"{self.clientID} publishing {message} to topic: {topic}")
        self.client.myPublish(topic, message)

    def notify(self, topic, message):
        if(topic in self.unsubTopics or topic == f"PoliTo/C4ES/{self.clientID}/attack"):
            pass        # i.e., ignore the message
        elif(bool(pattern.match(str(topic))) and not topic in self.unsubTopics):
            fields = topic.split("/")
            fieldClientID = fields[2]
            newUnsubTopic = self.baseTopic + fieldClientID + "/#"
            print("[DEBUG]  " + str(newUnsubTopic))
            d = json.loads(message)
            altered_file = d["hash_mismatch_in"]
            untrusted_topic = d["untrust_topic"]
            self.currBlackListFile = open("blacklist.json", "r")
            self.currBlackList = json.load(self.currBlackListFile)
            self.currBlackListFile.close()
            self.currBlackList.append({"clientID" : fieldClientID, "banTime" : time.time(), "altered_file" : altered_file, "untrusted_topic" : untrusted_topic})
            self.newBlackListFile = open("blacklist.json", "w")
            json.dump(self.currBlackList, self.newBlackListFile)
            print(f"In {fieldClientID} there is a wrong hash at {altered_file}, I'm gonna unsubscribe from {untrusted_topic} - unsubrscribe finto !")
            # END da testare !
        else:
            print(f"{self.clientID} received {message} from {topic}")

# cose da aggiungere: logica per cui se currTime - entryTime > threshold => riabilita il client