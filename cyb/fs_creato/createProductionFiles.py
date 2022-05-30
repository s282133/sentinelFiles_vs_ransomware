import random
import os
import string

letters = string.ascii_lowercase + string.ascii_uppercase + string.digits

def generateRandomRow(num_chars):
    return ''.join(random.choice(letters) for i in range(num_chars))



if __name__ == "__main__":
    
    path =os.getcwd()
    #we shall store all the file names in this list
    dirlist = []

    for root, dirs, files in os.walk(path):
        for dir in dirs:
            dirlist.append(os.path.join(root,dir))

    allfilesListInDir = []
    filesListInDir = []

    for dirname in dirlist:
        randNumFiles = random.randint(0, 7) 
        for i in range(0,randNumFiles):
            filenameLength = random.randint(4, 10)
            newfileName = generateRandomRow(filenameLength)
            numrows = random.randint(0, 40)
            newfileName = os.path.join(dirname, newfileName)
            with open(newfileName, "w") as f:
                num_rows = random.randint(0, 100)
                for j in range(0, num_rows):
                    num_chars = random.randint(0, 100)
                    row = generateRandomRow(num_chars)
                    f.write(row + "\n")