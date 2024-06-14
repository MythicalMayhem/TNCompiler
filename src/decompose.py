import re
def get(lines:list) -> None:  
    tdnt = -1
    tdo = -1
    algo = len(lines)

    for i in range(len(lines)):
        if re.match("^(algorithme) ", lines[i], re.IGNORECASE):
            tdo = i-1
            break
        if re.match("^(#tdo)", lines[i], re.IGNORECASE):
            tdnt = i-1 

    return tdnt+1, tdo, algo

 