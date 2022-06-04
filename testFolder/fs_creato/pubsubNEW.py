from time import sleep
from MyMQTT import *
import paho.mqtt.client as PahoMQTT
import json
import time
import re
import sys, os
import subprocess

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
        self.dirlist = self.getRecursivePaths()
        

    def start (self):
        self.client.start()                

    def myPublish(self, topic, message):
        print(f"{self.clientID} publishing {message} to topic: {topic}")
        self.client.myPublish(topic, message)

    def notify(self, topic, message):
        #print("sono nella notify")

        msg_dict = json.loads(message)

        msg_type = msg_dict["type"]

        untrusted_topics = self.getUntrustedTopics()

        isUntrusted = self.isUntrusted(topic, untrusted_topics) or topic == f"PoliTo/C4ES/{self.clientID}/attack"        
        # ignore message if EITHER the topic is untrusted OR I'm the owner of the attack message (loopback)

        if(isUntrusted):
            pass        # i.e., ignore the message
        else:           # if the topic is not in the unstrusted list       
            if(msg_type == "attack_notification"):
                print(f"{self.clientID} received attack notification from {self.getSenderClientID(topic)}")
                self.insertUntrustedTopic(msg_dict, topic)
            elif(msg_type == "command_to_run"):
                print(f"{self.clientID} received command to run from {self.getSenderClientID(topic)}")
                self.run_check_integrity(self.dirlist)
            else:
                print(f"{self.clientID} received message of type {msg_type}, neither an attack_notification nor a command_to_run")
        
    def getRecursivePaths(self):
            path =os.getcwd()
            dirlist = []
            for root, dirs, files in os.walk(path):
                for dir in dirs:
                    dirlist.append(os.path.join(root,dir))

    def getUntrustedTopics():
        blackListFILE = open("blacklist.json", "r")
        blackList = json.load(blackListFILE)
        blackListFILE.close()
        banList = blackList["ban_list"]
        untrusted_topics = []
        for client in banList:
            untrusted_topics.append(client["untrust_topic"])
        return untrusted_topics

    def isUntrusted(self, topic, untrusted_topics):
        if(topic in untrusted_topics):
            return True
        else:
            return False

    def getNewUnsubTopic(self, topic):
            fields = topic.split("/")
            fieldClientID = fields[2]
            newUnsubTopic = self.baseTopic + fieldClientID + "/#"
            return newUnsubTopic

    def getSenderClientID(self, topic):
        fields = topic.split("/")
        senderClientID = fields[2]
        return senderClientID

    def insertUntrustedTopic(self, msg_dict, topic):
        fieldClientID = self.getSenderClientID(topic)
        altered_file = msg_dict["hash_mismatch_in"]
        untrusted_topic = msg_dict["untrust_topic"]
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

    def run_check_integrity(self, dirlist):
        print("Start check integrity...")
        for dirname in dirlist:  
            storedHashFileName = dirname + "/.hashes.txt" 
            storedHashFile = open(storedHashFileName, "r")
            storedSentinelsNum = int(storedHashFile.readline())
        for i in range(storedSentinelsNum):
            hash_i_name = str(storedHashFile.readline().rstrip('\n'))
            #print(f"hash_i_name : {hash_i_name}")
            hash_i_digestSTORED = str(storedHashFile.readline().rstrip('\n'))
            #print(f"hash_i_digestSTORED\n{repr(hash_i_digestSTORED)}")
            filename = hash_i_name
            if not os.path.exists(filename):
                print(f"Sentinel File {filename} has been deleted!")
                message = {"hash_mismatch_in" : filename, "untrust_topic" : self.pubTopic}
                self.myPublish("PoliTo/C4ES/" + clientname + "/attack", message)
                self.shutdownRPI()

            #print(f"filename : {filename}")
            hash_i_digestCOMPUTED = self.computeHash(filename)
            #print(f"hash_i_digestCOMPUTED\n{repr(hash_i_digestCOMPUTED)}")
            if repr(str(hash_i_digestSTORED)) != repr(str(hash_i_digestCOMPUTED)):
                print(f"MISMATCH!! in {filename}")
                # qui devo pubblicare il messaggio via MQTT
                # @TODO: capire come prendere il clientID del malware
                message = {"hash_mismatch_in" : filename, "untrust_topic" : self.pubTopic}
                self.myPublish("PoliTo/C4ES/" + clientname + "/attack", message)
                self.shutdownRPI()

    def shutdownRPI(self):
        print("Start shutdown procedure RPI...")
        currentBlacklistFile = open("blacklist.json", "r")
        currentBlacklist = json.load(currentBlacklistFile)
        currentBlacklistFile.close()
        currentBannedList = currentBlacklist["ban_list"]
        currentBannedList = []
        currentBlacklist["ban_list"] = currentBannedList
        emptyBlacklistFile = open("blacklist.json", "w")
        json.dump(currentBlacklist, emptyBlacklistFile)
        bashcommand = "shutdown -h now"
        while True:
            # voglio prima controllare che il json si resetti
            pass

    def computeHash(filename):
        bashcommand = "sha512sum " + filename
        process = subprocess.Popen(bashcommand.split(), stdout=subprocess.PIPE)
        output,error = process.communicate()
        output = output.split()[0].decode("utf-8")
        #print(output)
        return output

    def unban_expired_entries(self):
        currTime = round(time.time())
        currBlacklistFILE = open("blacklist.json", "r")
        currBlacklist = json.load(currBlacklistFILE)
        currBanList = currBlacklist["ban_list"]
        currBlacklistFILE.close()
        for client in currBanList:
            if currTime - client["banned_until"] > 0:
                currBanList.remove(client)
                print(f"{client['clientID']} unbanned")
        currBlacklist["ban_list"] = currBanList
        newBlacklistFILE = open("blacklist.json", "w")
        json.dump(currBlacklist, newBlacklistFILE)
        newBlacklistFILE.close()

# cose da aggiungere: logica per cui se currTime - entryTime > threshold => riabilita il client

if __name__ == "__main__":
    #print("[DEBUG]  " + str(sys.argv))

    clientname = str(sys.argv[1])

    rpi = pubsub(clientname)

    counter = 0

    while True:

        if counter % 60 == 0: 
            rpi.unban_expired_entries()
        counter += 1
        time.sleep(1)
    