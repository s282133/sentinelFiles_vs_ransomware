import os

encrypted = 0;
non_encrypted = 0;

pwd = os.getcwd()

for root, subFolder, files in os.walk(pwd): 
    for item in files: 
        if item.endswith(".gpg") : 
            print(item)
            encrypted += 1
        else:
            non_encrypted += 1;

all = encrypted + non_encrypted

print(f"{encrypted} files got encrypted out of {all} files.")