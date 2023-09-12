//import random
//import math
//import numpy as np
function __writeinterminal(s) {
    //write in terminal
}
function input() {
    //write in terminal
}

function estnum(n) { return !isNaN(parseFloat(n)) && isFinite(n); }
function majus(s) { return s.toUpperCase() }
function minus(s) { return s.toLowerCase() }
function valeur(n) { return Number(n) }
function convch(e) { return String(e) }
function long(n) { return n.length }
function sous_chaine(chaine, start, length) { return chaine.substring(start, length) }
function racine_carree(n) { return math.sqrt(n) }
function puissance(x, y) { return math.pow(x, y) }
function arrondi(n) { return math.round(n) }
function alea(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max)+1;
    return Math.floor(Math.random() * (max - min) + min)
}
function ecrire() {
    L = []
    for (i of arguments) {
        L.push(str(i))
        __writeinterminal(' '.join(L))
    }
}
function ecrire_nl() { 
    L = []
    for (i of arguments) {
        L.push(str(i));
        __writeinterminal(' '.join(L) + '\n')
    }
}
vrai = Vrai = true
faux = Faux = false