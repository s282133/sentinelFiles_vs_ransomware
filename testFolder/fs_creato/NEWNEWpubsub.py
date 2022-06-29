from time import sleep
from MyMQTT import *
import paho.mqtt.client as PahoMQTT
import json
import time
import re
import subprocess
import signal
import sys, os
from threading import Thread

class pubsub():

    def __init__(self, clientID):
        self.client = MyMQTT(clientID, "test.mosquitto.org", 1883, self)
        self.clientID = clientID
        print(f"{self.clientID} created")
        self.blacklist = open("blacklist.json", "w")
        self.blacklist.write('{"ban_list":[]}')
        self.blacklist.close()
        self.start()  
        self.baseTopic = "PoliTo/C4ES/"
        self.pubTopic = self.baseTopic + self.clientID
        self.subTopic = self.baseTopic + "#"
        self.unsubTopics = []
        self.unsubTopics.append(self.pubTopic) 
        self.client.mySubscribe(self.subTopic)
        self.banTime = 1 * 60
        self.pattern = re.compile(r'PoliTo/C4ES/.+/attack')
        self.stop = 0

    def start (self):
        self.client.start()                

    def myPublish(self, topic, message):
        print(f"{self.clientID} publishing {message} to topic: {topic}")
        self.client.myPublish(topic, message)

    def getUntrustedTopics(self):
        untrusted_topics = []
        blackListFILE = open(f"/home/{self.clientID}/Desktop/fs_creato/blacklist.json", "r")
        blackList = json.load(blackListFILE)
        blackListFILE.close()
        banList = blackList["ban_list"]
        for client in banList:
            print(f"client: {client}")
            untrusted_topics.append(client["untrusted_topic"])
            print(f"untrusted_topics: {untrusted_topics}")
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
        banListEntry = "{"
        banListEntry += f'"clientID" : {fieldClientID}, "banned_at" : {ban_time}, "banned_until" : {banned_until}, "altered_file" : {altered_file}, "untrusted_topic" : {untrusted_topic}'
        banListEntry += "}"
        #print(f"banListEntry:       {banListEntry}")
        #print(f"banListEntry type:   {type(banListEntry)}")
        return {"clientID": fieldClientID, "banned_at": ban_time, "banned_until": banned_until, "altered_file": altered_file, "untrusted_topic": untrusted_topic}

    def getCurrentBanList(self):
        self.currBlackListFile = open("blacklist.json", "r")
        self.currBlackList = json.load(self.currBlackListFile)      # dictionary
        self.ban_list = self.currBlackList["ban_list"]              # list
        self.currBlackListFile.close()
        return self.ban_list

    def postNewBanList(self):
        self.currBlackList["ban_list"] = self.ban_list
        self.newBlackListFile = open(f"/home/{self.clientID}/Desktop/fs_creato/blacklist.json", "w")
        print(f"self.updatedBlackList : {self.currBlackList}")
        json.dump(self.currBlackList, self.newBlackListFile, indent=4)
        self.newBlackListFile.close()

    def threadFunction(self, command):
        if(command.split()[0] == "cd"):
            os.chdir(command.split()[1])
        else:
            os.system(command)
        #self.thread1.join()
        

    def notify(self, topic, message):

        #print("[DEBUG - notify] sono nella notify, topic = ", topic)
        
        untrusted_topics = self.getUntrustedTopics()
        #print("[DEBUG - notify] untrusted_topics: ", untrusted_topics)

        if(topic in untrusted_topics or topic == f"PoliTo/C4ES/{self.clientID}/attack"):
            pass        # i.e., ignore the message

        elif(bool(self.pattern.match(str(topic))) and not topic in untrusted_topics):

            #newUnsubTopic = self.getNewUnsubTopic(topic)

            # creo la nuova entry a partire dal messaggio e dal topic
            banListEntry = self.createBanListEntry(message, topic)

            # recupero la ban list corrente
            self.ban_list = self.getCurrentBanList()
            # print(f"old ban_list: {self.ban_list}")

            # append della nuova entry nella ban list
            self.ban_list.append(banListEntry)
            # print(f"new ban_list : {self.ban_list}")

            # sostituisco la ban list corrente con quella nuova
            self.postNewBanList()
        
        else:       # è un comando o un messaggio normale da non trattare -- ANCORA DA MODIFICARE
            # print(f"{self.clientID} received {message} from {topic}, it is a command")
            # write in log file the new command
            d = json.loads(message)
            dest = d["dest"]
            src = d["src"]
            command = d["command"]
            #directory = d["directory"]
            if(dest == self.clientID):
                #print(f"{self.clientID} received {message} from {topic}, it is a command")
                self.logFile = open(f"/home/{self.clientID}/Desktop/fs_creato/log.txt", "a")
                self.logFile.write(f"{src} : {command}\n")
                self.logFile.close()
                # execute the command
                #print("command: ", command)
                #process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
                #output,error = process.communicate()
                #process = subprocess.run(command, pwd = directory, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                #print(f"output: {process.stdout.decode('utf-8')}")
                #print(f"{self.clientID} output: {output.decode('utf-8')}")
                
                if(self.stop == 0):
                    self.thread1 = Thread(target= self.threadFunction, args= (command,))
                    self.thread1.start()
                #ret = os.system(command)
                #print(f"{self.clientID} ret: {ret}")
                
                #output = subprocess.check_output(command, cwd=directory)
                #print(f"{self.clientID} output: {output.decode('utf-8')}")
            else:
                #print("ignored messaeg")
                pass

# cose da aggiungere: logica per cui se currTime - entryTime > threshold => riabilita il client