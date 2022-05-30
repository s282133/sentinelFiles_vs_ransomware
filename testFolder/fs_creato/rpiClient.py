from MyMQTT import *
from time import sleep
import sys
import os
import hashlib

from pubsub import *

def computeHash(file):
    hasher = hashlib.sha512()
    print(f"Computing hash for {file}")
    with open(file, "r") as afile:
        buf = afile.read()
        hasher.update(buf)
        hashhex = hasher.hexdigest()
    return hashhex

if __name__ == "__main__":

    clientname = str(sys.argv[1])

    rpi = pubsub(clientname)

    # while True:

    path =os.getcwd()
    
    dirlist = []

    for root, dirs, files in os.walk(path):
        for dir in dirs:
            dirlist.append(os.path.join(root,dir))

    allfilesListInDir = []
    filesListInDir = []

    for dirname in dirlist:  
        storedHashFileName = dirname + "\.hashes.txt"       # per windows, / per linux
        storedHashFile = open(storedHashFileName, "r")
        storedSentinelsNum = int(storedHashFile.readline())
        for i in range(storedSentinelsNum):
            hash_i_name = str(storedHashFile.readline())
            print(f"hash_i_name : {hash_i_name}")
            hash_i_digestSTORED = storedHashFile.readline()
            print(f"hash_i_digestSTORED : {hash_i_digestSTORED}")
            hash_i_digestCOMPUTED = computeHash(os.path.join(dirname, hash_i_name))
            print(f"hash_i_digestCOMPUTED : {hash_i_digestCOMPUTED}")
            if hash_i_digestSTORED != hash_i_digestCOMPUTED:
                #print(f"{hash_i_name} : {hash_i_digestSTORED} != {hash_i_digestCOMPUTED}")
                #rpi.publish(hash_i_name, hash_i_digestCOMPUTED)
                print("MISMATCH!!")