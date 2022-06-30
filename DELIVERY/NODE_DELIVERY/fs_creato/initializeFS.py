import os

path =os.getcwd()
#we shall store all the file names in this list
dirlist = []

filelist = []

for root, dirs, files in os.walk(path):
    for file in files:
        if (file.endswith(".py") or file.endswith(".sh")):
            pass
        else:
            filelist.append(os.path.join(root,file))
#print(filelist)

for filename in filelist:
    os.remove(filename)
    
