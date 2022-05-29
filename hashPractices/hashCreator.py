# Questo script è solo un esperimento, dovrebbe essere lanciato solo al momento della creazione 
# dei file sentinella e dovrebbe agire in ogni cartella del FileSystem

import os
import hashlib
from stat import S_IREAD, S_IRGRP, S_IROTH

hasher = hashlib.sha512()

thisDirectory = os.getcwd()

with open(".hashes.txt", "w") as file:
    for filename in os.listdir(thisDirectory):
        f = os.path.join(thisDirectory, filename)
        # checking if it is a file
        if os.path.isfile(f) and filename != ".hashes.txt":
            with open(f, "rb") as afile:
                buf = afile.read()
                hasher.update(buf)
                file.write(f + ": " + hasher.hexdigest() + "\n")

# changing permissions: now owner has READ permission, group has READ permission, others have READ permission
os.chmod(".hashes.txt",  S_IREAD | S_IRGRP | S_IROTH)

# idea: mettere in testa una riga che contenga il numero di file sentinelle nel file ".hashes.txt"