import random
import math
import numpy as np
def estnum(n):return n.isnumeric()
def majus(s):return s.upper()
def minus(s):return s.lower()
def valeur(n):return int(n)
def convch(e):return str(e)
def long(n):return len(n)
def sous_chaine(chaine,start,length):return chaine[start:length]
def racine_carree(n):return math.sqrt(n)
def     puissance(x,y):return math.pow(x,y)
def arrondi(n):return round(n)
def alea(min,max):return random.randint(min,max)
def ecrire(*args):
    L = []
    for i in args:L.append(str(i));print(' '.join(L))
def ecrire_nl(*args):
    L = []
    for i in args:L.append(str(i));print(' '.join(L)+'\n')
vrai = Vrai = True
faux = Faux = False
class test:
	x = 0 
	tab = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 

x = 0
T = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]#debut#14
while True :#15
	pass#15
	ecrire('sai'gdf'sdfg'dfg'k'jfgh'dsg'dsfg'sir x')#16
	if type(x) is bool :#17
		x= bool(input())#17
	elif type(x) is float:#17
		x= float(input())#17
	elif type(x) is int:#17
		x= int(input())#17
	else:#17
		x= input()#17
#	finsi#17
	if (10<x<20):#18
		break#18
#finsi#18
for i in range(0,x):#20
	pass#20
	ecrire('T['+convch(i)+']')#21
	if type(T[i]) is bool :#22
		T[i]= bool(input())#22
	elif type(T[i]) is float:#22
		T[i]= float(input())#22
	elif type(T[i]) is int:#22
		T[i]= int(input())#22
	else:#22
		T[i]= input()#22
#	finsi#22
#fin_pour#23
ecrire(T)#25
