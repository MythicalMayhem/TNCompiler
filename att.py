import numpy as np


class obj:
    t = "x"


# mat=np.array([([obj]*3)]*2)

x = "sd"


def nom(x):
    x = "s"
    globals()["x"] = x


nom("x")

if 'a' in globals() :
    if type(a) is bool :
        a= bool(input())
    elif type(a) is float:
        a= float(input())
    elif type(a) is int:    
        a= int(input())
    elif type(a) is str :
    	a= str(input())
else:
    errstr = f'a invalide'
    raise Exception(errstr)
print(a)