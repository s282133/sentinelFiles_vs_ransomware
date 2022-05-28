import subprocess
import os
import string
import sys

bashcommand = "ls"

process = subprocess.Popen(bashcommand.split(), stdout=subprocess.PIPE)
output,error = process.communicate()

#for filename  in output:
#    print(filename)

#print(output)

myparam = sys.argv[1]

print(myparam)

outputStr = output.decode("utf-8")

filesList = outputStr.split("\n")

for filename in filesList:
    print(filename)

#mylist = os.system("ls")

