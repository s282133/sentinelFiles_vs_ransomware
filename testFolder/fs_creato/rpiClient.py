from MyMQTT import *
from time import sleep
import sys
import os
import hashlib
import subprocess
import time

from pubsub import *

def computeHash(filename):
    # hasher = hashlib.sha512()
    # print(f"Computing hash for {filename}")
    # print(f"filename = {filename}")
    # with open(filename, "rb") as afile:
    #     buf = afile.read()
    #     hasher.update(buf)
    #     #hashfile.write(f'{sentinel} : {hasher.hexdigest()} \n')
    #     hashhex = str(hasher.hexdigest())
    bashcommand = "sha512sum " + filename
    process = subprocess.Popen(bashcommand.split(), stdout=subprocess.PIPE)
    output,error = process.communicate()
    output = output.split()[0].decode("utf-8")
    #print(output)
    return output

if __name__ == "__main__":

    clientname = str(sys.argv[1])

    rpi = pubsub(clientname)

    # while True:

    path =os.getcwd()
    
    rounds = 0

    while rounds < 1000000:
            
        start = time.time()
    
        dirlist = []

        for root, dirs, files in os.walk(path):
            for dir in dirs:
                dirlist.append(os.path.join(root,dir))

        allfilesListInDir = []
        filesListInDir = []

        for dirname in dirlist:  
            storedHashFileName = dirname + "/.hashes.txt"       # \ per windows, / per linux
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
                    rpi.myPublish("PoliTo/C4ES/" + clientname + "/attack", "possible ransomware attack in progress!")
                    while True:
                        pass
        end = time.time()
        rounds += 1
        print(f"Time elapsed: {end-start}")