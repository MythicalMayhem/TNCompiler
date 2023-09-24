function saisir() {
    /*debut*/
    while (true) {
        if ((typeof N) === 'boolean') { N = Boolean(input('N')) }
        else if (typeof N === 'number' && !Number.isNaN(N) && !Number.isInteger(N)) { N = parseFloat(input('N')) }
        else if (typeof N === 'number' && !Number.isNaN(N) && Number.isInteger(N)) { N = parseInt(input('N')) }
        else { N = input('N') } if (5 <= N && N <= 20) { break; };
    };/*finsi*/
};/*fin*/
function remplire(T, N) {
    __OLDN = N;/*debut*/
    for (let i = 0; i < (N - 1); i += 1) { T[i] = alea(10, 50); };/*finpour*/
};/*fin*/
function Calcul(T, N, ind) {
    __OLDT = T; __OLDN = N;
    __OLDind = ind;/*debut*/
    right = 0;
    left = 0;
    for (let i = 0; i < (ind); i += 1) { left = left + T[i]; };/*finpour*/
    for (let i = ind + 1; i < (N - 1); i += 1) { right = right + T[i]; };/*finpour*/
};/*fin*/;
function chercher(T, N) {/*entier*/__OLDT = T; __OLDN = N;/*debut*/index = 10000;
    for (let i = 1; i < (N - 1); i += 1) { if (Calcul(T, N, i) < index) { index = Calcul(T, N, i); };/*finsi*/ };/*finpour*/
    ecrire(index);
};/*fin*/;
saisir();
remplire(T, N);
chercher(T, N);
ecrire(T);