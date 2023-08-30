import re
import os

os.system("cls")
f = open("test.algo", "r").readlines()
res = []
for i in f:
    i = re.sub(" +", " ", i)
    res.append(i.replace("\n", "").strip())

variables = []
for i, v in enumerate(res):
    if re.match("^(algorithme) ", v, re.IGNORECASE):
        variables = res[0:i]
        res = res[i::]
        break

tdo = []
tdnt = []
for i, v in enumerate(variables):
    if v == "#TDNT":
        tdnt = variables[i + 1 : :]
        tdo = variables[1:i]


if re.match("^(algorithme) .+", res[0], re.IGNORECASE):
    pass
else:
    raise Exception("declaration algorithme invalide")
if res[1].lower() != "debut":
    raise Exception("debut manquante")
if res[len(res) - 1].lower() != "fin":
    raise Exception(f"fin manquante : ligne {len(res)}")

res.pop(0)
res.pop(1)
res.pop()


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
    raise Exception(f"extra {name} at {start+1}")


# compress
for i in range(0, len(res)):
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


res = arraying(res)
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


def getParams(el):
    eltab = el.split(",")
    while "" in eltab:
        eltab.remove("")
    alls = []
    unchanges = []
    for i in eltab:
        i = re.sub(" +", " ", str(i))
        if i == " ":
            continue
        test = re.match(
            "(?P<name>@?[a-z]+([a-z]|[0-9]))*(:[a-z]+([a-z]|[0-9])*)?", i, re.IGNORECASE
        )
        name = test.group("name")
        if test and name:
            if name[0] != "@":
                unchanges.append(["__OLD" + test.group("name"), test.group("name")])
                alls.append(name)
            else:
                alls.append(name[1::])
        else:
            return False, False
    return alls, unchanges


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
    if newel:
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
        alls, unchages = getParams(newel.group("arguments"))
        if alls == []:
            return f"def {newel.group('name')} ():#{newel.group('returntype')}", []
        if unchages:
            return (
                f"def {newel.group('name')} ({','.join(alls)}):#{newel.group('returntype')}",
                unchages,
            )
        else:
            return False, False
    return False, False


def isProcedure(el):
    newel = re.match(
        "procedure[ ]+(?P<name>[a-z]([a-z]|[0-9])*)[ ]*\((?P<arguments>.*)\)",
        el,
        re.IGNORECASE,
    )
    if newel:
        alls, unchages = getParams(newel.group("arguments"))
        if alls == []:
            return f"def {newel.group('name')} ():", []
        if unchages:
            return f"def {newel.group('name')} ({','.join(alls)}):", unchages
        else:
            return False, False
    return False, False


def isTantque(el):
    newel = re.match("tantque[ ]+(?P<arguments>.*)", el, re.IGNORECASE)
    if newel:
        return f'while {newel.group("arguments")}:'
    else:
        return False


def isJusqua(el):
    newel = re.match("Jusqu'?a[ ]+(?P<arguments>.+)", el, re.IGNORECASE)
    if newel:
        return f'if ({newel.group("arguments")}):'
    else:
        return False


def isRepeter(el):
    newel = re.match("repeter[ ]*:?", el, re.IGNORECASE)
    if newel:
        return f"while True :"
    else:
        return False


for i in range(0, len(res)):
    res[i] = re.sub(" +", " ", res[i])
    starter = res[i].split(" ")[0].lower().strip() + " "

    res[i] = re.sub("<--", " = ", res[i], re.IGNORECASE)
    res[i] = re.sub("=", "==", res[i], re.IGNORECASE)
    res[i] = re.sub("====", "==", res[i], re.IGNORECASE)
    res[i] = re.sub("div", "//", res[i], re.IGNORECASE)
    res[i] = re.sub("\^", "**", res[i], re.IGNORECASE)
    res[i] = re.sub("([^a-z0-9])(Vrai)[^a-z0-9]", " True ", res[i], re.IGNORECASE)
    res[i] = re.sub("([^a-z0-9])(Faux)[^a-z0-9]", " False ", res[i], re.IGNORECASE)
    res[i] = re.sub("([^a-z0-9])(Vrai)$", " True ", res[i], re.IGNORECASE)
    res[i] = re.sub("^(Vrai)[^a-z0-9]", " True ", res[i], re.IGNORECASE)
    res[i] = re.sub("([^a-z0-9])(Faux)$", " False ", res[i], re.IGNORECASE)
    res[i] = re.sub("^(Faux)[^a-z0-9]", " False ", res[i], re.IGNORECASE)

    if re.match("^pour[ ]+", starter, re.IGNORECASE):
        if isBoucleFor(res[i]):
            newres.append(isBoucleFor(res[i]))
        else:
            print("pour invalide")
    elif re.match("^si[ ]+", starter, re.IGNORECASE):
        if isSi(res[i]):
            newres.append(isSi(res[i]))
        else:
            print("si invalide ")
    elif re.match("^sinonsi[ ]+", starter, re.IGNORECASE):
        try:
            if searchParent(i, "si") or (searchParent(i, "sinonsi")):
                newres.append(isSinonsi(res[i]))
            else:
                print("sinon invalide")
        except:
            print("sinon invalide")
    elif re.match("^sinon[ ]*:?", starter, re.IGNORECASE):
        try:
            if (searchParent(i, "si") or searchParent(i, "sinonsi")) and isSinon(
                res[i]
            ):
                newres.append(isSinon(res[i]))
            else:
                print("sinon invalide")
        except:
            print("sinon invalide")
    elif re.match("^fonction[ ]+", starter, re.IGNORECASE):
        a, b = isFonction(res[i])
        if a:
            newres.append(a)
            newres.append(b)
            for l in b:
                newres.append(l[0] + " = " + l[1])
        else:
            print("fonction invalide ")
    elif re.match("^procedure[ ]+", starter, re.IGNORECASE):
        a, b = isProcedure(res[i])
        if a and b:
            newres.append(a)
            newres.append(b)
            for l in b:
                newres.append(l[0] + " = " + l[1])
        else:
            print("procedure invalide ")
    elif re.match("^tant[ ]?que", starter, re.IGNORECASE):
        if isTantque(res[i]):
            newres.append(isTantque(res[i]))
        else:
            print("tantque invalide ")
    elif re.match("^jusqu'?(a|à)", starter, re.IGNORECASE):
        if isJusqua(res[i]):
            newres.append(isJusqua(res[i]))
            newres.append("break")
            newres.append("finsi")
        else:
            print(" Jusqu'a invalide ")
    elif re.match("^R(e|é)p(e|é)ter[ ]*", starter, re.IGNORECASE):
        if isRepeter(res[i]):
            newres.append(isRepeter(res[i]))
        else:
            print("repeter invalide ")
    elif re.match("^lire\(.+\)", starter, re.IGNORECASE):
        lire = re.match("^lire\((?P<stuff>.+)\)", res[i], re.IGNORECASE)
        if lire and lire.group("stuff"):
            if isVariable(lire.group("stuff")):
                newres.append(f'{lire.group("stuff")}= input()')
            else:
                print("lire Invalide")
    elif re.match("^retourner[ ]+", starter, re.IGNORECASE):
        test = re.match("^retourner[ ]+(?P<stuff>(.*))", res[i], re.IGNORECASE)
        if test:
            newres.append(f'return {test.group("stuff")}')
        else:
            newres.append(f"return ")
    else:
        newres.append(res[i])


while "" in newres:
    newres.remove("")


wres = []
for i in range(0, len(newres)):
    if newres[i] == "fin":
        forlater = ""
        if newres[i - 1].split(" ")[0] == "return":
            forlater = newres[i - 1]
            wres.pop()
        for k in range(i, -1, -1):
            if check(newres[k]) == False and re.match(
                "^def[ ]+", newres[k], re.IGNORECASE
            ):
                botargs = newres[k + 1]
                for l in botargs:
                    wres.append(l[1] + " = " + l[0])
                break
        if forlater != "":
            wres.append(forlater)
    wres.append(newres[i])
while True:
    test = True
    for i in range(0, len(wres)):
        if check(wres[i]):
            wres.pop(i)
            test = False
            break
    if test == True:
        break
while "" in wres:
    wres.remove("")

# writing
wres2 = []
predef = open("predefined.py", "r").readlines()
for i in predef:
    i = i.strip()
while "" in predef:
    predef.remove("")
for i in predef:
    wres2.append(i)

indent = 0
for i in range(0, len(wres)):
    wres[i] = re.sub(" +", " ", str(wres[i])).strip()
    starter = wres[i]
    if re.match("debut", starter, re.IGNORECASE):
        wres2.append("#" + "\t" * (indent - 1) + str(wres[i]) + "\n")
    elif re.match("finpour|finsi|fin|fintantque", starter, re.IGNORECASE):
        indent = abs(indent - 1)
        wres2.append("#" + "\t" * (indent) + str(wres[i]) + "\n")
    elif re.match("break", starter, re.IGNORECASE):
        wres2.append("\t" * (indent) + str(wres[i]) + "\n")
        indent = abs(indent - 1)
    elif re.match("if|while|def|for", starter, re.IGNORECASE):
        wres2.append("\t" * indent + str(wres[i]) + "\n")
        indent += 1
    elif re.match("elif|else", starter, re.IGNORECASE):
        wres2.append("\t" * (abs(indent - 1)) + str(wres[i]) + "\n")
    else:
        wres2.append(("\t" * indent) + str(wres[i]) + "\n")

tdo2 = {}
for i, v in enumerate(tdo):
    v = re.sub(" +", "", v)
    if v == "":
        continue
    keys = v.split(":")[0]
    val = v.split(":")[1]
    for j in keys:
        tdo2[j] = val


def createClass(enregistrement):
    classlist = []
    classlist.append(f"class {list(enregistrement.keys())[0]}:")
    enrdesc = dict(list(enregistrement.values())[0])
    for i, v in enumerate(enrdesc):
        classlist.append("\t" + v + "=" + 'None')
        #classlist.append("\t" + v + ":" + enrdesc[v])
    return classlist


tableau = []
enregistrement = []
enrnames = []
tabnames = []
for i, v in enumerate(tdnt):
    v = v.strip()
    if v in ["fin", "debut", ""]:
        continue
    if (v.find(":") == -1) and (v[0:8] != "tableau "):
        estr = f"declaration d'objet invalide dans TDNT ligne {i} :{v} "
        raise Exception(estr)

    key = v.strip().split(":")[0].strip()
    value = v.strip().split(":")[1].strip()

    if value == "enregistrement":
        for j in range(i, len(tdnt)):
            if tdnt[j].strip() == "fin":
                details = tdnt[i : j + 1][2:-1]
                detailsdict = {}
                for k in details:
                    if k in ["fin", "debut", ""]:
                        continue
                    detailsdict[k.split(":")[0]] = k.split(":")[1]
                enregistrement.append(createClass({key: detailsdict}))
                enregistrement.append('\n')
                enrnames.append(key.strip())
                break
    elif value[0:8] == "tableau ":
        s = value.split(" ")
        tabnames.append(key.strip())
        tableau.append({key: [s[-2], s[-1]]})


# writing
wres2 = []




predef = open("predefined.py", "r").readlines()
for i in predef:
    i = i.strip()
for i in predef:
    wres2.append(i)
    
    
for i in enregistrement:
    wres2.append('\n'.join(i))
for i,v in enumerate(tableau): 
    tab = [] 
    tabname = list(tableau[i].keys())[0]
    tablength  = int(list(tableau[i].values())[0][0].strip())
    type = list(tableau[i].values())[0][1].strip()
    if type=='entier':
        for j in range(0,tablength+1):
            tab.append(0)
    elif type in ['chaine','caractere'] :
        for j in range(0,tablength+1):
            tab.append('')
    elif type=='reel':
        for j in range(0,tablength+1):
            tab.append(0.0)
    elif type =='booleen':
        for j in range(0,tablength+1):
            tab.append(False)
    elif type in tabnames:
        for j in range(0,tablength+1):
            tab.append([])
    elif type in enrnames:
        for j in range(0,tablength+1):
            tab.append(type+'()')
        wres2.append(f'{tabname} = [{",".join(tab)}]\n')   
        continue
    wres2.append(f'{tabname} = {tab}\n') 

for i in range(0, len(wres)):
    wres[i] = re.sub(" +", " ", str(wres[i])).strip()
    starter = wres[i]
    if re.match("debut", starter, re.IGNORECASE):
        wres2.append("#" + "\t" * (indent - 1) + str(wres[i]) + "\n")
    elif re.match("finpour|finsi|fin|fintantque", starter, re.IGNORECASE):
        indent = abs(indent - 1)
        wres2.append("#" + "\t" * (indent) + str(wres[i]) + "\n")
    elif re.match("break", starter, re.IGNORECASE):
        wres2.append("\t" * (indent) + str(wres[i]) + "\n")
        indent = abs(indent - 1)
    elif re.match("if|while|def|for", starter, re.IGNORECASE):
        wres2.append("\t" * indent + str(wres[i]) + "\n") 
        indent += 1
    elif re.match("elif|else", starter, re.IGNORECASE):
        wres2.append("\t" * (abs(indent - 1)) + str(wres[i]) + "\n")
    else:
        wres2.append(("\t" * indent) + str(wres[i]) + "\n")

f = open("test.py", "w+")
f.writelines(wres2)
