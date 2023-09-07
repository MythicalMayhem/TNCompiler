import re 
import subprocess

from compress import arraying
def zeroclamp(n):
    if n < 0:
        return 0
    return n

def indent(translated):
    result = []
    indent = 0
    for i in range(0, len(translated)):
        translated[i] = re.sub(" +", " ", str(translated[i])).strip()
        starter = translated[i].strip()
        if re.match("d.but", starter, re.IGNORECASE):
            result.append("#" + "\t" * (indent - 1) + str(translated[i]) + "\n")
        elif re.match("^(fin[-_ ]?selon)", starter, re.IGNORECASE):
            indent = zeroclamp(indent - 2)
            result.append("#" + "\t" * (indent) + str(translated[i]) + "\n")
        elif re.match(
            "^((fin[-_ ]?pour)|(fin[-_ ]?si)|(fin)|(fin[-_ ]?tant[-_ ]?que))",
            starter,
            re.IGNORECASE,
        ):
            indent = zeroclamp(indent - 1)
            result.append("#" + "\t" * (indent) + str(translated[i]) + "\n")

        elif re.match("break", starter, re.IGNORECASE):
            result.append("\t" * (indent) + str(translated[i]) + "\n")
            indent = zeroclamp(indent - 1)
        elif re.match("^(if|while|def|for)", starter, re.IGNORECASE):
            result.append("\t" * indent + str(translated[i]) + "\n")
            indent += 1
        elif re.match("^match", starter, re.IGNORECASE):
            result.append("\t" * indent + str(translated[i]) + "\n")
            indent += 2
        elif re.match("elif|else|case", starter, re.IGNORECASE):
            result.append("\t" * (zeroclamp(indent - 1)) + str(translated[i]) + "\n")
        else:
            result.append(("\t" * indent) + str(translated[i]) + "\n")
    return result

def commit(tdo,tdnt,indented,where):
    predef = open("predefined.py", "r").readlines()
    final = []
    final += predef
    final += arraying(tdnt.classes)
    final += tdo
    final += indented
    f = open(where, "w+")
    f.writelines(final)
    f.close()
def run(what):
    subprocess.call(what, shell=True)