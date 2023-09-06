import re
import os
import subprocess

os.system("cls")
f = open("test.algo", "r",encoding='utf-8').readlines()
res = []
for i in range(len(f) - 1, -1, -1):
    if f[i].strip() == "fin":
        f = f[0 : i + 1]
        break
for i,v in enumerate(f):
    if v.strip()=='':
        continue
    res.append({i+1:re.sub(" +", " ", v).replace("\n", "").strip()})


for v in res:
    print(v)
