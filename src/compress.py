import re 

def arraying(pig):
    L = pig
    while isinstance(L,list):
        for i in range(0, len(L)):
            if isinstance(L[i],list):
                item = L[i]
                L.remove(L[i])
                for j in range(len(item) - 1, -1, -1):
                    L.insert(i, item[j])
        test = True
        for i in range(0, len(L)):
            if isinstance(L[i],list) == True:
                test = False
        if test:
            break
    return L


def searchParent(start, lookfor,where):

    for k in range(start, -1, -1):
        line = list(where[k].values())[0]
        if str(line).startswith("["):
            continue
        if re.match(lookfor, line, re.IGNORECASE):
            return k
    estr = f"extra {lookfor} at {start+1}"
    raise Exception(estr)


def compressionalgo(matcher,start,where):
    if re.match("^fin[-_ ]?pour", matcher, re.IGNORECASE):
        return searchParent(start, "^pour[ ]+",where)
    elif re.match("^fin[-_ ]?si", matcher, re.IGNORECASE):
        return searchParent(start, "^si[ ]+",where)
    elif re.match("^jusqu'?(a|à)", matcher, re.IGNORECASE):
        return searchParent(start, "^R(e|é)p(e|é)ter[ ]*",where)
    elif re.match("fin[-_ ]?tant[-_ ]?que", matcher, re.IGNORECASE):
        return searchParent(start, "^selon",where)
    elif re.match("fin[-_ ]selon", matcher, re.IGNORECASE):
        return searchParent(start, "^(fonction|proc(e|é)dure) ",where)
    elif re.match("fin", matcher, re.IGNORECASE):
        return searchParent(start, "^(fonction|proc(e|é)dure) ",where)


def run(LIST):
    tocompress = LIST.copy() 
    for i in range(0, len(tocompress)):
        value = list(tocompress[i].values())[0]
        search = compressionalgo(value.strip(),i,tocompress)
        if search:
            tocompress[search] = tocompress[search : i + 1]
            while {} in tocompress[search]:
                tocompress[search].remove({})
            for j in range(search + 1, i + 1):
                tocompress[j] = {}
    while {} in tocompress:
        tocompress.remove({}) 

