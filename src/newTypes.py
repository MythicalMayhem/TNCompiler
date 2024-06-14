import re
 

def get(lines:list, start:int, end:int)->None:
    vars = {'enregistrement':[],'tables':[],'matrices':[]}
    TDNT = {}
  
    i = start
    while i<end+1:
        if i == end:break
        line = lines[i].strip()
        key = line.split(":")[0].strip()
        Ivalue = line.split(":")[1].strip()  
        if Ivalue== "enregistrement": 
            fin = -1
            j = i
            while (fin==-1) and (j!=end):
                j +=1
                if lines[j].strip() == 'fin':
                    fin = j
                    TDNT[key] = lines[i+2:j]
                    vars["enregistrement"].append(key)
                    i = j+2
                    break 
            continue 
        s1 = re.match("^(tableau)[ ]+de[ ]+(?P<long>[0-9]+)+[ ]+(?P<type>[0-9a-z]+)$", Ivalue, re.IGNORECASE)
        if   s1 and s1.group("long") and s1.group("type") : 
            TDNT[key] = [int(s1.group("long")), s1.group("type")]
            vars["tables"].append(key)
            i = i+1
            continue 
        
        s2 = re.match("^(tableau|matrice)[ ]+de[ ]+(((?P<rows1>[0-9]+)[ ]+lignes \* (?P<cols1>[0-9]+)[ ]+colon?nes)|((?P<cols2>[0-9]+)[ ]+colon?nes) \* (?P<rows2>[0-9]+)[ ]+lignes)[ ]*(?P<type>[a-z][0-9a-z]*)$", Ivalue, re.IGNORECASE)
        if   s2 and s2.group("rows1") and s2.group("cols1") and s2.group("type") :
            TDNT[key] = [int(s2.group("rows1")), int(s2.group("cols1")), s2.group("type") ]
            vars['matrices'].append(key)
        elif s2 and s2.group("rows2") and s2.group("cols2") and s2.group("type") :
            TDNT[key] = [int(s2.group("rows2")), int(s2.group("cols2")), s2.group("type") ]
            vars['matrices'].append(key)

        i = i +1  
    return vars,TDNT

def createVar(type:str,vars:list,tdnt:dict):
    if   type == "chaine"  : return "''"
    elif type == "entier"  : return 0
    elif type == "float"   : return 0.0
    elif type == "booleen" : return False
    elif type in vars['tables']         : return createTable(tdnt[type][0],tdnt[type][1],vars,tdnt)
    elif type in vars['matrices']       : return createMatrix(tdnt[type][0],tdnt[type][1],tdnt[type][2],vars,tdnt)
    elif type in vars['enregistrement'] : return createClass(tdnt[type],vars,tdnt)

def createTable(size:int,type:str,vars:list,tdnt:dict)->str          : return f'numpy.array([{createVar(type,vars,tdnt)}] *{size})'
def createMatrix(rows:int,cols:int,type:str,vars:list,tdnt:dict)->str: return f'numpy.array([[{createVar(type,vars,tdnt)}] *{cols}]*{rows})'
def createClass(key,items:list,vars:list,tdnt:dict):
    ch = [f'class {key}'] 
    for item in items : 
        name   = item.split(':')[0].strip()    
        type = item.split(':')[1].strip()    
        ch.append(f'\t{name} ={str(createVar(type,vars,tdnt))}')
    return ch

def format(vars:list,tdnt:dict):
    ch = {} 
    for key in (tdnt.keys()): 
        if   key in vars['tables']   : ch[key]=createTable(tdnt[key][0],tdnt[key][1],vars,tdnt)
        elif key in vars['matrices'] : ch[key]=createMatrix(tdnt[key][0],tdnt[key][1],tdnt[key][2],vars ,tdnt)
        elif key in vars['enregistrement']  : ch[key]=createClass(key,tdnt[key],vars,tdnt)
 
    return ch


