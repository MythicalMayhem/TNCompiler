import re
import os
import subprocess

os.system("cls")
f = open("test.algo", "r").readlines()
res = []
for i in f:
    i = re.sub("è|é|ê|ë", "e", i)
    i = re.sub("à", "a", i)
    res.append(re.sub(" +", " ", i).replace("\n", "").strip())


for i in range(len(res) - 1, -1, -1):
    if res[i].strip() == "fin":
        res = res[0 : i + 1]
        break

tdo = []
tdnt = []

for i, v in enumerate(res):
    if re.match("^(algorithme) ", v, re.IGNORECASE):
        variables = res[0:i]
        res = res[i::]
        for i, v in enumerate(variables):
            if v == "#TDO":
                tdo = variables[i + 1 : :]
                tdnt = variables[1:i]
        break


if re.match("^(algorithme) .+", res[0], re.IGNORECASE):
    res[0] = "#" + res[0]
else:
    raise Exception("declaration algorithme invalide")

if res[1].lower() != "debut":
    raise Exception("debut manquante")
if res[len(res) - 1].lower() != "fin":
    raise Exception(f"fin manquante : ligne {len(res)}")


res.pop(0)
res.pop(0)
res.pop()


# compress
def searchParent(start, name):
    for k in range(start, -1, -1):
        if str(res[k]).startswith("["):
            continue
        if re.match(name, res[k], re.IGNORECASE):
            return k
    estr = f"extra {name} at {start+1}"
    raise Exception(estr)


def compressionalgo(items):
    if re.match("finpour", items, re.IGNORECASE):
        return searchParent(i, "^pour[ ]+")
    elif re.match("finsi", items, re.IGNORECASE):
        return searchParent(i, "^si[ ]+")
    elif re.match("^jusqu'?(a|à)", items, re.IGNORECASE):
        return searchParent(i, "^R(e|é)p(e|é)ter[ ]*")
    elif re.match("fin[-_]?tant[-_]?que", items, re.IGNORECASE):
        return searchParent(i, "^tant[ ]?que")
    elif re.match("fin", items, re.IGNORECASE):
        return searchParent(i, "^(fonction|proc(e|é)dure) ")


def compressor(LIST):
    compressed = LIST.copy()
    for i in range(0, len(compressed) - 1):
        search = compressionalgo(compressed[i].strip())
        if search:
            compressed[search] = compressed[search : i + 1]
            for j in range(search + 1, i + 1):
                compressed[j] = ""


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
    changes = []
    for i in eltab:
        i = re.sub(" +", " ", str(i))
        if i == " ":
            continue
        test = re.match(
            "(?P<name>^@?[a-z_]+([a-z0-9_]))*(:[a-z_]+([a-z0-9_])*)?$", i, re.IGNORECASE
        )
        name = test.group("name")
        if test and name:
            if name[0] != "@":
                unchanges.append(["__OLD" + test.group("name"), test.group("name")])
                alls.append(name)
            else:
                changes.append(test.group("name")[1::])
                alls.append(name[1::])
        else:
            return False, False, False
    return alls, unchanges, changes


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
        "fonction[ ]+(?P<name>[a-z]([a-z]|[0-9])*)[ ]*\((?P<arguments>.*)\)[ ]*:[ ]*(?P<returntype>[a-z]+[0-9]*)",
        el,
        re.IGNORECASE,
    )
    if newel:
        alls, unchanges, changes = getParams(newel.group("arguments"))
        if alls == []:
            return f"def {newel.group('name')} ():#{newel.group('returntype')}", [], []
        if unchanges or changes:
            return (
                f"def {newel.group('name')} ({','.join(alls)}):#{newel.group('returntype')}",
                unchanges,
                changes,
            )
        else:
            return False, False, False
    return False, False, False


def isProcedure(el):
    newel = re.match(
        "procedure[ ]+(?P<name>[a-z]([a-z]|[0-9])*)[ ]*\((?P<arguments>.*)\)",
        el,
        re.IGNORECASE,
    )
    if newel:
        alls, unchanges, changes = getParams(newel.group("arguments"))
        if alls == []:
            return f"def {newel.group('name')} ():", [], []
        if unchanges or changes:
            return f"def {newel.group('name')} ({','.join(alls)}):", unchanges, changes
        else:
            return False, False, False
    return False, False, False


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


def isLire(el):
    lire = re.match("^lire\((?P<stuff>.+)\)", res[i], re.IGNORECASE)
    if lire and lire.group("stuff"):
        if isVariable(lire.group("stuff")):
            inptstr = [
                f'if type({lire.group("stuff")}) is bool :',
                f'{lire.group("stuff")}= bool(input())',
                f'elif type({lire.group("stuff")}) is float:',
                f'{lire.group("stuff")}= float(input())',
                f'elif type({lire.group("stuff")}) is int:',
                f'{lire.group("stuff")}= int(input())',
                f"else:",
                f'{lire.group("stuff")}= str(input())',
                f"finsi",
            ]
            return inptstr
        else:
            return False
    else:
        return False


def getSpanTable(start, ende):
    begin = int(ord(start))
    ender = int(ord(ende))
    count = int(begin)
    tab = []
    for i in range(begin, ender + 1):
        tab.append(chr(i))
    return tab


for i in range(0, len(res)):
    res[i] = re.sub("([^:]*)(:+)$", r"\1", res[i])
    res[i] = re.sub("\[A\.\.Z\]", f" {getSpanTable('A','Z')} ", res[i])
    res[i] = re.sub("\[a\.\.z\]", f" {getSpanTable('a','z')} ", res[i])
    res[i] = re.sub("\[0\.\.9\]", f" {getSpanTable('0','9')} ", res[i])
    res[i] = re.sub("selon (.+)", r"match \1 :", res[i],re.IGNORECASE)
    res[i] = re.sub("[^a-z0-9_]non[^a-z0-9_]", " not ", res[i], re.IGNORECASE)
    res[i] = re.sub("[^a-z0-9_]dans[^a-z0-9_]", " in ", res[i], re.IGNORECASE)
    res[i] = re.sub(" +", " ", res[i])
    res[i] = re.sub("<--", " = ", res[i], re.IGNORECASE)
    res[i] = re.sub("=", "==", res[i], re.IGNORECASE)
    res[i] = re.sub("====", "==", res[i], re.IGNORECASE)
    res[i] = re.sub(" div ", " // ", res[i], re.IGNORECASE)
    res[i] = re.sub("\^", "**", res[i], re.IGNORECASE)
    res[i] = re.sub(
        "^(Vrai)[^a-z0-9_]|(([^a-z0-9_])(Vrai)[^a-z0-9_]|([^a-z0-9_])(Vrai)$)",
        " True ",
        res[i],
        re.IGNORECASE,
    )
    res[i] = re.sub(
        "^(Faux)[^a-z0-9_]|(([^a-z0-9_])(Faux)[^a-z0-9_]|([^a-z0-9_])(Faux)$)",
        " False ",
        res[i],
        re.IGNORECASE,
    )

    starter = res[i].split(" ")[0].lower().strip() + " "
    if re.match("^pour[ ]+", starter, re.IGNORECASE):
        if isBoucleFor(res[i]):
            newres.append(isBoucleFor(res[i]))
            newres.append("pass")
        else:
            print("pour invalide")
    elif re.match("^si[ ]+", starter, re.IGNORECASE):
        if isSi(res[i]):
            newres.append(isSi(res[i]))
            newres.append("pass")
        else:
            print("si invalide ")
    elif re.match("^sinonsi[ ]+", starter, re.IGNORECASE):
        try:
            if searchParent(i, "si") or (searchParent(i, "sinonsi")):
                newres.append(isSinonsi(res[i]))
                newres.append("pass")
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
                newres.append("pass")
            else:
                print("sinon invalide")
        except:
            print("sinon invalide")
    elif re.match("^((cas[ ])+(?P<start>.+)):?(?P<other>)?", res[i], re.IGNORECASE):
        temp = re.match("^((cas[ ])+(?P<start>.+)+):?(?P<other>)?", res[i], re.IGNORECASE)
        if temp and temp.group('start') :
            print(temp.groups())
            newres.append('case'+temp.group('start')+':')
        if temp.group('other'):
            newres.append(temp.group('other'))
    elif re.match("^fonction[ ]+", starter, re.IGNORECASE):
        a, b, c = isFonction(res[i])
        if a:
            newres.append(a)
            newres.append("pass")
            newres.append(b)
            newres.append(c)
            for l in b:
                newres.append(l[0] + " = " + l[1])

        else:
            print("fonction invalide ")
    elif re.match("^procedure[ ]+", starter, re.IGNORECASE):
        a, b, c = isProcedure(res[i])
        if a:
            newres.append(a)
            newres.append("pass")
            newres.append(b)
            newres.append(c)
            for l in b:
                newres.append(l[0] + " = " + l[1])

        else:
            print("procedure invalide ")
    elif re.match("^tant[ ]?que", starter, re.IGNORECASE):
        if isTantque(res[i]):
            newres.append(isTantque(res[i]))
            newres.append("pass")
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
            newres.append("pass")
        else:
            print("repeter invalide ")
    elif re.match("^lire\(.+\)", starter, re.IGNORECASE):
        if isLire(res[i]):
            for it in isLire(res[i]):
                newres.append(it)
        else:
            print("lire invalide ")
    elif re.match("^retourner[ ]+", starter, re.IGNORECASE):
        test = re.match("^retourner[ ]+(?P<stuff>(.*))", res[i], re.IGNORECASE)
        if test:
            newres.append(f'return {test.group("stuff")}')
        else:
            newres.append(f"return ")
    else:
        newres.append(res[i])


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
                botargs = newres[k + 2]
                for l in botargs:
                    wres.append(l[1] + " = " + l[0])

                botargs2 = newres[k + 3]
                for l in botargs2:
                    wres.append(f'globals()[str("{l}")]=' + l)
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


# tdnt
tabtemplates = {}
mattemplates = {}
enregistrement = []
enrnames = []


def createVar(name, type):
    if type == "entier":
        return f"{name} = 0"
    elif type in ["chaine", "caractere"]:
        return f'{name} = ""'
    elif type == "reel":
        return f"{name} = 0.0"
    elif type == "booleen":
        return f"{name} = False"
    elif type in enrnames:
        return f'{name} = {type} + "()"'


def createClass(enregistrement):
    classlist = []
    classlist.append(f"class {list(enregistrement.keys())[0]}:\n")
    enrdesc = dict(list(enregistrement.values())[0])
    for i, v in enumerate(enrdesc):
        classlist.append(f"\t{createVar(v,enrdesc[v])} \n")
    classlist.append("\n")
    return classlist


def createTable(name, length, type):
    tab = []
    if type == "entier":
        for j in range(0, length + 1):
            tab.append("0")
    elif type in ["chaine", "caractere"]:
        for j in range(0, length + 1):
            tab.append("")
    elif type == "reel":
        for j in range(0, length + 1):
            tab.append("0.0")
    elif type == "booleen":
        for j in range(0, length + 1):
            tab.append(False)
    elif type in list(tabtemplates.values()):
        for j in range(0, length + 1):
            tab.append([])
    elif type in enrnames:
        for j in range(0, length + 1):
            tab.append(type + "()")
    return f"{name} = [{','.join(tab)}]\n"


def createMatrix(name, row, col, type):
    if type == "entier":
        return f"{name} = np.array([([int()]*{col})]*{row})"
    elif type in ["chaine", "caractere"]:
        return f"{name} = np.array([([str()]*{col})]*{row})"
    elif type == "reel":
        return f"{name} = np.array([([float()]*{col})]*{row})"
    elif type == "booleen":
        return f"{name} = np.array([([bool()]*{col})]*{row})"
    elif type in enrnames:
        return f"{name} = np.array([([{type}()]*{col})]*{row})"
    else:
        return f"{name} = np.array([([{type}]*{col})]*{row})"


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
                enrnames.append(key.strip())
                break
    elif re.match(
        "^tableau[ ]+de[ ]+(?P<long>[0-9]+)[ ]+(?P<type>[0-9a-z]+)$",
        value.strip(),
        re.IGNORECASE,
    ):
        s = re.match(
            "^tableau[ ]+de[ ]+(?P<long>[0-9]+)[ ]+(?P<type>[0-9a-z]+)$",
            value,
            re.IGNORECASE,
        )
        if s and s.group("long") and s.group("type"):
            tabtemplates[key] = [int(s.group("long")), s.group("type")]
    elif re.match(
        "^(tableau|matrice)[ ]+de[ ]+(((?P<rows1>[0-9]+)[ ]+lignes \* (?P<cols1>[0-9]+)[ ]+colonnes)|((?P<cols2>[0-9]+)[ ]+colonnes) \* (?P<rows2>[0-9]+)[ ]+lignes)[ ]*(?P<type>[a-z][0-9a-z]*)$",
        value.strip(),
        re.IGNORECASE,
    ):
        s = re.match(
            "^(tableau|matrice)[ ]+de[ ]+(((?P<rows1>[0-9]+)[ ]+lignes \* (?P<cols1>[0-9]+)[ ]+colonnes)|((?P<cols2>[0-9]+)[ ]+colonnes) \* (?P<rows2>[0-9]+)[ ]+lignes)[ ]*(?P<type>[a-z][0-9a-z]*)$",
            value.strip(),
            re.IGNORECASE,
        )
        if s:
            if s.group("rows1") and s.group("cols1") and s.group("type"):
                mattemplates[key] = [
                    int(s.group("rows1")),
                    int(s.group("cols1")),
                    s.group("type"),
                ]
            elif s.group("rows2") and s.group("cols2") and s.group("type"):
                mattemplates[key] = [
                    int(s.group("rows2")),
                    int(s.group("cols2")),
                    s.group("type"),
                ]


# tdo
tdo2 = {}
for i, v in enumerate(tdo):
    v = v.strip()
    if v == "":
        continue
    keys = v.split(":")[0].strip()
    val = v.split(":")[1].strip()
    for j in keys:
        tdo2[j] = val
tdo3 = []
for i in tdo2:
    if tdo2[i] in list(tabtemplates.keys()):
        tbl = createTable(i, int(tabtemplates[tdo2[i]][0]), tabtemplates[tdo2[i]][1])
        tdo3.append(tbl)
    elif tdo2[i] in list(mattemplates.keys()):
        tbl = createMatrix(
            i,
            int(mattemplates[tdo2[i]][0]),
            int(mattemplates[tdo2[i]][1]),
            mattemplates[tdo2[i]][2],
        )
        tdo3.append(tbl)
    elif re.match(
        "^tableau[ ]+de[ ]+(?P<long>[0-9]+)+[ ]+(?P<type>[0-9a-z]+)$",
        tdo2[i],
        re.IGNORECASE,
    ):
        s = re.match(
            "^tableau[ ]+de[ ]+(?P<long>[0-9]+)+[ ]+(?P<type>[0-9a-z]+)$",
            tdo2[i],
            re.IGNORECASE,
        )
        if s and s.group("long") and s.group("type"):
            tbl = createTable(i, int(s.group("long")), s.group("type"))
            tdo3.append(tbl)
    elif re.match(
        "^(tableau|matrice)[ ]+de[ ]+(((?P<rows1>[0-9]+)[ ]+lignes \* (?P<cols1>[0-9]+)[ ]+colonnes)|((?P<cols2>[0-9]+)[ ]+colonnes) \* (?P<rows2>[0-9]+)[ ]+lignes)[ ]*(?P<type>[a-z][0-9a-z]*)$",
        tdo2[i].strip(),
        re.IGNORECASE,
    ):
        s = re.match(
            "^(tableau|matrice)[ ]+de[ ]+(((?P<rows1>[0-9]+)[ ]+lignes \* (?P<cols1>[0-9]+)[ ]+colonnes)|((?P<cols2>[0-9]+)[ ]+colonnes) \* (?P<rows2>[0-9]+)[ ]+lignes)[ ]*(?P<type>[a-z][0-9a-z]*)$",
            tdo2[i].strip(),
            re.IGNORECASE,
        )
        if s:
            if (s.group("rows1") and s.group("cols1")) and s.group("type"):
                tbl = createMatrix(
                    int(s.group("rows1")), int(s.group("cols1")), s.group("type")
                )
                tdo3.append(tbl)
            elif (s.group("rows2") and s.group("cols2")) and s.group("type"):
                tbl = createMatrix(
                    int(s.group("rows2")), int(s.group("cols2")), s.group("type")
                )
                tdo3.append(tbl)
    else:
        if createVar(i.strip(), tdo2[i].strip()):
            tdo3.append(createVar(i.strip(), tdo2[i].strip()) + "\n")
        else:
            tdo3.append(i + f"={tdo2[i]}\n")

# writing
wres2 = []
indent = 0
def zeroclamp(n):
    if n<0:
        return 0
    return n
for i in range(0, len(wres)):
    wres[i] = re.sub(" +", " ", str(wres[i])).strip()
    starter = wres[i].strip()
    if re.match("d.but", starter, re.IGNORECASE):
        wres2.append("#" + "\t" * (indent - 1) + str(wres[i]) + "\n")
    elif re.match("^(fin[-_ ]?selon)", starter, re.IGNORECASE):
        indent = zeroclamp(indent - 2)
        wres2.append("#" + "\t" * (indent) + str(wres[i]) + "\n")
    elif re.match(
        "^((fin[-_ ]?pour)|(fin[-_ ]?si)|(fin)|(fin[-_ ]?tant[-_ ]?que))",
        starter,
        re.IGNORECASE,
    ):
        indent = zeroclamp(indent - 1)
        wres2.append("#" + "\t" * (indent) + str(wres[i]) + "\n")
  
    elif re.match("break", starter, re.IGNORECASE):
        wres2.append("\t" * (indent) + str(wres[i]) + "\n")
        indent = zeroclamp(indent - 1)
    elif re.match("^(if|while|def|for)", starter, re.IGNORECASE):
        wres2.append("\t" * indent + str(wres[i]) + "\n")
        indent += 1
    elif re.match("^match", starter, re.IGNORECASE):
        wres2.append("\t" * indent + str(wres[i]) + "\n")
        indent += 2
    elif re.match("elif|else|case", starter, re.IGNORECASE):
        wres2.append("\t" * (zeroclamp(indent - 1)) + str(wres[i]) + "\n")
    else:
        wres2.append(("\t" * indent) + str(wres[i]) + "\n")


predef = open("predefined.py", "r").readlines()
final = []
final += predef
final += arraying(enregistrement)
final += tdo3
final += wres2

f = open("test.py", "w+")
f.writelines(final)
f.close()

subprocess.call("python test.py", shell=True)
