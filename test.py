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
class eleve:
	age = 0 
	nom = "" 
	moyenne = 0.0 
	succes = False 

class eleve:
	age = 0 
	nom = "" 
	moyenne = 0.0 
	succes = False 

a = 0
b = ""
c = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
d = [eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve()]
e = [eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve(),eleve()]
f = np.array([([int()]*20)]*10)
if type(a) is bool :
	a= bool(input())
elif type(a) is float:
	a= float(input())
elif type(a) is int:
	a= int(input())
else:
	a= str(input())
#finsi

ecrire(a,"oldA")
def nom (a):#entier
	pass
#debut
	a = 'v'
	ecrire(a,"dans fonction")
	globals()[str("a")]=a
#fin

nom(a)
ecrire(a,"outside fonction")

def nom (parametres_formels):#entier
	pass
	__OLDparametres_formels = parametres_formels
	début
	
	parametres_formels = __OLDparametres_formels
#fin
