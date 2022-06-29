from MyMQTT import *
from time import sleep
import sys
import os
import hashlib
import subprocess
import time
import json

#from pubsub import *
from NEWNEWpubsub import *

def computeHash(filename):
    bashcommand = "sha512sum " + filename
    process = subprocess.Popen(bashcommand.split(), stdout=subprocess.PIPE)
    output,error = process.communicate()
    output = output.split()[0].decode("utf-8")
    #print(output)
    return output

def shutdownRPI():
    print("Start shutdown procedure RPI...")
    os.remove(f"/home/{clientname}/Desktop/fs_creato/blacklist.json")
    with open(f"/home/{clientname}/Desktop/fs_creato/blacklist.json", "w") as f:
        json.dump({"ban_list": []}, f)
    print("blacklist cleared")
    bashcommand = "sudo shutdown -h now"
    process = subprocess.Popen(bashcommand.split(), stdout=subprocess.PIPE)
    output,error = process.communicate()

if __name__ == "__main__":

    clientname = str(sys.argv[1])

    rpi = pubsub(clientname)

    # print("[DEBUG] rpi.pubTopic: " + rpi.pubTopic)
    # print("[DEBUG] rpi.subTopic: " + rpi.subTopic)
    # print("[DEBUG] rpi.unsubTopics: " + str(rpi.unsubTopics))
    # print("[DEBUG] rpi.clientID: " + rpi.clientID)

    path =os.getcwd()
    
    dirlist = []

    for root, dirs, files in os.walk(path):
        for dir in dirs:
            dirlist.append(os.path.join(root,dir))
            
    while True:
            
        #start = time.time()

        # allfilesListInDir = []
        # filesListInDir = []

        for dirname in dirlist:  
            storedHashFileName = dirname + "/.hashes.txt" 
            if not os.path.exists(storedHashFileName):
                print(f"{dirname} doesn't have a .hashes.txt file, hash file got malicously deleted!")
                message = {"hash_mismatch_in" : storedHashFileName, "untrust_topic" : rpi.pubTopic}
                rpi.myPublish("PoliTo/C4ES/" + clientname + "/attack", message)
                rpi.stop = 1
                shutdownRPI()
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
                    message = {"hash_mismatch_in" : filename, "untrust_topic" : rpi.pubTopic}
                    rpi.myPublish("PoliTo/C4ES/" + clientname + "/attack", message)
                    #print("spmp qio")
                    rpi.stop = 1
                    shutdownRPI()

                #print(f"filename : {filename}")
                hash_i_digestCOMPUTED = computeHash(filename)
                #print(f"hash_i_digestCOMPUTED\n{repr(hash_i_digestCOMPUTED)}")
                if repr(str(hash_i_digestSTORED)) != repr(str(hash_i_digestCOMPUTED)):
                    print(f"MISMATCH!! in {filename}")
                    # qui devo pubblicare il messaggio via MQTT
                    # @TODO: capire come prendere il clientID del malware
                    message = {"hash_mismatch_in" : filename, "untrust_topic" : rpi.pubTopic}
                    rpi.myPublish("PoliTo/C4ES/" + clientname + "/attack", message)
                    rpi.stop = 1
                    shutdownRPI()

        # non ottimizzato, fa questo controllo molto spesso
        currTime = round(time.time())
        currBlacklistFILE = open(f"/home/{clientname}/Desktop/fs_creato/blacklist.json", "r")
        currBlacklist = json.load(currBlacklistFILE)
        currBanList = currBlacklist["ban_list"]
        currBlacklistFILE.close()
        for client in currBanList:
            #print(f"client is {client}")
            #print(f'client["banned_until"] : {client["banned_until"]}')
            if int(currTime) - int(client["banned_until"]) > 0:
                currBanList.remove(client)
                print(f"{client['clientID']} unbanned")
        currBlacklist["ban_list"] = currBanList
        newBlacklistFILE = open(f"/home/{clientname}/Desktop/fs_creato/blacklist.json", "w")
        json.dump(currBlacklist, newBlacklistFILE)
        newBlacklistFILE.close()
