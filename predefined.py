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
