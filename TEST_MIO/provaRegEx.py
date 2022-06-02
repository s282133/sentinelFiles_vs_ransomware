import re
import json

# currBlackListFile = open("blacklist.json", "r")
# currBlackList = json.load(currBlackListFile)      # dictionary

p = re.compile("PoliTo/C4ES/.+/attack")

res1 = bool(p.match("PoliTo/C4ES/1/attack"))

res2 = bool(p.match("PoliTo/C4ES/2/attack"))

res3 = bool(p.match("PoliTo/C4ES//attack"))

res4 = bool(p.match("PoliTo/C4ES/pino/attack"))

res5 = bool(p.match("PoliTo/C4ES/TEST/attack"))

print(res1)
print(res2)
print(res3)
print(res4)
print(res5)

# currBanList = currBlackList["ban_list"]
# newBlackList = {'ban_list': [{'clientID': 'pi0', 'banTime': 1654098658.2481802, 'altered_file': '/home/pi/Desktop/fs_creato/A/TR/.samples_oH.txt', 'untrusted_topic': 'PoliTo/C4ES/pi0/#'}]}
# newBlackListFile = open("blacklist.json", "w")
# json.dump(newBlackList, newBlackListFile, indent=4)

