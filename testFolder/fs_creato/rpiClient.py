from MyMQTT import *
from time import sleep
import sys
import os
import hashlib
import subprocess
import time
import json

from pubsub import *

def computeHash(filename):
    bashcommand = "sha512sum " + filename
    process = subprocess.Popen(bashcommand.split(), stdout=subprocess.PIPE)
    output,error = process.communicate()
    output = output.split()[0].decode("utf-8")
    #print(output)
    return output

if __name__ == "__main__":

    clientname = str(sys.argv[1])

    rpi = pubsub(clientname)

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
            storedHashFile = open(storedHashFileName, "r")
            storedSentinelsNum = int(storedHashFile.readline())
            for i in range(storedSentinelsNum):
                hash_i_name = str(storedHashFile.readline().rstrip('\n'))
                #print(f"hash_i_name : {hash_i_name}")
                hash_i_digestSTORED = str(storedHashFile.readline().rstrip('\n'))
                #print(f"hash_i_digestSTORED\n{repr(hash_i_digestSTORED)}")
                filename = hash_i_name
                #print(f"filename : {filename}")
                hash_i_digestCOMPUTED = computeHash(filename)
                #print(f"hash_i_digestCOMPUTED\n{repr(hash_i_digestCOMPUTED)}")
                if repr(str(hash_i_digestSTORED)) != repr(str(hash_i_digestCOMPUTED)):
                    print(f"MISMATCH!! in {filename}")
                    # qui devo pubblicare il messaggio via MQTT
                    # @TODO: capire come prendere il clientID del malware
                    message = {"hash_mismatch_in" : filename, "untrust_topic" : rpi.pubTopic + "/#"}
                    rpi.myPublish("PoliTo/C4ES/" + clientname + "/attack", message)
                    while True:
                        # qui potrei mettere lo shutdown del sistema, per ora si ferma solamente
                        pass

        # non ottimizzato, fa questo controllo molto spesso
        currTime = round(time.time())
        currBlacklistFILE = open("blacklist.json", "r")
        currBlacklist = json.load(currBlacklistFILE)
        currBlacklistFILE.close()
        for client in currBlacklist:
            if currTime - client["banned_until"] > 0:
                currBlacklist.remove(client)
                print(f"{client['clientID']} unbanned")
        newBlacklistFILE = open("blacklist.json", "w")
        json.dump(currBlacklist, newBlacklistFILE)
        newBlacklistFILE.close()