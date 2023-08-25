import re

    
f = open("test.algo", "r").readlines()
res = []
for sub in f:
    res.append(sub.replace("\n", "").strip())


def searchParent(start, name):
    for k in range(start, -1, -1):
        if str(res[k]).startswith("["):
            continue
        items1 = res[k].split(" ")
        if name == "fonction":
            if items1[0] == "procedure" or items1[0] == "fonction":
                return k
        else:
            if items1[0] == name:
                return k


while "" in res:
    res.remove("")

if res[0].lower() != "debut":
    raise Exception("debut manquante")
if res[len(res) - 1].lower() != "fin":
    raise Exception(f"Debut manquante : ligne {len(res)}")
res.pop(0)
res.pop(-1)

for i in range(0, len(res) - 1):
    items = res[i].split(" ")
    if items[0] == "finpour":
        search = searchParent(i, "pour")
        res[search] = res[search : i + 1]
        for j in range(search + 1, i + 1):
            res[j] = ""
    elif items[0] == "finsi":
        search = searchParent(i, "si")
        res[search] = res[search : i + 1]
        for j in range(search + 1, i + 1):
            res[j] = ""
    elif items[0] == "Jusqu'a":
        search = searchParent(i, "Repeter")
        res[search] = res[search : i + 1]
        for j in range(search + 1, i + 1):
            res[j] = ""
    elif items[0] == "fintantque":
        search = searchParent(i, "tantque")
        res[search] = res[search : i + 1]
        for j in range(search + 1, i + 1):
            res[j] = ""
    elif items[0] == "fin":
        search = searchParent(i, "fonction")
        res[search] = res[search : i + 1]
        for j in range(search + 1, i + 1):
            res[j] = ""


def check(arr):
    if isinstance(arr, list):
        return True
    else:
        return False


def arraying(pig):
    L = pig
    while check(L):
        for i in range(0, len(L)):
            if check(L[i]):
                item = L[i]
                L.remove(L[i])
                for j in range(len(item) - 1, -1, -1):
                    L.insert(i, item[j])
        test = True
        for i in range(0, len(L)):
            if check(L[i]) == True:
                test = False
        if test:
            break
    return L


while "" in res:
    res.remove("")
#print(res)
res = arraying(res)
#print(res)

newres = []


def isVariable(el):
    l = el.lower()
    test = True
    if ("a" <= l[0] <= "z") == False:
        return False
    for i in l:
        if ("a" <= i <= "z" or "0" <= i <= "9") == False:
            return False
    return test


def isParam(el):
    els = el.split(",")
    for e in els:
        newel = re.match(
            "@?[a-z]+([a-z]|[0-9])*(:[a-z]+([a-z]|[0-9])*)?", e, re.IGNORECASE
        )
        if newel:
            continue
        else:
            return False
    return True


def isBoucleFor(el):
    el = el.split(" ")[1:-1]
    index, start, end = 0, 0, 0
    for i in range(0, len(el)):
        if el[i] == "de":
            index = i
        if el[i] == "a":
            start = i 
    index, start, end = el[0:index], el[index + 1 : start], el[start + 1 : len(el)]
    if len(index) > 1:
        return False
    index = index[0]
    if isVariable(index) and check(end) and check(start):
        return f'for {index} in range({" ".join(start)},{" ".join(end)}):'
    else:
        return False


def isSi(el):
    newel = re.match("si[ ]+(?P<arguments>.+)[ ]+alors", el, re.IGNORECASE)
    if newel:
        return f'if ({newel.group("arguments")}):'
    else:
        return False


def isSinonsi(el):
    newel = re.match("sinonsi[ ]+(?P<arguments>.+)[ ]+alors", el, re.IGNORECASE)
    if newel:
        return f'elif ({newel.group("arguments")}):'
    else:
        return False


def isSinon(el):
    newel = re.match("sinon[ ]*:?", el, re.IGNORECASE)
    if newel :
        return f"else :"
    else:
        return False


def isFonction(el):
    newel = re.match(
        "fonction[ ]+(?P<name>[a-z]([a-z]|[0-9])*)[ ]*\((?P<arguments>.*)\):(?P<returntype>[a-z]+[0-9]*)",
        el,
        re.IGNORECASE,
    )
    if newel:
        newarg = isParam(newel.group("arguments"))
        if newarg:
            return f"def {newel.group('name')} ({newel.group('arguments')}):{newel.group('returntype')}:"
        else:
            return False
    return False


def isProcedure(el):
    newel = re.match(
        "procedure[ ]+(?P<name>[a-z]([a-z]|[0-9])*)[ ]*\((?P<arguments>.*)\)",
        el,
        re.IGNORECASE,
    )
    if newel:
        newarg = isParam(newel.group("arguments"))
        if newarg:
            return f"def {newel.group('name')} ({newel.group('arguments')}):"
        else:
            return False
    return False


def isTantque(el):
    newel = re.match("tantque[ ]+(?P<arguments>.*)", el,re.IGNORECASE)
    if newel:
        return f'while {newel.group("arguments")}:'
    else:
        return False


def isJusqua(el):
    newel = re.match("Jusqu'?a[ ]+(?P<arguments>.+)", el,re.IGNORECASE)
    if newel:
        return f'if ({newel.group("arguments")}):'
    else:
        return False

def isRepeter(el):
    newel = re.match("repeter[ ]*:?", el, re.IGNORECASE)
    if newel :
        return f"while True :"
    else:
        return False

for i in range(0, len(res)):
    res[i] = re.sub(" +", " ", res[i])
    starter = res[i].split(" ")[0].lower()+' '
    
    if starter in ["finpour", "finsi", "fin"]:
        newres.append(res[i])
        continue 
    elif re.match("^pour[ ]+",starter,re.IGNORECASE):
        if isBoucleFor(res[i]):
            newres.append(isBoucleFor(res[i]))
        else:
            print("pour invalide")
    elif re.match("^si[ ]+",starter,re.IGNORECASE):
        if isSi(res[i]):
            newres.append(isSi(res[i]))
        else:
            print("si invalide ")
    elif re.match("^sinonsi[ ]+",starter,re.IGNORECASE):
        try:
            if searchParent(i, "si") or (searchParent(i, "sinonsi")):
                newres.append(isSinonsi(res[i]))
            else:
                print("sinon invalide")
        except:
            print("sinon invalide")
    elif re.match("^sinon[ ]*:?",starter,re.IGNORECASE):
        print(searchParent(i, "si"),searchParent(i, "sinonsi")),isSinon(res[i])
        try:
            if (searchParent(i, "si") or searchParent(i, "sinonsi"))and isSinon(res[i]):
                newres.append(isSinon(res[i]))
            else:
                print("sinon invalide")
        except:
            print("sinon invalide")
    elif re.match("^fonction[ ]+",starter,re.IGNORECASE):
        if isFonction(res[i]):
            newres.append(isFonction(res[i]))
        else:
            print("fonction invalide ")
    elif re.match("^procedure[ ]+",starter,re.IGNORECASE):
        if isProcedure(res[i]):
            newres.append(isProcedure(res[i]))
        else:
            print("procedure invalide ")
    elif re.match("^tant[ ]?que",starter,re.IGNORECASE):
        if isTantque(res[i]):
            newres.append(isTantque(res[i]))
        else:
            print("tantque invalide ")
    elif re.match("^jusqu'?(a|à)",starter,re.IGNORECASE):
        if isJusqua(res[i]):
            newres.append(isJusqua(res[i]))
            newres.append('break')
            newres.append('\tfinsi')
        else:
            print(" Jusqu'a invalide ")
    elif re.match("^R(e|é)p(e|é)ter[ ]*",starter,re.IGNORECASE):
        if isRepeter(res[i]):
            newres.append(isRepeter(res[i]))
        else:
            print("repeter invalide ")
    else:
        newres.append(res[i])
while "" in newres:
    newres.remove("")
print(newres)

# writing
wres = []
indent = 0 
for i in range(0, len(newres)):
    newres[i] = re.sub(" +", " ", str(newres[i]))
    starter = newres[i].strip()
    if re.match('debut',starter,re.IGNORECASE):
        wres.append('#'+'\t'*(indent-1) + str(newres[i])+'\n')
    elif re.match('finpour|finsi|fin|fintantque',starter,re.IGNORECASE):
        indent= abs(indent-1)
        wres.append('#'+'\t'*(indent) + str(newres[i])+'\n')
    elif re.match('break',starter,re.IGNORECASE):
        wres.append('\t'*(indent) + str(newres[i])+'\n')
        indent= abs(indent-1)
    elif re.match('if|while|def|for',starter,re.IGNORECASE) :
        wres.append('\t'*indent + str(newres[i])+'\n')
        indent +=1
    elif re.match('elif|else',starter,re.IGNORECASE):
        wres.append('\t'*(abs(indent-1)) + str(newres[i])+'\n' )
    else:
        wres.append(('\t'*indent) + str(newres[i])+'\n')
    

j = open("test.py", "w+")
for i in wres:
    j.write(i)
