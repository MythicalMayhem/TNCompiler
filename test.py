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
x = 0
T = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
while True :
	pass
	ecrire('saisir x')
	if type(x) is bool :
		x= bool(input())
	elif type(x) is float:
		x= float(input())
	elif type(x) is int:
		x= int(input())
	else:
		x= str(input())
#	finsi
	if (10<x<20):
		break
#finsi

for i in range(0,x):
	pass
	ecrire('T['+convch(i)+']')
	if type(T[i]) is bool :
		T[i]= bool(input())
	elif type(T[i]) is float:
		T[i]= float(input())
	elif type(T[i]) is int:
		T[i]= int(input())
	else:
		T[i]= str(input())
#	finsi
#fin_pour

ecrire(T)
