 

const codeArea = document.querySelector('#main').querySelector('textarea')
const submit = document.querySelector('#main').querySelector('button') 
submit.addEventListener('click', () => { 
    // console.log(isBoucleFor('pour i de     10 a n faire'))
    // console.log(isSi('si (test) alors'))
    // console.log(isFonction('fonction test(@args:ersd,@asdfadf:rwe,adsf,adf,a):test'))
    // console.log(isProcedure('procedure test(@args:ersd,@asdfadf:rwe,adsf,adf,a):test'))
    // console.log(isTantque('tantque test'))
    let f = codeArea.value.split('\n')
    let lines = {}
    for (const i in f ) {
        let line = codeArea.value.split('\n')[i]
        lines[i.toString()] = line
    }
    //console.log(lines)
    translateLines([{1:'selon "je suis"'}])
}) 
