from pubsub import *
from MyMQTT import *
from time import sleep
import sys
import os
import hashlib

def computeHash(file):
    hasher = hashlib.sha512()
    with open(file, "rb") as afile:
        buf = afile.read()
        hasher.update(buf)
        hashhex = hasher.hexdigest()
    return hashhex


if __name__ == "__main__":

    clientname = str(sys.argv[1])

    rpi = pubsub(clientname)

    path =os.getcwd()

    dirlist = []

    for root, dirs, files in os.walk(path):
        for dir in dirs:
            dirlist.append(os.path.join(root,dir))

    allfilesListInDir = []
    filesListInDir = []

    for dirname in dirlist:
        hashfile = open(os.path.join(dirname,".hashes.txt"), "r")
        numSentinels = int(hashfile.readline())
        for i in range(numSentinels):
            row = hashfile.readline()
            sentinelname = str(row).split(":")[0]
            storedSentinelhash = str(row).split(":")[1]
            computedSentinelhash = computeHash(os.path.join(dirname,sentinelname))
            if storedSentinelhash != computedSentinelhash:
                print(f"SENTINEL HASH MISMATCH in {os.path.join(dirname,sentinelname)}")
        

    for i in range(0,10):
        message = f"hi_from_{clientname}"
        rpi.myPublish(rpi.pubTopic, message)
        sleep(10)