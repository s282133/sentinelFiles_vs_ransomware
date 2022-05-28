import hashlib

hasher = hashlib.sha512()

with open('tobehashed.txt', 'rb') as afile:
    buf = afile.read()
    hasher.update(buf)
    originalHash = hasher.hexdigest()

print(originalHash)