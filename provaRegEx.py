import re

p = re.compile("PoliTo/C4ES/.+/attack")

res1 = bool(p.match("PoliTo/C4ES/1/attack"))

res2 = bool(p.match("PoliTo/C4ES/2/attack"))

res3 = bool(p.match("PoliTo/C4ES//attack"))

res4 = bool(p.match("PoliTo/C4ES/pino/attack"))

print(res1)
print(res2)
print(res3)
print(res4)