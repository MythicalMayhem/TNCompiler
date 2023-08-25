import re
string = """
fonction nom(@ghjk:asdfa,@sdfgsf:gsdfgs):type
debut
lire(ghjk
ghjk <-- ghjk*2
retourner 
fin
        """.split('\n')[1:-1]


def standAlonelegit(hay,needle): 
    rematch = re.findall(f'(?P<before>.?)(?P<middle>{needle})(?P<after>.?)',hay,re.IGNORECASE)
    print(rematch)
def defFixer(arr):
    params = arr[0].split("(")[1].split(")")[0].split(",")
    while "" in params:
        params.remove("")
    toreplace = []
    for i in range(0, len(params)):
        params[i] = params[i].split(":")[0]
        if params[i][0] == "@":
            toreplace.append(params[i][1::])
    for i in range(1, len(arr) - 1):
        for j in range(0,len(toreplace)):
            standAlonelegit(arr[i],toreplace[j]) 

defFixer(string)