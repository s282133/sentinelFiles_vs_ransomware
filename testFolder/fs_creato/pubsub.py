from time import sleep
from MyMQTT import *
import paho.mqtt.client as PahoMQTT
import json
import time
import re
import subprocess
import sys, os

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
        self.blacklist.write('{"ban_list":[]}')
        self.blacklist.close()
        self.banTime = 1 * 60
        

    def start (self):
        self.client.start()                

    def myPublish(self, topic, message):
        print(f"{self.clientID} publishing {message} to topic: {topic}")
        self.client.myPublish(topic, message)

    def notify(self, topic, message):
        #print("sono nella notify")
        blackListFILE = open("blacklist.json", "r")
        blackList = json.load(blackListFILE)
        blackListFILE.close()
        banList = blackList["ban_list"]
        untrusted_topics = []
        for client in banList:
            untrusted_topics.append(client["untrust_topic"])

        if(topic in untrusted_topics or topic == f"PoliTo/C4ES/{self.clientID}/attack"):
            #print("sono nella notify - ignored message")
            pass        # i.e., ignore the message
        elif(bool(pattern.match(str(topic))) and not topic in untrusted_topics):
            #print("sono nella notify - attack message")
            fields = topic.split("/")
            fieldClientID = fields[2]
            newUnsubTopic = self.baseTopic + fieldClientID + "/#"
            print("[DEBUG]  " + str(newUnsubTopic))
            d = json.loads(message)
            altered_file = d["hash_mismatch_in"]
            untrusted_topic = d["untrust_topic"]
            self.currBlackListFile = open("blacklist.json", "r")
            self.currBlackList = json.load(self.currBlackListFile)      # dictionary
            self.ban_list = self.currBlackList["ban_list"]              # list
            print(f"old ban_list: {self.ban_list}")
            # self.currBlackListFile.close()
            ban_time = round(time.time())
            banned_until = ban_time + self.banTime
            self.ban_list.append({"clientID" : fieldClientID, "banned_at" : ban_time, "banned_until" : banned_until, "altered_file" : altered_file, "untrusted_topic" : untrusted_topic})
            print(f"new ban_list : {self.ban_list}")
            self.currBlackList["ban_list"] = self.ban_list
            self.newBlackListFile = open("blacklist.json", "w")
            print(f"self.updatedBlackList : {self.currBlackList}")
            json.dump(self.currBlackList, self.newBlackListFile, indent=4)
            self.newBlackListFile.close()
            self.currBlackListFile.close()
            print(f"In {fieldClientID} there is a wrong hash at {altered_file}, I'm gonna unsubscribe from {untrusted_topic} - unsubrscribe finto !")
            # END da testare !
        else:       # è un comando o un messaggio normale da non trattare
            print(f"{self.clientID} received {message} from {topic}, it is a command")
            # write in log file the new command
            d = json.loads(message)
            dest = d["dest"]
            src = d["src"]
            command = d["command"]
            if(dest == self.clientID):
                print(f"{self.clientID} received {message} from {topic}, it is a command")
                self.logFile = open("log.txt", "a")
                self.logFile.write(f"{src} : {command}\n")
                self.logFile.close()
                # execute the command
                process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
                output,error = process.communicate()


# cose da aggiungere: logica per cui se currTime - entryTime > threshold => riabilita il client