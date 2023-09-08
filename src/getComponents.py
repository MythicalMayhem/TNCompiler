import re


class dissect:
    algo:list
    tdo :list
    tdnt:list
    Name:str
def get(filePath: str):
    f1 = open(str(filePath), "r", encoding="utf-8")
    f = f1.readlines()
    res = []
    for i in range(len(f) - 1, -1, -1):
        if f[i].strip() == "fin":
            f = f[0 : i + 1]
            break
    for i, v in enumerate(f):
        if v.strip() == "":
            continue
        res.append({i + 1: re.sub(" +", " ", v).replace("\n", "").strip()})
    result = dissect
    for i, v in enumerate(res):
        if re.match("^(algorithme) ", list(res[i].values())[0], re.IGNORECASE):
            result.algo = res[i+1:-1]
            result.Name = res[i]
            variables   = res[0:i]
            for i, v in enumerate(variables): 
                if list(variables[i].values())[0] == "#TDO":
                    result.tdo = variables[i + 1 : :]
                    result.tdnt = variables[1:i]
            break
    f1.close()
    return result