import re 

def alphanum(ch):
    l = ch.lower()
    test = True
    if ("a" <= l[0] <= "z") == False: return False
    for i in l: 
        if (("a" <= i <= "z") or ( "0" <= i <= "9")) == False:return False
    return test

def assignment(ch):
    ch = ch.split('<--')
    varname = ch[0].strip()
    val = ''.join( ch[1:])
    print(varname,val,alphanum(varname))
    if alphanum(varname) and val.strip() != '':
        return f'{varname} = {val}'
    else : return False

def pour(ch):
    ch = ch.split(" ")[1:-1]
    index, start, end = 0, 0, 0
    for i in range(0, len(ch)):
        if ch[i] == "de": index = i
        if ch[i] == "a" : start = i

    index, start, end = ch[0:index], ch[index + 1 : start], ch[start + 1 : len(ch)]
    if len(index) > 1: return False 
    if alphanum(index[0]) and isinstance(start, list) and isinstance(end, list): return f'for {index[0]} in range({" ".join(start)},{" ".join(end)}):'
    else: return False

def tantque(el):
    ch = re.match("tantque[ ]+(?P<arguments>.*)", el, re.IGNORECASE)
    if ch: return f'while {ch.group("arguments")}:'
    else: return False


def jusqua(el):
    ch = re.match("Jusqu'?a[ ]+(?P<arguments>.+)", el, re.IGNORECASE)
    if ch: return f'if ({ch.group("arguments")}):'
    else: return False


def repeter(el):
    ch = re.match("repeter[ ]*:?", el, re.IGNORECASE)
    if ch: return f"while True :"
    else: return False

def si(el):
    newel = re.match("si[ ]+(?P<arguments>.+)[ ]+alors", el, re.IGNORECASE)
    if newel: return f'if ({newel.group("arguments")}):'
    else: return False
    


def sinonsi(el):
    newel = re.match("sinonsi[ ]+(?P<arguments>.+)[ ]+alors", el, re.IGNORECASE)
    if newel: return f'elif ({newel.group("arguments")}):'
    else: return False


def sinon(el):
    newel = re.match("sinon[ ]*:?", el, re.IGNORECASE)
    if newel: return f"else :"
    else: return False
