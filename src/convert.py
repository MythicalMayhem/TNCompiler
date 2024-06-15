import re 
import syntax as stx

def getSpanTable(start, ende):
    begin = int(ord(start))
    ender = int(ord(ende))
    tab = []
    for i in range(begin, ender + 1): tab.append(chr(i))
    return tab

def replacement(el):
    el1 = el
    el1 = re.sub("\[A\.\.Z\]", f" {getSpanTable('A','Z')} ", el1)
    el1 = re.sub("\[a\.\.z\]", f" {getSpanTable('a','z')} ", el1)
    el1 = re.sub("\[0\.\.9\]", f" {getSpanTable('0','9')} ", el1)
    el1 = re.sub("[^a-z0-9_]non[^a-z0-9_]", " not ", el1, re.IGNORECASE)
    el1 = re.sub("[^a-z0-9_]et[^a-z0-9_]", " and ", el1, re.IGNORECASE)
    el1 = re.sub("[^a-z0-9_]ou[^a-z0-9_]", " or ", el1, re.IGNORECASE)
    el1 = re.sub("[^a-z0-9_]dans[^a-z0-9_]", " in ", el1, re.IGNORECASE)
    el1 = re.sub(" +", " ", el1)
    el1 = re.sub("=", "==", el1, re.IGNORECASE) 
    el1 = re.sub(" div ", " // ", el1, re.IGNORECASE)
    el1 = re.sub(" mod ", " % ", el1, re.IGNORECASE)
    el1 = re.sub("\^", "**", el1, re.IGNORECASE) 

    return el1
def replaceInString(el):
    opened = None
    start = 0
    end = len(el)
    quoted = []
    legit = []
    full = ""
    for i in range(0, len(el)):
        item = el[i].strip()
        before = 0
        if i > 0: before = i - 1 

        if (item == '"' or item == "'") and el[before] != "\\":
            if opened == None:
                opened = i
                end = i - 1
                full += replacement(el[start : end + 1])
            elif el[opened] == item:
                quoted.append([opened, i])
                legit.append([start, end])
                full += el[opened : i + 1]
                start = i + 1
                end = len(el) - 1
                opened = None
    legit.append([start, end])
    full += replacement(el[start : end + 1])
    if opened != None: exit("unformatted String ")

    return full

def read(lines,start,end):
    jdid = []
    for i in range(start+1,end-1): 
        line = lines[i].strip()
        line = replaceInString(line)
        line = re.sub("([^:]*)(:+)$", r"\1", line)
        starter =  line.split(" ")[0].lower().strip() + " "

        if re.match("(.*)[<\--](.*)", line, re.IGNORECASE):
            print('ggggg')
            test = stx.assignment(line)
            if test : jdid.append(f'{test}#{str(len(jdid))} \n\tpass#{str(len(jdid)+1)}')
            else    : exit(f"assignment invalide line {i}")

        elif re.match("^pour[ ]+", starter, re.IGNORECASE):
            test = stx.pour(line)
            if test : jdid.append(f'{test}#{str(len(jdid))} \n\tpass#{str(len(jdid)+1)}')
            else    : exit(f"pour invalide line {i} ")

        elif re.match("^si[ ]+", starter, re.IGNORECASE):
            test = stx.si(line)
            if test: jdid.append(f'{test}#{str(len(jdid))} \n\tpass#{str(len(jdid)+1)}')
            else: exit(f"si invalide line {i} ")

        elif re.match("^sinonsi[ ]+", starter, re.IGNORECASE):
            test = stx.sinonsi(line)
            if test:jdid.append(f'{test}#{str(len(jdid))} \n\tpass#{str(len(jdid)+1)}')
            else: exit(f"sinonsi invalide line {i} ")

        elif re.match("^sinon[ ]*:?", starter, re.IGNORECASE):
            test = stx.sinon(line)
            if test:jdid.append(f'{test}#{str(len(jdid))} \n\tpass#{str(len(jdid)+1)}')
            else: exit(f"sinon invalide line {i} ")

        elif re.match("^tant[ ]?que", starter, re.IGNORECASE):
            test = stx.tantque(line)
            if test:jdid.append(f'{test}#{str(len(jdid))} \n\tpass#{str(len(jdid)+1)}')
            else: exit(f"tantque invalide line {i} ")

        elif re.match("^jusqu'?(a|à)", starter, re.IGNORECASE):
            test = stx.jusqua(line)
            if test:
                jdid.append(f'{test}#{str(len(jdid))}\n\tbreak#{str(len(jdid)+1)}')
                jdid.append("finsi" + "#" + str(len(jdid)))
            else: exit(f"Jusqu'a invalide line {i} ")

        elif re.match("^R(e|é)p(e|é)ter[ ]*", starter, re.IGNORECASE):
            test = stx.repeter(line)
            if test: jdid.append(f'{test}#{str(len(jdid))} \n\tpass#{str(len(jdid)+1)}')
            else: exit(f"repeter invalide line {i} ")
        else : jdid.append(line)
    print(jdid)
    return jdid