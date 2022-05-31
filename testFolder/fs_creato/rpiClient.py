from MyMQTT import *
from time import sleep
import sys
import os
import hashlib

from pubsub import *

def computeHash(filename):
    hasher = hashlib.sha512()
    print(f"Computing hash for {filename}")
    print(f"filename = {filename}")
    with open(filename, "rb") as afile:
        buf = afile.read()
        hasher.update(buf)
        #hashfile.write(f'{sentinel} : {hasher.hexdigest()} \n')
        hashhex = str(hasher.hexdigest())
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
        storedHashFileName = dirname + "/.hashes.txt"       # \ per windows, / per linux
        storedHashFile = open(storedHashFileName, "r")
        storedSentinelsNum = int(storedHashFile.readline())
        for i in range(storedSentinelsNum):
            hash_i_name = str(storedHashFile.readline().rstrip('\n'))
            print(f"hash_i_name : {hash_i_name}")
            hash_i_digestSTORED = str(storedHashFile.readline().rstrip('\n'))
            print(f"hash_i_digestSTORED\n{repr(hash_i_digestSTORED)}")
            filename = hash_i_name
            print(f"filename : {filename}")
            hash_i_digestCOMPUTED = computeHash(filename)
            print(f"hash_i_digestCOMPUTED\n{repr(hash_i_digestCOMPUTED)}")
            if repr(str(hash_i_digestSTORED)) != repr(str(hash_i_digestCOMPUTED)):
                print("MISMATCH!!")
                while True:
                    pass
