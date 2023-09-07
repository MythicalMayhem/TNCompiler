import re
from compress import searchParent 

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
            "(?P<name>^@?[a-z_]+([a-z0-9_])*)(:[a-z_]+([a-z0-9_])*)?$", i, re.IGNORECASE
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
    if isVariable(index) and isinstance(start, list) and isinstance(end, list):
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


def isLire(el,key):
    lire = re.match("^lire\((?P<stuff>.+)\)", el, re.IGNORECASE)
    if lire and lire.group("stuff"):
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
 
def getSpanTable(start, ende):
    begin = int(ord(start))
    ender = int(ord(ende)) 
    tab = []
    for i in range(begin, ender + 1):
        tab.append(chr(i))
    return tab

def translateLines(res):
    newres = []
    for i,v in enumerate(res): 
        key = list(res[i].keys())[0] 
        res[i][key] = re.sub("([^:]*)(:+)$", r"\1", res[i][key])
        res[i][key] = re.sub("selon (.+)", r"match \1 :",res[i][key], re.IGNORECASE)
        kids = res[i][key].strip().split('"') 
        
        for j in range(0,len(kids),2): 
            kids[j] = re.sub("\[A\.\.Z\]", f" {getSpanTable('A','Z')} ", kids[j])
            kids[j] = re.sub("\[a\.\.z\]", f" {getSpanTable('a','z')} ", kids[j])
            kids[j] = re.sub("\[0\.\.9\]", f" {getSpanTable('0','9')} ", kids[j])
            kids[j] = re.sub("[^a-z0-9_]non[^a-z0-9_]", " not ", kids[j], re.IGNORECASE)
            kids[j] = re.sub("[^a-z0-9_]et[^a-z0-9_]", " and ",  kids[j], re.IGNORECASE)
            kids[j] = re.sub("[^a-z0-9_]ou[^a-z0-9_]", " or ",   kids[j], re.IGNORECASE)
            kids[j] = re.sub("[^a-z0-9_]dans[^a-z0-9_]", " in ", kids[j], re.IGNORECASE)
            kids[j] = re.sub(" +", " ",      kids[j])
            kids[j] = re.sub("=", "==",      kids[j], re.IGNORECASE)
            kids[j] = re.sub("====", "==",   kids[j], re.IGNORECASE)
            kids[j] = re.sub(" div ", " // ",kids[j], re.IGNORECASE)
            kids[j] = re.sub(" mod ", " % ",kids[j], re.IGNORECASE)
            kids[j] = re.sub("\^", "**",     kids[j], re.IGNORECASE)
            kids[j] = re.sub("<--", " = ",   kids[j], re.IGNORECASE)
        res[i][key] = '"'.join(kids)
        starter = res[i][key].split(" ")[0].lower().strip() + " "
        if re.match("^pour[ ]+", starter, re.IGNORECASE):
            test = isBoucleFor(res[i][key])
            if test:
                newres.append(test+'#'+str(key))
                newres.append("pass"+'#'+str(key))
            else:
                print("pour invalide")
        elif re.match("^si[ ]+", starter, re.IGNORECASE):
            test = isSi(res[i][key])
            if test:
                newres.append(test+'#'+str(key))
                newres.append("pass"+'#'+str(key))
            else:
                print("si invalide ")
        elif re.match("^sinonsi[ ]+", starter, re.IGNORECASE):
            test = isSinonsi(res[i][key])
            if test:
                newres.append(test+'#'+str(key))
                newres.append("pass"+'#'+str(key))
            else:  
                print("sinonsi invalide ")
        elif re.match("^sinon[ ]*:?", starter, re.IGNORECASE):
            test = isSinon(res[i][key])
            if test:
                newres.append(test+'#'+str(key))
                newres.append("pass"+'#'+str(key))
            else:  
                print("sinon invalide ")
        elif re.match("^((cas[ ])+(?P<start>.+)):?(?P<other>)?", res[i][key], re.IGNORECASE):
            temp = re.match(
                "^((cas[ ])+(?P<start>.+)+):?(?P<other>)?", res[i][key], re.IGNORECASE
            )
            if temp and temp.group("start"):
                newres.append("case" + temp.group("start") + ":"+'#'+str(key))
            if temp.group("other"):
                newres.append(temp.group("other")+'#'+str(key))
        
        elif re.match("^tant[ ]?que", starter, re.IGNORECASE):
            test = isTantque(res[i][key])
            if test:
                newres.append(test+'#'+str(key))
                newres.append("pass"+'#'+str(key))
            else:
                print("tantque invalide ")
        elif re.match("^jusqu'?(a|à)", starter, re.IGNORECASE):
            test = isJusqua(res[i][key])
            if test:
                newres.append(test+'#'+str(key))
                newres.append("break"+'#'+str(key))
                newres.append("finsi"+'#'+str(key))
            else:
                print(" Jusqu'a invalide ")
        elif re.match("^R(e|é)p(e|é)ter[ ]*", starter, re.IGNORECASE):
            test = isRepeter(res[i][key])
            if test:
                newres.append(test+'#'+str(key))
                newres.append("pass"+'#'+str(key))
            else:
                print("repeter invalide ")
        elif re.match("^fonction[ ]+", starter, re.IGNORECASE):
            a, b, c = isFonction(res[i][key]+'#'+str(key))
            if a:
                newres.append(a+'#'+str(key))
                newres.append("pass"+'#'+str(key))
                newres.append(b+'#'+str(key))
                newres.append(c+'#'+str(key))
                for l in b:
                    newres.append(l[0] + " = " + l[1]+'#'+str(key))

            else:
                print("fonction invalide ")
        elif re.match("^procedure[ ]+", starter, re.IGNORECASE):
            a, b, c = isProcedure(res[i][key])
            if a:
                newres.append(a+'#'+str(key))
                newres.append("pass"+'#'+str(key))
                newres.append(b+'#'+str(key))
                newres.append(c+'#'+str(key))
                for l in b:
                    newres.append(l[0] + " = " + l[1]+'#'+str(key))

            else:
                print("procedure invalide ")
        elif re.match("^lire\(.+\)", starter, re.IGNORECASE):
            test = isLire(res[i][key],str(key))
            if test:
                for it in test:
                    newres.append(it+'#'+str(key))
            else:
                print("lire invalide ")
        elif re.match("^retourner[ ]+", starter, re.IGNORECASE):
            test = re.match("^retourner[ ]+(?P<stuff>(.*))", res[i][key], re.IGNORECASE)
            if test:
                newres.append(f'return {test.group("stuff")}'+'#'+str(key))
            else:
                newres.append(f"return ")
        else:
            newres.append(res[i][key]+'#'+str(key))
    
    wres = []
    for i in range(0, len(newres)):
        if newres[i] == "fin":
            forlater = ""
            if newres[i - 1].split(" ")[0] == "return":
                forlater = newres[i - 1]
                wres.pop()
            for k in range(i, -1, -1):
                if isinstance(newres[k],list) == False and re.match(
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
            if isinstance(wres[i],list):
                wres.pop(i)
                test = False
                break
        if test == True:
            break
    return wres