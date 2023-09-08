import re


class TDNTtamplates:
    tables: dict
    Matrices: dict
    classes: list
    classNames: list


def createVar(name, type, templates):
    if type == "entier":
        return f"{name} = 0"
    elif type in ["chaine", "caractere"]:
        return f'{name} = ""'
    elif type == "reel":
        return f"{name} = 0.0"
    elif type == "booleen":
        return f"{name} = False"
    elif type in templates.classes:
        return f'{name} = {type} + "()"'
    elif type in list(templates.tables.keys()):
        return createTable(
            type, templates.tables[type][0], templates.tables[type][1], templates
        )


def createClass(enregistrement, template):
    classlist = []
    classlist.append(f"class {list(enregistrement.keys())[0]}:\n")
    enrdesc = dict(list(enregistrement.values())[0])
    for i, v in enumerate(enrdesc):
        classlist.append(f"\t{createVar(v,enrdesc[v],template)} \n")

    classlist.append("\n")
    return classlist


def createTable(name, length, type, templates):
    tab = []
    if type == "entier":
        tab = [0]
        return f"{name} = {str(tab*length)}"
    elif type in ["chaine", "caractere"]:
        tab = [""]
        return f"{name} = {str(tab*length)}"
    elif type == "reel":
        tab = [0.0]
        return f"{name} = {str(tab*length)}"
    elif type == "booleen":
        tab = [False]
        return f"{name} = {str(tab*length)}"
    elif type in list(templates.tables.values()):
        return f"{name} = {str([]*length)}"
    elif type in templates.classes:
        return f"{name} = {str((type + '()')*length)}"
    return f"{name} = [{','.join(tab)}]\n"


def createMatrix(name, row, col, type, templates):
    if type == "entier":
        return f"{name} = np.array([([int()]*{col})]*{row})"
    elif type in ["chaine", "caractere"]:
        return f"{name} = np.array([([str()]*{col})]*{row})"
    elif type == "reel":
        return f"{name} = np.array([([float()]*{col})]*{row})"
    elif type == "booleen":
        return f"{name} = np.array([([bool()]*{col})]*{row})"
    elif type in templates.classNames:
        return f"{name} = np.array([([{type}()]*{col})]*{row})"
    elif type in list(templates.tables.keys()):
        return f"{name} = np.array([([{createTable(type,templates.tables[type][0],templates.tables[type][1],templates)}]*{col})]*{row})"
    else:
        return f"{name} = np.array([([{type}]*{col})]*{row})"


def formatTDNT(tdnt):
    newObjects = TDNTtamplates()
    newObjects.tables = {}
    newObjects.Matrices = {}
    newObjects.classes = []
    newObjects.classNames = []
    for i, V in enumerate(tdnt):
        k = list(V.keys())[0]
        v = list(V.values())[0].strip()
        if v in ["fin", "debut", "", "__SKIP__"]:
            continue
        if (v.find(":") == -1) and (v[0:8] != "tableau "):
            estr = f"declaration d'objet invalide dans TDNT ligne {i} :{v} "
            raise Exception(estr)

        key = v.strip().split(":")[0].strip()
        Ivalue = v.strip().split(":")[1].strip()
        s1 = re.match(
            "^tableau[ ]+de[ ]+(?P<long>[0-9]+)[ ]+(?P<type>[0-9a-z]+)$",
            Ivalue.strip(),
            re.IGNORECASE,
        )
        s2 = re.match(
            "^(tableau|matrice)[ ]+de[ ]+(((?P<rows1>[0-9]+)[ ]+lignes \* (?P<cols1>[0-9]+)[ ]+colonnes)|((?P<cols2>[0-9]+)[ ]+colonnes) \* (?P<rows2>[0-9]+)[ ]+lignes)[ ]*(?P<type>[a-z][0-9a-z]*)$",
            Ivalue.strip(),
            re.IGNORECASE,
        )
        if Ivalue == "enregistrement":
            for j in range(i, len(tdnt)):
                if list(tdnt[j].values())[0].strip() == "fin":
                    details = tdnt[i : j + 1][2:-1]
                    for exp in range(i, j + 1):
                        tdnt[exp] = {k: "__SKIP__"}
                    detailsdict = {}
                    for H in details:
                        if H in ["fin", "debut", ""]:
                            continue

                        detailsdict[list(H.values())[0].split(":")[0]] = list(
                            H.values()
                        )[0].split(":")[1]
                    newObjects.classes.append(
                        createClass({key: detailsdict}, newObjects)
                    )
                    newObjects.classNames.append(key.strip())

                    break

        elif s1:
            if s1 and s1.group("long") and s1.group("type"):
                newObjects.tables[key] = [int(s1.group("long")), s1.group("type")]
        elif s2:
            if s2:
                if s2.group("rows1") and s2.group("cols1") and s2.group("type"):
                    newObjects.Matrices[key] = [
                        int(s2.group("rows1")),
                        int(s2.group("cols1")),
                        s2.group("type"),
                    ]
                elif s2.group("rows2") and s2.group("cols2") and s2.group("type"):
                    newObjects.Matrices[key] = [
                        int(s2.group("rows2")),
                        int(s2.group("cols2")),
                        s2.group("type"),
                    ]
    return newObjects


def formatTDO(tdo, tdnt):
    template = formatTDNT(tdnt)
    tdoDict = {}
    for i, v in enumerate(tdo):
        v = list(v.values())[0].strip()
        if v == "":
            continue
        keys = v.split(":")[0].strip()
        val = v.split(":")[1].strip()
        for j in keys:
            tdoDict[j] = val
    tdoResult = []
    for i in tdoDict:
        s1 = re.match(
            "^tableau[ ]+de[ ]+(?P<long>[0-9]+)+[ ]+(?P<type>[0-9a-z]+)$",
            tdoDict[i],
            re.IGNORECASE,
        )
        s2 = re.match(
            "^(tableau|matrice)[ ]+de[ ]+(((?P<rows1>[0-9]+)[ ]+lignes \* (?P<cols1>[0-9]+)[ ]+colonnes)|((?P<cols2>[0-9]+)[ ]+colonnes) \* (?P<rows2>[0-9]+)[ ]+lignes)[ ]*(?P<type>[a-z][0-9a-z]*)$",
            tdoDict[i].strip(),
            re.IGNORECASE,
        )
        if tdoDict[i] in list(template.tables.keys()):
            tbl = createTable(
                i,
                int(template.tables[tdoDict[i]][0]),
                template.tables[tdoDict[i]][1],
                template,
            )
            tdoResult.append(tbl)
        elif tdoDict[i] in list(template.Matrices.keys()):
            tbl = createMatrix(
                i,
                int(template.Matrices[tdoDict[i]][0]),
                int(template.Matrices[tdoDict[i]][1]),
                template.Matrices[tdoDict[i]][2],
                template,
            )
            tdoResult.append(tbl)
        elif s1:
            if s1 and s1.group("long") and s1.group("type"):
                tbl = createTable(i, int(s1.group("long")), s1.group("type"))
                tdoResult.append(tbl)
        elif s2: 
            if s2:
                if (s2.group("rows1") and s2.group("cols1")) and s2.group("type"):
                    tbl = createMatrix(
                        int(s2.group("rows1")), int(s2.group("cols1")), s2.group("type")
                    )
                    tdoResult.append(tbl)
                elif (s2.group("rows2") and s2.group("cols2")) and s2.group("type"):
                    tbl = createMatrix(
                        int(s2.group("rows2")), int(s2.group("cols2")), s2.group("type")
                    )
                    tdoResult.append(tbl)
        else:
            if createVar(i.strip(), tdoDict[i].strip(), template):
                tdoResult.append(
                    createVar(i.strip(), tdoDict[i].strip(), template) + "\n"
                )
            else:
                tdoResult.append(i + f"={tdoDict[i]}\n")
    return tdoResult
