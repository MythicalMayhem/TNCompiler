def format(lines:list,start:int,end:int,tdnt:dict)->dict:
    vars = {}
    for i in range(start,end):
        line = lines[i]
        key = line.split(':')[0].strip()
        value = line.split(':')[1].strip()

        if   value in list(tdnt.keys()): vars[key] = tdnt[value]
        elif value == "chaine"  : vars[key] = "''"
        elif value == "entier"  : vars[key] = 0
        elif value == "float"   : vars[key] = 0.0
        elif value == "booleen" : vars[key] = False
    return vars