import random
import math
 
def estnum(n):return n.isnumeric()
def valeur(n):return int(n)
def racine_carree(n):return math.sqrt(n)
def arrondi(n):return round(n)
def alea(min,max):return random.randint(min,max)

def long(n):return len(n)
def convch(e):return str(e)
def sous_chaine(chaine,start,length):return chaine[start:length]
def majus(s):return s.upper()
def minus(s):return s.lower()

def ecrire(*args):print(' '.join(args))
