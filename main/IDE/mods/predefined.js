function __writeinterminal(s) {
    let parent = document.getElementById('innerTerminal')
    let node = document.createElement('div')
    node.innerText = s
    parent.appendChild(node)
}
function input(name) {
    let terminal = document.getElementById('innerTerminal')
    let x = prompt(`${name} = `)
    if (!x) { throw 'exit' }
    let wrapper = document.createElement('div')
    wrapper.innerText = `   <sys> ${name} <---- ${x}`
    terminal.appendChild(wrapper)
    return x
}

function estnum(n) { return !isNaN(parseFloat(n)) && isFinite(n); }
function majus(s) { return s.toUpperCase() }
function minus(s) { return s.toLowerCase() }
function valeur(n) { return Number(n) }
function convch(e) { return String(e) }
function long(n) { return n.length }
function sous_chaine(chaine, start, length) { return chaine.substring(start, length) }
function racine_carree(n) { return Math.sqrt(n) }
function puissance(x, y) { return Math.pow(x, y) }
function abs(n) { return Math.abs(n) }
function arrondi(n) { return Math.round(n) }
function alea(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max) + 1;
    return Math.floor(Math.random() * (max - min) + min)
}
function ecrire() {
    L = []
    for (i of arguments) {
        L.push(String(i))
    }
    __writeinterminal(L.join(' '))
}
function ecrire_nl() {
    L = []
    for (i of arguments) {
        L.push(String(i));
    }
    __writeinterminal(L.join(' ') + '\n')
}
vrai = Vrai = true
faux = Faux = false