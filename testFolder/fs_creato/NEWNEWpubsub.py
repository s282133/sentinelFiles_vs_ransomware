from time import sleep
from MyMQTT import *
import paho.mqtt.client as PahoMQTT
import json
import time
import re
import subprocess
import sys, os

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
        self.pattern = re.compile(r'PoliTo/C4ES/.+/attack')

    def start (self):
        self.client.start()                

    def myPublish(self, topic, message):
        print(f"{self.clientID} publishing {message} to topic: {topic}")
        self.client.myPublish(topic, message)

    def getUntrustedTopics(self):
        untrusted_topics = []
        blackListFILE = open("blacklist.json", "r")
        blackList = json.load(blackListFILE)
        blackListFILE.close()
        banList = blackList["ban_list"]
        for client in banList:
            untrusted_topics.append(client["untrust_topic"])
        return untrusted_topics

    def getNewUnsubTopic(self, topic):
        fields = topic.split("/")
        fieldClientID = fields[2]
        newUnsubTopic = self.baseTopic + fieldClientID + "/#"
        return newUnsubTopic

    def getUntrustedTopicFromMessage(self, message):
        d = json.loads(message)
        untrusted_topic = d["untrust_topic"]
        return untrusted_topic

    def createBanListEntry(self, message, topic):
        untrusted_topic = self.getUntrustedTopicFromMessage(message)
        fieldClientID = topic.split("/")[2]
        ban_time = round(time.time())
        banned_until = ban_time + self.banTime
        d = json.loads(message)
        altered_file = d["hash_mismatch_in"]
        banListEntry = {"clientID" : fieldClientID, "banned_at" : ban_time, "banned_until" : banned_until, "altered_file" : altered_file, "untrusted_topic" : untrusted_topic}
        return banListEntry

    def getCurrentBanList(self):
        self.currBlackListFile = open("blacklist.json", "r")
        self.currBlackList = json.load(self.currBlackListFile)      # dictionary
        self.ban_list = self.currBlackList["ban_list"]              # list
        self.currBlackListFile.close()

    def postNewBanList(self):
        self.currBlackList["ban_list"] = self.ban_list
        self.newBlackListFile = open("blacklist.json", "w")
        print(f"self.updatedBlackList : {self.currBlackList}")
        json.dump(self.currBlackList, self.newBlackListFile, indent=4)
        self.newBlackListFile.close()


    def notify(self, topic, message):

        print("sono nella notify, topic = ", topic)
        
        untrusted_topics = self.getUntrustedTopics()

        print("untrusted_topics: ", untrusted_topics)

        if(topic in untrusted_topics or topic == f"PoliTo/C4ES/{self.clientID}/attack"):
            #print("sono nella notify - ignored message")
            pass        # i.e., ignore the message
        elif(bool(self.pattern.match(str(topic))) and not topic in untrusted_topics):
            #print("sono nella notify - attack message")
            newUnsubTopic = self.getNewUnsubTopic(topic)
            print("[DEBUG]  " + str(newUnsubTopic))
            banListEntry = self.createBanListEntry()

            self.ban_list = self.getCurrentBanList()
            print(f"old ban_list: {self.ban_list}")

            self.ban_list.append(banListEntry)

            print(f"new ban_list : {self.ban_list}")
            
            self.postNewBanList()
            # END da testare !
        
        else:       # è un comando o un messaggio normale da non trattare
            # @todo : lo modifico dopo
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
                print(f"{self.clientID} executed {command}")
                print(f"{self.clientID} output: {output}")


# cose da aggiungere: logica per cui se currTime - entryTime > threshold => riabilita il client