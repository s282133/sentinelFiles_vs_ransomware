import os
from os.path import isfile, join
import random
import string
import hashlib

hasher = hashlib.sha512()

letters = string.ascii_lowercase + string.ascii_uppercase + string.digits

def generateSentinels(firstname, lastname, numSentinels, dirname):
    sentinelList = []
    for i in range(0, numSentinels):                    # da legare ai parametri firstname e lastname
        sentinelName = generateRandomName(firstname, lastname, i, numSentinels)
        sentinelList.append(sentinelName)
        sentinelPath = os.path.join(dirname, sentinelName)
        newfileName = sentinelPath
        with open(newfileName, "w") as f:
            num_rows = random.randint(0, 100)
            for j in range(0, num_rows):
                num_chars = random.randint(0, 100)
                row = generateRandomRow(num_chars)
                f.write(row + "\n")
    return sentinelList

def generateRandomRow(num_chars):
    return ''.join(random.choice(letters) for i in range(num_chars))

def generateRandomName(firstname, lastname, i, numSentinels):
    if i == 0:
        if(firstname[0] == '.'):
            return ".0"  + firstname[1:]
        else:
            return "." + firstname
    elif i == numSentinels - 1:
        return "z" + lastname
    else:
        name = ""
        namelength = min(len(firstname), len(lastname))
        for j in range(0, namelength):
            #print(firstname[j], ord(firstname[j]), lastname[j], ord(lastname[j]))
            ascii_sum = ord(firstname[j]) + ord(lastname[j])
            #print(f"ascii_sum : {ascii_sum}")
            ascii_avg = ascii_sum / 2
            #print(f"ascii_avg : {ascii_avg}")
            ascii_avg = int(ascii_avg)
            if(ascii_avg >=0 and ascii_avg < 48):
                ascii_avg = 48
            elif(ascii_avg >= 58 and ascii_avg < 64):
                ascii_avg = 65
            elif(ascii_avg >= 91 and ascii_avg < 97):
                ascii_avg = 97
            elif(ascii_avg >= 123 and ascii_avg <= 127):
                ascii_avg = 122
            else:
                ascii_avg = ascii_avg
            char = chr(ascii_avg)
            #print(f"char : {char}")
            name += char
        return name


if __name__ == "__main__":

    path =os.getcwd()
    #we shall store all the file names in this list
    dirlist = []

    for root, dirs, files in os.walk(path):
        for dir in dirs:
            dirlist.append(os.path.join(root,dir))

    allfilesListInDir = []
    filesListInDir = []

    for dirname in dirlist:                                                          # all directories starting from the root  
        hashfile = open(dirname + "/.hashes.txt", "w")
        onlyfiles = [f for f in os.listdir(dirname) if isfile(join(dirname, f))]     # all files in current dir 
        #if(len(onlyfiles) > 0):
        print(f"DIR: {dirname} FILEs PRIMA: {onlyfiles}")
        numFiles = len(onlyfiles)
        numSentinels = int( int(numFiles) / 2) +2                                   # ne crea sempre minimo 2 in ogni directory
        if numFiles > 0:
            firstname = onlyfiles[0]
            lastname = onlyfiles[-1]
        else:
            firstname = ".00"
            lastname = "zzz"
        sentinelList = generateSentinels(firstname, lastname, numSentinels, dirname)
        hashfile.write(f"{numSentinels}\n")
        for sentinel in sentinelList:
            onlyfiles.append(sentinel)
            sentinelfilename = os.path.join(dirname, sentinel)
            with open(sentinelfilename, "rb") as afile:
                buf = afile.read()
                hasher.update(buf)
                hashfile.write(f'{sentinel} : {hasher.hexdigest()} \n')
        hashfile.close()
        print(f"DIR: {dirname} FILEs DOPO: {onlyfiles}")
